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

            mock.Setup(x => x.HttpPageLinkToParse).Returns(httpPageLink.Link);
            mock.Setup(x => x.ElementIdOfNewSongTextField).Returns(TestConfig.ElementIdOfNewSongTextField);
            mock.Setup(x => x.ElementIdOfAddSongButton).Returns(TestConfig.ElementIdOfAddSongButton);
            mock.Setup(x => x.ClassNameOfNotificationIcon).Returns(TestConfig.ClassNameOfNotificationIcon);
            mock.Setup(x => x.ClassNameOfSuccessNotificationIcon).Returns(TestConfig.ClassNameOfSuccessNotificationIcon);
            mock.Setup(x => x.ClassNameOfErrorNotificationIcon).Returns(TestConfig.ClassNameOfErrorNotificationIcon);
            mock.Setup(x => x.ClassNameOfNotificationDescription).Returns(TestConfig.ClassNameOfNotificationDescription);

            return mock.Object;
        }
    }
}
