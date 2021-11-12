using System;
using System.IO;
using Scripts.SongRequest.CSharp.Core.Models;
using Scripts.SongRequest.CSharp.Logging;
using Scripts.SongRequest.CSharp.Models.Drivers;
using Scripts.SongRequest.CSharp.Web.Drivers.Chrome;
using Scripts.SongRequest.CSharp.Web.Drivers.Custom;
using WebDriverManager.DriverConfigs;
using WebDriverManager.DriverConfigs.Impl;
using WebDriverManager.Helpers;

namespace Scripts.SongRequest.CSharp.Web.Drivers
{
    public sealed class DriverProvider
    {
        private readonly IScriptLogger _logger;
        private readonly CustomDriverManager _customDriverManager;
        private readonly IDriverConfig _driverConfig;
        private readonly DriverVersion _driverVersion;
        private readonly Architecture _architecture;


        private DriverProvider(
            IScriptLogger logger,
            CustomDriverManager customDriverManager,
            IDriverConfig driverConfig,
            DriverVersion driverVersion,
            Architecture architecture)
        {
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
            _customDriverManager = customDriverManager ?? throw new ArgumentNullException(nameof(customDriverManager));
            _driverConfig = driverConfig ?? throw new ArgumentNullException(nameof(driverConfig));
            _driverVersion = driverVersion ?? throw new ArgumentNullException(nameof(driverVersion));
            _architecture = architecture;
        }

        public static DriverProvider Create(
            IScriptLogger logger,
            FilePath driverPath,
            FileName driverExecutableName,
            IDriverConfig driverConfig,
            DriverVersion driverVersion,
            Architecture architecture = Architecture.Auto)
        {
            var driverManager = CustomDriverManager.Create(driverPath, driverExecutableName);
            return new DriverProvider(
                logger: logger,
                customDriverManager: driverManager,
                driverConfig: driverConfig,
                driverVersion: driverVersion,
                architecture: architecture
            );
        }

        public string ProvideBrowserDriver()
        {
            _logger.Debug("Checking browser driver.");

            string fullDriverPath = _customDriverManager.ConstructFullDriverPath();
            bool canAutoResolveVersion = CanAutoResolveVersion();

            // Check whether browser file exists.
            if (File.Exists(fullDriverPath))
            {
                // If it is exist, check whether we can resolve it version or not.
                if (!canAutoResolveVersion)
                {
                    _logger.Debug("Browser driver installed, cannot check version, update will be skipped.");
                    return fullDriverPath;
                }

                // If we can autoupdate it, check whether we should update it or not.
                if (ChromeVersionChecker.DoesDriverVersionEqualToBrowser(fullDriverPath))
                {
                    _logger.Debug("Appropriate browser driver installed, update is not required.");
                    return fullDriverPath;
                }

                _logger.Debug("Browser driver must be updated.");
            }
            else
            {
                _logger.Debug("Browser driver is not installed.");
            }

            // Install or update driver.
            return AutoInstallOrUpdateDriver(canAutoResolveVersion);
        }

        private bool CanAutoResolveVersion()
        {
            // We provide autoresolve version for Chrome only.
            return StringComparer.OrdinalIgnoreCase.Equals(
                _driverConfig.GetName(),
                new ChromeConfig().GetName()
            );
        }

        private string AutoInstallOrUpdateDriver(bool canAutoResolveVersion)
        {

            string driverVersionToUse = _driverVersion.GetActualValueToUse(canAutoResolveVersion);
            _logger.Debug($"Driver version to use based on settings: '{driverVersionToUse}'.");

            _logger.Info($"Browser driver for {_driverConfig.GetName()} version {driverVersionToUse} will be installed or updated by script. In case of failure you have to install it by yourself.");

            string binaryPath = _customDriverManager.SetUpDriver(
                _driverConfig, driverVersionToUse, _architecture
            );
            _logger.Debug($"Binary path of the broser driver: [{binaryPath}].");

            return binaryPath;
        }
    }
}
