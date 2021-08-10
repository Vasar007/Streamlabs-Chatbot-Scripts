using System;
using OpenQA.Selenium;
using Scripts.SongRequest.CSharp.Logging;
using Scripts.SongRequest.CSharp.Models.Requests;
using Scripts.SongRequest.CSharp.Models.Settings;

namespace Scripts.SongRequest.CSharp.Web
{
    public sealed class HttpWebScrapper : IDisposable
    {
        private readonly ISongRequestScriptSettings _settings;
        private readonly IScriptLogger _logger;
        private readonly IWebDriver _webDriver;

        private readonly Lazy<IWebElement> _newSongTextFieldLazy;
        private IWebElement NewSongTextField => _newSongTextFieldLazy.Value;

        private readonly Lazy<IWebElement> _addSongButtonLazy;
        private IWebElement AddSongButton => _addSongButtonLazy.Value;


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

        public void OpenUrl()
        {
            string httpPageLinkToParse = _settings.HttpPageLinkToParse;

            if (string.IsNullOrWhiteSpace(httpPageLinkToParse))
            {
                throw new ArgumentException("Failed to open empty link.", nameof(_settings));
            }

            if (StringComparer.OrdinalIgnoreCase.Equals(_webDriver.Url, httpPageLinkToParse))
            {
                _logger.Warning("Trying to open the same URL. Use Refresh method instead.");
                return;
            }

            _logger.Info($"Openning URL: '{httpPageLinkToParse}'.");
            _webDriver.Navigate().GoToUrl(httpPageLinkToParse);
        }

        public void Refresh()
        {
            _logger.Info($"Refreshing URL: '{_webDriver.Url}'.");
            _webDriver.Navigate().Refresh();
        }

        public SongRequestResult Process(SongRequestModel songRequest)
        {
            _logger.Info($"Processing song request [{songRequest}].");

            if (songRequest.State != SongRequestState.ApprovedAndPending)
            {
                string errorMessage = (
                    "Invalid song request to process. Expected " +
                    $"state {nameof(SongRequestState.ApprovedAndPending)}, " +
                    $"actual state {songRequest.State.ToString()}."
                );
                throw new ArgumentException(errorMessage, nameof(songRequest));
            }

            AddNewSong(songRequest);

            return ProcessResult(songRequest);
        }

        private void AddNewSong(SongRequestModel songRequest)
        {
            NewSongTextField.Clear();
            NewSongTextField.SendKeys(songRequest.SongLink.Link);
            AddSongButton.Click();
        }

        private SongRequestResult ProcessResult(SongRequestModel songRequest)
        {
            _logger.Info(
                $"Song request '{songRequest.RequestId.ToString()}' seems to be added, " +
                 "processing result."
            );

            var frame = _webDriver.SwitchTo().Frame(0);
            _logger.Info("Switched to frame 0.");

            var notification = frame.FindElement(
                By.XPath($"//div[@class='{_settings.ClassNameOfNotificationIcon}']")
            );
            _logger.Info("Found notification icon.");

            var success = notification.FindElements(
                By.ClassName(_settings.ClassNameOfSuccessNotificationIcon)
            );
            _logger.Info("Tried to find susccess notification icon.");

            var failure = notification.FindElements(
                By.ClassName(_settings.ClassNameOfErrorNotificationIcon)
            );
            _logger.Info("Tried to find error notification icon.");

            var description = notification.FindElement(
                By.XPath($"//div[@class='{_settings.ClassNameOfNotificationDescription}']")
            );
            var descriptionText = description.Text;
            _logger.Info($"Found notification description: [{descriptionText}].");

            _webDriver.SwitchTo().DefaultContent();
            _logger.Info("Switched back to default content.");

            // Success.
            if (success.Count > 0 && failure.Count == 0)
            {
                _logger.Info(
                    $"Song request '{songRequest.RequestId.ToString()}' processed successfully. " +
                    $"Result: {descriptionText}"
                );
                return SongRequestResult.Success(songRequest);
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
