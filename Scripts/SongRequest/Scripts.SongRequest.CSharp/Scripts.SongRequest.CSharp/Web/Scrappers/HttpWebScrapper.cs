using System;
using OpenQA.Selenium;
using OpenQA.Selenium.Support.UI;
using Scripts.SongRequest.CSharp.Core.Models;
using Scripts.SongRequest.CSharp.Logging;
using Scripts.SongRequest.CSharp.Models.Requests;
using Scripts.SongRequest.CSharp.Models.Settings;

namespace Scripts.SongRequest.CSharp.Web.Scrapper
{
    internal sealed class HttpWebScrapper : IHttpWebScrapper
    {
        private readonly ISongRequestScriptSettings _settings;
        private readonly IScriptLogger _logger;
        private readonly IWebDriver _webDriver;

        private readonly Lazy<IWebElement> _newSongTextFieldLazy;
        private IWebElement NewSongTextField => _newSongTextFieldLazy.Value;

        private readonly Lazy<IWebElement> _addSongButtonLazy;
        private IWebElement AddSongButton => _addSongButtonLazy.Value;

        private TimeSpan TimeoutToWait => TimeSpan.FromMilliseconds(_settings.TimeoutToWaitInMilliseconds);


        internal HttpWebScrapper(
            ISongRequestScriptSettings settings,
            IScriptLogger logger,
            IWebDriver webDriver)
        {
            _settings = settings ?? throw new ArgumentNullException(nameof(settings));
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
            _webDriver = webDriver ?? throw new ArgumentNullException(nameof(webDriver));

            _newSongTextFieldLazy = new Lazy<IWebElement>(() => FindNewSongTextField());
            _addSongButtonLazy = new Lazy<IWebElement>(() => FindAddSongButton());
        }

        private IWebElement FindNewSongTextField()
        {
            return _webDriver.FindElement(By.Id(_settings.ElementIdOfNewSongTextField));
        }

        private IWebElement FindAddSongButton()
        {
            return _webDriver.FindElement(By.Id(_settings.ElementIdOfAddSongButton));
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

        #region IHttpWebScrapper Implementation

        public void OpenUrl()
        {
            HttpLink httpPageLinkToParse = _settings.HttpPageLinkToParse;

            if (!httpPageLinkToParse.HasValue)
            {
                throw new ArgumentException("Failed to open empty link.", nameof(_settings));
            }

            if (StringComparer.OrdinalIgnoreCase.Equals(_webDriver.Url, httpPageLinkToParse))
            {
                _logger.Warning("Trying to open the same URL. Use Refresh method instead.");
                return;
            }

            _logger.Info($"Openning URL: '{httpPageLinkToParse.Value}'.");
            _webDriver.Navigate().GoToUrl(httpPageLinkToParse.Value);
        }

        public void Refresh()
        {
            _logger.Info($"Refreshing URL: '{_webDriver.Url}'.");
            _webDriver.Navigate().Refresh();
        }

        public SongRequestResult Process(SongRequestModel songRequest)
        {
            _logger.Info($"Processing song request [{songRequest}].");

            if (!songRequest.IsApprovedAndProcessing)
            {
                string errorMessage = (
                    "Invalid song request to process. Expected " +
                    $"state {nameof(SongRequestState.ApprovedAndProcessing)}, " +
                    $"actual state {songRequest.State.ToString()}."
                );
                throw new ArgumentException(errorMessage, nameof(songRequest));
            }

            AddNewSong(songRequest);

            return ProcessResult(songRequest);
        }

        #endregion

        private void AddNewSong(SongRequestModel songRequest)
        {
            // Page can be loaded to quickly, need that UI will be available.
            var waiter = new WebDriverWait(_webDriver, TimeoutToWait);
            waiter.IgnoreExceptionTypes(typeof(ElementClickInterceptedException));

            waiter.Until(_ => NewSongTextField.Enabled);
            NewSongTextField.Clear();
            NewSongTextField.SendKeys(songRequest.SongLink.Value);

            waiter.Until(_ =>
            {
                AddSongButton.Click();
                return true;
            });
        }

        private SongRequestResult ProcessResult(SongRequestModel songRequest)
        {
            _logger.Info(
                $"Song request '{songRequest.RequestId.ToString()}' seems to be added, " +
                 "processing result."
            );

            // Page can be loaded to quickly, need that notification will be enabled.
            var waiter = new WebDriverWait(_webDriver, TimeoutToWait);

            var notification = waiter.Until(
                driver => driver.FindElement(By.ClassName(_settings.ClassNameOfNotificationIcon))
            );
            _logger.Debug("Found notification icon.");

            var success = notification.FindElements(
                By.ClassName(_settings.ClassNameOfSuccessNotificationIcon)
            );
            _logger.Debug("Tried to find susccess notification icon.");

            var failure = notification.FindElements(
                By.ClassName(_settings.ClassNameOfErrorNotificationIcon)
            );
            _logger.Debug("Tried to find error notification icon.");

            var description = _webDriver.FindElement(
                By.ClassName(_settings.ClassNameOfNotificationDescription)
            );
            var descriptionText = description.Text;
            _logger.Debug($"Found notification description: [{descriptionText}].");

            // Success.
            if (success.Count > 0 && failure.Count == 0)
            {
                _logger.Info(
                    $"Song request '{songRequest.RequestId.ToString()}' processed successfully. " +
                    $"Result: {descriptionText}"
                );
                return SongRequestResult.Success(songRequest, descriptionText);
            }

            // Failure.
            _logger.Info(
                $"Song request {songRequest.RequestId.ToString()} processed with failure. " +
                $"Error: {descriptionText}"
            );
            return SongRequestResult.Fail(songRequest, descriptionText);
        }
    }
}
