using System;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Edge;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Opera;
using OpenQA.Selenium.Remote;
using Scripts.SongRequest.CSharp.Logging;
using Scripts.SongRequest.CSharp.Models.Settings;

namespace Scripts.SongRequest.CSharp.Web
{
    public static class HttpWebScrapperFactory
    {
        public static HttpWebScrapper Create(
          ISongRequestScriptSettings settings,
          IScriptLogger logger,
          string driverDirPath,
          string driverType)
        {
            logger.Info($"Creating web scrapper for driver '{driverType}' from [{driverDirPath}].");

            var webDriver = CreateWebDriver(driverDirPath, driverType);
            return new HttpWebScrapper(settings, logger, webDriver);
        }

        private static RemoteWebDriver CreateWebDriver(string driverDirPath, string driverType)
        {
            return driverType switch
            {
                "Edge" => new EdgeDriver(driverDirPath),

                "Chromium/Chrome" => new ChromeDriver(driverDirPath),

                "Firefox" => new FirefoxDriver(driverDirPath),

                "Opera" => new OperaDriver(driverDirPath),

                _ => throw new ArgumentOutOfRangeException(
                    nameof(driverType),
                    driverType,
                    $"Unexpected webdriver type value: '{driverType}'."
                )
            };
        }
    }
}