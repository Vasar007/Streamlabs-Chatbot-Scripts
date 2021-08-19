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

        string CommandSkipSongRequest { get; }
        int CommandSkipSongRequestCooldown { get; }

        string CommandOptionSongRequest { get; }
        int CommandOptionSongRequestCooldown { get; }
        string SubcommandChangeUserOptionForSongRequests { get; }
        string SubcommandResetNumberOfOrderedSongRequests { get; }

        string ParameterAll { get; }

        #endregion

        #region Setup Group

        HttpLink HttpPageLinkToParse { get; }
        int NumberOfSongRequestsToAdd { get; }
        int WaitingTimeoutForSongRequestsInSeconds { get; }
        int DispatchTimeoutInSeconds { get; }
        int TimeoutToWaitBetweenSongRequestsInSeconds { get; }
        int TimeoutToWaitInMilliseconds { get; }
        bool UseWhisperMessagesToControlSongRequests { get; }
        string ModIdsToWhisper { get; }
        bool LowMessageMode { get; }
        bool EnableCommandProcessing { get; }
        bool EnableLinkValidation { get; }

        #endregion

        #region Parsing Group

        WebDriverType SelectedBrowserDriver { get; }
        FilePath BrowserDriverPath { get; }
        FileName BrowserDriverExecutableName { get; }
        string ElementIdOfNewSongTextField { get; }
        string ElementIdOfAddSongButton { get; }
        string ClassNameOfNotificationIcon { get; }
        string ClassNameOfSuccessNotificationIcon { get; }
        string ClassNameOfErrorNotificationIcon { get; }
        string ClassNameOfNotificationDescription { get; }
        string ElementIdOfSkipSongButton { get; }
        string ElementIdOfRemoveQueueSongButton { get; }

        #endregion

        #region Permission Group

        string PermissionOnAddCancelSongRequest { get; }
        string PermissionInfoOnAddCancelSongRequest { get; }

        string PermissionOnManageSongRequest { get; }
        string PermissionInfoOnManageSongRequest { get; }

        string PermissionDeniedMessage { get; }

        #endregion

        #region Chat Messages Group

        string InvalidCommandCallMessage { get; }
        string TimeRemainingMessage { get; }
        string MaxLimitOfSongRequestsIsExceededMessage { get; }
        string InvalidTargetMessage { get; }
        string NoSongRequestsMessage { get; }
        string SongRequestNumberAndLinkFormat { get; }
        string ProcessedSongRequestNumberAndLinkFormat { get; }
        string AutoApproveReason { get; }
        string NonExistentSongRequestNumberMessage { get; }
        string AlreadyProcessedSongRequestMessage { get; }
        string SongRequestDecisionReasonMessage { get; }
        string SongRequestAddedMessage { get; }
        string SongRequestToApproveMessage { get; }
        string SongRequestApprovedMessage { get; }
        string OnSuccessSongRequestMessage { get; }
        string OnSuccessSongRequestDefaultResultMessage { get; }
        string OnFailureSongRequestMessage { get; }
        string OnFailureSongRequestDefaultErrorMessage { get; }
        string SongRequestRejectedMessage { get; }
        string SongRequestDefaultRejectReason { get; }
        string SongRequestCancelMessage { get; }
        string GotUserSongRequestsMessage { get; }
        string NoUserSongRequestsMessage { get; }
        string ResetUserSongRequestOptionsMessage { get; }
        string InvalidOptionsSubcommandMessage { get; }
        string OptionValueTheSameMessage { get; }
        string OptionValueChangedMessage { get; }
        string FailedToSetOptionMessage { get; }
        string FailedToSetOptionInvalidTypeMessage { get; }
        string FailedToSetOptionInvalidNameMessage { get; }
        string FailedToValidateLinkMessage { get; }
        string CommandProcessingDisabledMessage { get; }
        string SkipAllSongRequestsMessage { get; }
        string SkipCurrentSongRequestMessage { get; }
        string NoSongRequestsToSkipMessage { get; }
        string FailedToSkipSongRequestsMessage { get; }

        #endregion

        #region Debugging Group

        ScriptLogLevel LoggingLevel { get; }
        bool AllowLoggingToFile { get; }
        bool EnableWebDriverDebug { get; }

        #endregion
    }
}
