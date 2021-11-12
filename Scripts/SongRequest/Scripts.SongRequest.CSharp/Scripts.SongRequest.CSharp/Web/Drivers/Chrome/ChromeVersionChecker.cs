using System;
using System.Runtime.InteropServices;
using Scripts.SongRequest.CSharp.Core.Processes;
using WebDriverManager.Helpers;

namespace Scripts.SongRequest.CSharp.Web.Drivers.Chrome
{
    internal static class ChromeVersionChecker
    {
        public static bool DoesDriverVersionEqualToBrowser(string fullDriverPath)
        {
            string rawBrowserVersion = GetRawBrowserVersionViaRegistry();
            string rawDriverVersion = GetChromeDriverVersionViaProcess(fullDriverPath);

            return DoesVersionEqual(rawBrowserVersion, rawDriverVersion);
        }

        private static bool DoesVersionEqual(string rawBrowserVersion, string rawDriverVersion)
        {
            string browserVersionWithoutRevision = VersionHelper.GetVersionWithoutRevision(rawBrowserVersion);
            string driverVersionWithoutRevision = VersionHelper.GetVersionWithoutRevision(rawDriverVersion);

            return StringComparer.OrdinalIgnoreCase.Equals(
                browserVersionWithoutRevision,
                driverVersionWithoutRevision
            );
        }

        private static string GetRawBrowserVersionViaRegistry()
        {
            if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
            {
                return RegistryHelper.GetInstalledBrowserVersionWin("chrome.exe");
            }

            if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux))
            {
                return RegistryHelper.GetInstalledBrowserVersionLinux("google-chrome", "--product-version");
            }

            if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
            {
                return RegistryHelper.GetInstalledBrowserVersionOsx("Google Chrome", "--version");
            }

            throw new PlatformNotSupportedException($"Operating system {RuntimeInformation.OSDescription} is not supported.");
        }

        private static string GetChromeDriverVersionViaProcess(string fullDriverPath)
        {
            const string args = "-v";

            var manager = new ProcessManager();
            string output = manager.GetOutput(fullDriverPath, args);

            return ChromeVersionParser.ParseDriverVersion(output);
        }
    }
}
