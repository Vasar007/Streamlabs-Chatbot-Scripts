using System;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Edge;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Opera;
using Scripts.SongRequest.CSharp.Core.Helpers;
using Scripts.SongRequest.CSharp.Core.Models;
using Scripts.SongRequest.CSharp.Logging;
using Scripts.SongRequest.CSharp.Models.Settings;
using Scripts.SongRequest.CSharp.Web.Drivers;

namespace Scripts.SongRequest.CSharp.Web.Scrapper
{
    public static class HttpWebScrapperFactory
    {
        public static IHttpWebScrapper Create(
            ISongRequestScriptSettings settings,
            IScriptLogger logger)
        {
            logger.Info($"Creating web scrapper for driver '{settings.SelectedBrowserDriver.Value}'.");
            logger.Info($"WebDriver path: [{settings.BrowserDriverPath.Value}].");
            logger.Info($"WebDriver executable name: [{settings.BrowserDriverExecutableName.GetFullFilename()}].");

            var webDriver = CreateWebDriver(settings, logger);
            return new HttpWebScrapper(settings, logger, webDriver);
        }

        private static IWebDriver CreateWebDriver(
            ISongRequestScriptSettings settings,
            IScriptLogger logger)
        {
            EnsureBrowserDriverIsInstalled(settings, logger);

            return settings.SelectedBrowserDriver.Value switch
            {
                WebDriverType.RawEdgeDriver => CreateEdgeDriver(settings),

                WebDriverType.RawChromeDriver => CreateChromeDriver(settings),

                WebDriverType.RawFirefoxDriver => CreateFirefoxDriver(settings),

                WebDriverType.RawOperaDriver => CreateOperaDriver(settings),

                _ => throw new ArgumentOutOfRangeException(
                    nameof(settings.SelectedBrowserDriver),
                    settings.SelectedBrowserDriver,
                    $"Unexpected webdriver type value: '{settings.SelectedBrowserDriver.Value}'."
                )
            };
        }

        private static IWebDriver CreateEdgeDriver(ISongRequestScriptSettings settings)
        {
            using var scope = new DisposableScope();

            bool enableWebDriverDebug = settings.EnableWebDriverDebug;
            FilePath driverDirPath = settings.BrowserDriverPath;
            string driverExecutableFileName = settings.BrowserDriverExecutableName.GetFullFilename();

            var driverService = scope.Capture(
                EdgeDriverService.CreateDefaultService(driverDirPath.Value, driverExecutableFileName)
            );
            SetCommonDriverServiceSettings(driverService, enableWebDriverDebug);
            driverService.UseVerboseLogging = enableWebDriverDebug;

            var options = new EdgeOptions();

            var driver = new EdgeDriver(driverService, options);
            return scope.ReleaseAllAndReturn(driver);
        }

        private static IWebDriver CreateChromeDriver(ISongRequestScriptSettings settings)
        {
            using var scope = new DisposableScope();

            bool enableWebDriverDebug = settings.EnableWebDriverDebug;
            FilePath driverDirPath = settings.BrowserDriverPath;
            string driverExecutableFileName = settings.BrowserDriverExecutableName.GetFullFilename();

            var driverService = scope.Capture(
                ChromeDriverService.CreateDefaultService(driverDirPath.Value, driverExecutableFileName)
            );
            SetCommonDriverServiceSettings(driverService, enableWebDriverDebug);
            driverService.EnableVerboseLogging = enableWebDriverDebug;

            var options = new ChromeOptions();
            if (!enableWebDriverDebug)
            {
                options.AddArgument(WebDriverArguments.Headless);
                options.AddArgument(WebDriverArguments.MuteAudio);
            }

            var driver = new ChromeDriver(driverService, options);
            return scope.ReleaseAllAndReturn(driver);
        }

        private static IWebDriver CreateFirefoxDriver(ISongRequestScriptSettings settings)
        {
            using var scope = new DisposableScope();

            bool enableWebDriverDebug = settings.EnableWebDriverDebug;
            FilePath driverDirPath = settings.BrowserDriverPath;
            string driverExecutableFileName = settings.BrowserDriverExecutableName.GetFullFilename();

            var driverService = scope.Capture(
                FirefoxDriverService.CreateDefaultService(driverDirPath.Value, driverExecutableFileName)
            );
            SetCommonDriverServiceSettings(driverService, enableWebDriverDebug);

            var options = new FirefoxOptions();
            if (!enableWebDriverDebug)
            {
                options.AddArgument(WebDriverArguments.Headless);
                options.AddArgument(WebDriverArguments.MuteAudio);
            }

            var driver = new FirefoxDriver(driverService);
            return scope.ReleaseAllAndReturn(driver);
        }

        private static IWebDriver CreateOperaDriver(ISongRequestScriptSettings settings)
        {
            using var scope = new DisposableScope();

            bool enableWebDriverDebug = settings.EnableWebDriverDebug;
            FilePath driverDirPath = settings.BrowserDriverPath;
            string driverExecutableFileName = settings.BrowserDriverExecutableName.GetFullFilename();

            var driverService = scope.Capture(
                OperaDriverService.CreateDefaultService(driverDirPath.Value, driverExecutableFileName)
            );
            SetCommonDriverServiceSettings(driverService, enableWebDriverDebug);
            driverService.EnableVerboseLogging = enableWebDriverDebug;

            var options = new OperaOptions();
            if (!enableWebDriverDebug)
            {
                options.AddArgument(WebDriverArguments.Headless);
                options.AddArgument(WebDriverArguments.MuteAudio);
            }

            var driver = new OperaDriver(driverService, options);
            return scope.ReleaseAllAndReturn(driver);
        }

        private static void SetCommonDriverServiceSettings(DriverService driverService,
            bool enableWebDriverDebug)
        {
            driverService.SuppressInitialDiagnosticInformation = enableWebDriverDebug;
            driverService.HideCommandPromptWindow = !enableWebDriverDebug;
        }

        private static void EnsureBrowserDriverIsInstalled(
            ISongRequestScriptSettings settings,
            IScriptLogger logger)
        {
            var driverProvider = DriverProviderFactory.Create(settings, logger);
            driverProvider.ProvideBrowserDriver();
        }
    }
}
