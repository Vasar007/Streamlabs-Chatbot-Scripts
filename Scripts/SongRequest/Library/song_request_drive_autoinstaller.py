# coding: utf-8
"""
Helper functions for filename and URL generation.
"""

import sys
import os
import re
import zipfile
import xml.etree.ElementTree as elemTree

from io import BytesIO
from six.moves import urllib

import song_request_helpers as helpers


try:
    from subprocess import DEVNULL
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


def get_variable_separator():
    """
    Returns the environment variable separator for the current platform.
    :return: Environment variable separator
    """
    if helpers.is_windows_platform():
        return ";"
    return ":"


def get_platform_architecture():
    if sys.platform.startswith("linux") and sys.maxsize > 2 ** 32:
        platform = "linux"
        architecture = "64"
    elif sys.platform == "darwin":
        platform = "mac"
        architecture = "64"
    elif helpers.is_windows_platform():
        platform = "win"
        architecture = "32"
    else:
        raise RuntimeError("Could not determine chromedriver download URL for this platform.")
    return platform, architecture


def get_chromedriver_url(version):
    """
    Generates the download URL for current platform , architecture and the given version.
    Supports Linux, MacOS and Windows.
    :param version: chromedriver version string
    :return: Download URL for chromedriver
    """
    base_url = "https://chromedriver.storage.googleapis.com/"
    platform, architecture = get_platform_architecture()
    return base_url + version + "/chromedriver_" + platform + architecture + ".zip"


def find_binary_in_path(filename):
    """
    Searches for a binary named `filename` in the current PATH. If an executable is found, its absolute path is returned
    else None.
    :param filename: Filename of the binary
    :return: Absolute path or None
    """
    if "PATH" not in os.environ:
        return None
    for directory in os.environ["PATH"].split(get_variable_separator()):
        binary = os.path.abspath(os.path.join(directory, filename))
        if os.path.isfile(binary) and os.access(binary, os.X_OK):
            return binary
    return None


def get_chromedriver_version(chromedriver_path):
    version = subprocess.check_output([chromedriver_path, "-v"])
    return re.match(r".*?([\d.]+).*?", version.decode("utf-8"))[1]


def check_version(chromedriver_path, required_version):
    try:
        version = get_chromedriver_version(chromedriver_path)
        if version == required_version:
            return True
    except Exception:
        return False
    return False


def get_chrome_version():
    """
    :return: the version of chrome installed on client
    """
    platform, _ = get_platform_architecture()
    if platform == "linux":
        with subprocess.Popen(["chromium-browser", "--version"], stdout=subprocess.PIPE) as proc:
            version = proc.stdout.read().decode("utf-8").replace("Chromium", "").strip()
            version = version.replace("Google Chrome", "").strip()
    elif platform == "mac":
        process = subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode("UTF-8").replace("Google Chrome", "").strip()
    elif platform == "win":
        process = subprocess.Popen(
            ["reg", "query", "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon", "/v", "version"],
            stdout=subprocess.PIPE, stderr=DEVNULL, stdin=DEVNULL
        )
        version = process.communicate()[0].decode("UTF-8").strip().split()[-1]
    else:
        return
    return version


def get_major_version(version):
    """
    :param version: the full version.
    :return: the major version of input value.
    """
    return version.split(".")[0]


def get_matched_chromedriver_version(version):
    """
    :param version: the version of chrome
    :return: the version of chromedriver
    """
    doc = urllib.request.urlopen("https://chromedriver.storage.googleapis.com").read()
    root = elemTree.fromstring(doc)
    for k in root.iter("{http://doc.s3.amazonaws.com/2006-03-01}Key"):
        if k.text.find(get_major_version(version) + ".") == 0:
            return k.text.split("/")[0]
    return None


def get_chromedriver_path():
    """
    :return: path of the chromedriver binary
    """
    return os.path.abspath(os.path.dirname(__file__))


def print_chromedriver_path():
    """
    Print the path of the chromedriver binary.
    """
    print get_chromedriver_path()


def download_chromedriver(settings, logger):
    """
    Downloads, unzips and installs chromedriver.
    If a chromedriver binary is found in PATH it will be copied, otherwise downloaded.

    :param SongRequestSettings settings: Instance of the script settings.
    :param SongRequestLogger logger: Instance of logger.
    :return: The file path of chromedriver.
    """
    logger.info("Trying to download, unzip and installs chromedriver.")

    chrome_version = get_chrome_version()
    if not chrome_version:
        logger.debug("Chrome is not installed.")
        return
    chromedriver_version = get_matched_chromedriver_version(chrome_version)
    if not chromedriver_version:
        logger.warning("Can not find chromedriver for currently installed chrome version.")
        return
    major_version = get_major_version(chromedriver_version)
    logger.info(
        settings.AutoInstallOrUpdateBrowserDriverMessage
        .format(settings.SelectedBrowserDriver, major_version)
    )

    if not os.path.isdir(settings.BrowserDriverPath):
        raise ValueError("Invalid path: {0}".format(settings.BrowserDriverPath))
    chromedriver_dir = settings.BrowserDriverPath
  
    chromedriver_filename = settings.get_full_browser_driver_filename()
    chromedriver_filepath = os.path.join(chromedriver_dir, chromedriver_filename)
    if not os.path.isfile(chromedriver_filepath) or \
            not check_version(chromedriver_filepath, chromedriver_version):
        logger.info("Downloading chromedriver ({0})...".format(chromedriver_version))
        if not os.path.isdir(chromedriver_dir):
            os.makedirs(chromedriver_dir)
        url = get_chromedriver_url(version=chromedriver_version)
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() != 200:
                raise urllib.error.URLError("Not Found")
        except urllib.error.URLError:
            raise RuntimeError("Failed to download chromedriver archive: {0}".format(url))
        archive = BytesIO(response.read())
        with zipfile.ZipFile(archive) as zip_file:
            zip_file.extract(chromedriver_filename, chromedriver_dir)
    else:
        logger.info("Chromedriver is already installed.")

    if not os.access(chromedriver_filepath, os.X_OK):
        os.chmod(chromedriver_filepath, 0o744)
    return chromedriver_filepath


def autoinstall_or_update_browser_driver(settings, logger):
    # We provide autoinstall for Chrome only.
    download_chromedriver(settings, logger)


def ensure_browser_driver_is_installed(settings, logger):
    browser_driver = settings.get_full_browser_driver_filepath()

    logger.info(
        "Checking browser driver in {0} for selected {1}."
        .format(browser_driver, settings.SelectedBrowserDriver)
    )  # debug

    # Check whether browser file exists.
    if os.path.exists(browser_driver):
        # If autoupdate is not supported, finish validation.
        if not settings.supports_autoinstall():
            logger.info("Browser driver installed, autoupdate is not supported.")
            return

        # If it exists, then try to check driver and autoupdate if needed.
        autoinstall_or_update_browser_driver(settings, logger)
    else:
        # If it is not exist, check that script can autoinstall it.
        if not settings.supports_autoinstall():
            # If cannot, raise exception.
            raise RuntimeError(
                settings.FailedToValidateBrowserDriverMessage
                .format(settings.SelectedBrowserDriver)
            )

        # If can, autoinstall it.
        autoinstall_or_update_browser_driver(settings, logger)
