using Scripts.SongRequest.CSharp.Logging;

namespace Scripts.SongRequest.CSharp.Models.Settings
{
    public interface ISongRequestScriptSettings
    {
        #region Setup Group

        string CommandAddSongRequest { get; }
        int CommandAddSongRequestCooldown { get; }

        string CommandCancelSongRequest { get; }
        int CommandCancelSongRequestCooldown { get; }

        string CommandApproveSongRequest { get; }
        int CommandApproveSongRequestCooldown { get; }

        string CommandRejectSongRequest { get; }
        int CommandRejectSongRequestCooldown { get; }

        string CommandGetSongRequest { get; }
        int CommandGetSongRequestCooldown { get; }

        string CommandUseWhisperSongRequest { get; }
        int CommandUseWhisperSongRequestCooldown { get; }

        string HttpPageLinkToParse { get; }
        int NumberOfSongRequestsToAdd { get; }
        bool UseWhisperMessagesToControlSongRequests { get; }
        int DispatchTimeoutInSeconds { get; }

        string BrowserDriverPath { get; }
        string SelectedBrowserDriver { get; }
        string ElementIdOfNewSongTextField { get; }
        string ElementIdOfAddSongButton { get; }
        string ClassNameOfNotificationIcon { get; }
        string ClassNameOfSuccessNotificationIcon { get; }
        string ClassNameOfErrorNotificationIcon { get; }
        string ClassNameOfNotificationDescription { get; }

        #endregion

        #region Permission Group

        string PermissionOnAddCancelSongRequest { get; }
        string PermissionInfoOnAddCancelSongRequest { get; }
        string PermissionOnApproveRejectGetSongRequest { get; }
        string PermissionInfoOnApproveRejectGetSongRequest { get; }
        string PermissionDeniedMessage { get; }

        #endregion

        #region Permission Group

        string InvalidCommandCallMessage { get; }
        string OnSuccessSongRequestMessage { get; }
        string TimeRemainingMessage { get; }

        #endregion

        #region Debugging Group

        ScriptLogLevel LoggingLevel { get; }
        bool AllowLoggingToFile { get; }

        #endregion
    }
}
