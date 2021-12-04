using Moq;
using Scripts.SongRequest.CSharp.Core.Models;
using Scripts.SongRequest.CSharp.Models.Settings;

namespace Scripts.SongRequest.TestConsoleApp.Mocks
{
    internal static class TestSettings
    {
        public static ISongRequestScriptSettings MockSettings(HttpLink httpPageLink)
        {
            var mock = new Mock<ISongRequestScriptSettings>();

            mock.Setup(x => x.ParameterAll).Returns(TestConfig.ParameterAll);

            mock.Setup(x => x.EnableWebDriverDebug).Returns(TestConfig.EnableWebDriverDebug);
            mock.Setup(x => x.BrowserPath).Returns(TestConfig.BrowserPath);
            mock.Setup(x => x.BrowserDriverPath).Returns(TestConfig.BrowserDriverPath);
            mock.Setup(x => x.BrowserDriverExecutableName).Returns(TestConfig.BrowserDriverExecutableName);
            mock.Setup(x => x.BrowserDriverVersion).Returns(TestConfig.BrowserDriverVersion);
            mock.Setup(x => x.SelectedBrowserDriver).Returns(TestConfig.SelectedBrowserDriver);
            mock.Setup(x => x.HttpPageLinkToParse).Returns(httpPageLink);
            mock.Setup(x => x.TimeoutToWaitInMilliseconds).Returns(TestConfig.TimeoutToWaitInMilliseconds);

            mock.Setup(x => x.ElementIdOfNewSongTextField).Returns(TestConfig.ElementIdOfNewSongTextField);
            mock.Setup(x => x.ElementIdOfAddSongButton).Returns(TestConfig.ElementIdOfAddSongButton);
            mock.Setup(x => x.ClassNameOfNotificationIcon).Returns(TestConfig.ClassNameOfNotificationIcon);
            mock.Setup(x => x.ClassNameOfSuccessNotificationIcon).Returns(TestConfig.ClassNameOfSuccessNotificationIcon);
            mock.Setup(x => x.ClassNameOfErrorNotificationIcon).Returns(TestConfig.ClassNameOfErrorNotificationIcon);
            mock.Setup(x => x.ClassNameOfNotificationDescription).Returns(TestConfig.ClassNameOfNotificationDescription);
            mock.Setup(x => x.ElementIdOfSkipSongButton).Returns(TestConfig.ElementIdOfSkipSongButton);
            mock.Setup(x => x.ElementIdOfRemoveQueueSongButton).Returns(TestConfig.ElementIdOfRemoveQueueSongButton);

            mock.Setup(x => x.NoSongRequestsToSkipMessage).Returns(TestConfig.NoSongRequestsToSkipMessage);
            mock.Setup(x => x.AutoApproveReason).Returns(TestConfig.AutoApproveReason);

            return mock.Object;
        }
    }
}
