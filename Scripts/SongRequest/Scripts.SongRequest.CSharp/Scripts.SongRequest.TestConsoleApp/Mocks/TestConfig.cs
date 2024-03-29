﻿using Scripts.SongRequest.CSharp.Core.Models;
using Scripts.SongRequest.CSharp.Models.Drivers;
using Scripts.SongRequest.CSharp.Models.Settings;

namespace Scripts.SongRequest.TestConsoleApp.Mocks
{
    internal static class TestConfig
    {
        public const int TimeoutToWaitInMilliseconds = 3000;
        public const string ParameterAll = "all";

        public static readonly FilePath BrowserPath = new(@"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe");
        public static readonly FilePath BrowserDriverPath = new(@"C:\Program Files\Common Files\Webdrivers");
        public static readonly FileName BrowserDriverExecutableName = new("chromedriver", ".exe");
        public static readonly DriverVersion BrowserDriverVersion = DriverVersion.Auto;

        public static readonly WebDriverType SelectedBrowserDriver = WebDriverType.ChromeDriver;

        public const bool EnableWebDriverDebug = false;

        public const string ElementIdOfNewSongTextField = "newSong";
        public const string ElementIdOfAddSongButton = "playerAddSong";
        public const bool ShouldParseResult = true;
        public const string DefaultSuccessMessage = "Song has been added";
        public const string ClassNameOfNotificationIcon = "ui-pnotify-icon";
        public const string ClassNameOfSuccessNotificationIcon = "brighttheme-icon-success";
        public const string ClassNameOfErrorNotificationIcon = "brighttheme-icon-error";
        public const string ClassNameOfNotificationDescription = "ui-pnotify-text";
        public const string ElementIdOfSkipSongButton = "playerSkip";
        public const string ElementIdOfRemoveQueueSongButton = "queueRemove";

        public const string NoSongRequestsToSkipMessage = "No songs in playlist available to skip.";
        public const string AutoApproveReason = "Request has been auto-approved";

        public static readonly HttpLink SongLink = new("https://www.youtube.com/watch?v=CAEUnn0HNLM");
    }
}
