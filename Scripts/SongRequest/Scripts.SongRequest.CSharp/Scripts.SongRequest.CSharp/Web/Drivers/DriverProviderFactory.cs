using System;
using Scripts.SongRequest.CSharp.Logging;
using Scripts.SongRequest.CSharp.Models.Settings;
using WebDriverManager.DriverConfigs;
using WebDriverManager.DriverConfigs.Impl;
using WebDriverManager.Helpers;

namespace Scripts.SongRequest.CSharp.Web.Drivers
{
    public static class DriverProviderFactory
    {
        public static DriverProvider Create(
            ISongRequestScriptSettings settings,
            IScriptLogger logger,
            Architecture architecture = Architecture.Auto)
        {
            return settings.SelectedBrowserDriver.Value switch
            {
                WebDriverType.RawEdgeDriver => CreateForEdge(settings, logger, architecture),

                WebDriverType.RawChromeDriver => CreateForChrome(settings, logger, architecture),

                WebDriverType.RawFirefoxDriver => CreateForFirefox(settings, logger, architecture),

                WebDriverType.RawOperaDriver => CreateForOpera(settings, logger, architecture),

                _ => throw new ArgumentOutOfRangeException(
                    nameof(settings.SelectedBrowserDriver),
                    settings.SelectedBrowserDriver,
                    $"Unexpected webdriver type value: '{settings.SelectedBrowserDriver.Value}'."
                )
            };
        }

        private static DriverProvider CreateForEdge(
            ISongRequestScriptSettings settings,
            IScriptLogger logger,
            Architecture architecture)
        {
            return CreateWithConfig(settings, logger, architecture, new EdgeConfig());
        }

        private static DriverProvider CreateForChrome(
            ISongRequestScriptSettings settings,
            IScriptLogger logger,
            Architecture architecture)
        {
            return CreateWithConfig(settings, logger, architecture, new ChromeConfig());
        }

        private static DriverProvider CreateForFirefox(
            ISongRequestScriptSettings settings,
            IScriptLogger logger,
            Architecture architecture)
        {
            return CreateWithConfig(settings, logger, architecture, new FirefoxConfig());
        }

        private static DriverProvider CreateForOpera(
            ISongRequestScriptSettings settings,
            IScriptLogger logger,
            Architecture architecture)
        {
            return CreateWithConfig(settings, logger, architecture, new OperaConfig());
        }

        private static DriverProvider CreateWithConfig(
            ISongRequestScriptSettings settings,
            IScriptLogger logger,
            Architecture architecture,
            IDriverConfig driverConfig)
        {
            return DriverProvider.Create(
                logger: logger,
                driverPath: settings.BrowserDriverPath,
                driverExecutableName: settings.BrowserDriverExecutableName,
                driverConfig: driverConfig,
                driverVersion: settings.BrowserDriverVersion,
                architecture: architecture
            );
        }
    }
}
