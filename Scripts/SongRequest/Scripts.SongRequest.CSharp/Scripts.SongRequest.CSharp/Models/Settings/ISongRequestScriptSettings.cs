using Scripts.SongRequest.CSharp.Core.Models;
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

        HttpLink HttpPageLinkToParse { get; }
        int NumberOfSongRequestsToAdd { get; }
        bool UseWhisperMessagesToControlSongRequests { get; }
        int DispatchTimeoutInSeconds { get; }
        int TimeoutToWaitInMilliseconds { get; }

        FilePath BrowserDriverPath { get; }
        FileName BrowserDriverExecutableName { get; }
        WebDriverType SelectedBrowserDriver { get; }
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

        #region Chat Messages Group

        string InvalidCommandCallMessage { get; }
        string TimeRemainingMessage { get; }
        string MaxLimitOfSongRequestsIsExceededMessage { get; }
        string InvalidTargetMessage { get; }
        string NoSongRequestsMessage { get; }
        string NonExistentSongRequestNumberMessage { get; }
        string SongRequestAddedMessage { get; }
        string SongRequestToApproveMessage { get; }
        string SongRequestApprovedMessage { get; }
        string OnSuccessSongRequestMessage { get; }
        string OnFailureSongRequestMessage { get; }
        string OnFailureSongRequestDefaultErrorMessage { get; }
        string SongRequestRejectedMessage { get; }
        string SongRequestDefaultRejectReason { get; }
        string SongRequestCancelMessage { get; }

        #endregion

        #region Debugging Group

        ScriptLogLevel LoggingLevel { get; }
        bool AllowLoggingToFile { get; }
        bool EnableWebDriverDebug { get; }

        #endregion
    }
}
