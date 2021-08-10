﻿using Scripts.SongRequest.CSharp.Core.Models;
using Scripts.SongRequest.CSharp.Models.Settings;

namespace Scripts.SongRequest.TestConsoleApp.Mocks
{
    internal static class TestConfig
    {
        public const int TimeoutToWaitInMilliseconds = 3000;

        public static readonly FilePath BrowserDriverPath = new("C:\\Program Files\\Common Files\\Webdrivers");
        public static readonly FileName BrowserDriverExecutableName = new("MicrosoftWebDriver.exe");

        public static readonly WebDriverType SelectedBrowserDriver = WebDriverType.EdgeDriver;

        public const bool EnableWebDriverDebug = false;

        public const string ElementIdOfNewSongTextField = "newSong";
        public const string ElementIdOfAddSongButton = "playerAddSong";
        public const string ClassNameOfNotificationIcon = "ui-pnotify-icon";
        public const string ClassNameOfSuccessNotificationIcon = "brighttheme-icon-success";
        public const string ClassNameOfErrorNotificationIcon = "brighttheme-icon-error";
        public const string ClassNameOfNotificationDescription = "ui-pnotify-text";

        public static readonly HttpLink SongLink = new("https://www.youtube.com/watch?v=CAEUnn0HNLM");
    }
}
