namespace Scripts.SongRequest.CSharp.Models.Requests
{
    public enum SongRequestState : int
    {
        Unknown = 0,
        WaitingForApproval = 1,
        ApprovedAndPending = 2,
        ApprovedAndProcessing = 3,
        ApprovedAndAddedSuccessfully = 4,
        ApprovedButAddedFailure = 5,
        Rejected = 6,
        Cancelled = 7
    }
}
