using System;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Edge;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Opera;
using OpenQA.Selenium.Remote;

namespace Scripts.SongRequest.WebScrapper
{
    public sealed class HttpWebScrapper : IDisposable
    {
        private readonly RemoteWebDriver _webDriver;


        private HttpWebScrapper(
            RemoteWebDriver webDriver)
        {
            _webDriver = webDriver ?? throw new ArgumentNullException(nameof(webDriver));
        }

        public static HttpWebScrapper Create(
            string driverDirPath,
            string driverType)
        {
            var webDriver = CreateWebDriver(driverDirPath, driverType);
            return new HttpWebScrapper(webDriver);
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

        #region IDisposable Implementation

        private bool _disposed;

        public void Dispose()
        {
            if (_disposed)
            {
                return;
            }

            _webDriver.Dispose();

            _disposed = true;
        }

        #endregion

        public string Run()
        {
            return _webDriver.Title;
        }
    }
}
