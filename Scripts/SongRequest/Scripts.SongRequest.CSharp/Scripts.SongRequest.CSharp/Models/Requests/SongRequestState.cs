namespace Scripts.SongRequest.CSharp.Models.Requests
{
    public enum SongRequestState : int
    {
        Unknown = 0,
        WaitingForApproval = 1,
        ApprovedAndPending = 2,
        ApprovedAndAddedSuccessfully = 3,
        ApprovedButAddedFailure = 4,
        Rejected = 5,
        Cancelled = 6
    }
}
