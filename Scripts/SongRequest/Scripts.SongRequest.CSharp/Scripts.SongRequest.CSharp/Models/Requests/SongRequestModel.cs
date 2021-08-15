using System;
using Scripts.SongRequest.CSharp.Core.Models;

namespace Scripts.SongRequest.CSharp.Models.Requests
{
    public sealed record SongRequestModel
    {
        public Guid RequestId { get; init; }
        public UserData UserData { get; init; }
        public HttpLink SongLink { get; init; }
        public SongRequestNumber RequestNumber { get; init; }
        public SongRequestState State { get; init; }
        public DateTime CreationTimeUtc { get; init; }

        public bool IsWaitingForApproval => State == SongRequestState.WaitingForApproval;
        public bool IsApprovedAndPending => State == SongRequestState.ApprovedAndPending;
        public bool IsApprovedAndProcessing => State == SongRequestState.ApprovedAndProcessing;
        public bool IsApprovedAndAddedSuccessfully => State == SongRequestState.ApprovedAndAddedSuccessfully;
        public bool IsApprovedButAddedFailure => State == SongRequestState.ApprovedButAddedFailure;
        public bool IsRejected => State == SongRequestState.Rejected;
        public bool IsCanceled => State == SongRequestState.Canceled;


        public SongRequestModel(
            Guid requestId,
            UserData userData,
            HttpLink songLink,
            SongRequestNumber requestNumber,
            SongRequestState state,
            DateTime creationTimeUtc)
        {
            RequestId = requestId;
            UserData = userData ?? throw new ArgumentNullException(nameof(userData));
            SongLink = songLink ?? throw new ArgumentNullException(nameof(songLink));
            RequestNumber = requestNumber ?? throw new ArgumentNullException(nameof(requestNumber));
            State = state;
            CreationTimeUtc = creationTimeUtc;
        }

        public static SongRequestModel CreateNew(
            UserData userData,
            HttpLink songLink,
            SongRequestNumber requestNumber)
        {
            return new SongRequestModel(
                requestId: Guid.NewGuid(),
                userData: userData,
                songLink: songLink,
                requestNumber: requestNumber,
                state: SongRequestState.WaitingForApproval,
                creationTimeUtc: DateTime.UtcNow
            );
        }

        public SongRequestModel Approve()
        {
            return this with
            {
                State = SongRequestState.ApprovedAndPending
            };
        }

        public SongRequestModel StartProcessing()
        {
            return this with
            {
                State = SongRequestState.ApprovedAndProcessing
            };
        }

        public SongRequestModel AddToPlaylist()
        {
            return this with
            {
                State = SongRequestState.ApprovedAndAddedSuccessfully
            };
        }

        public SongRequestModel FailToAdd()
        {
            return this with
            {
                State = SongRequestState.ApprovedButAddedFailure
            };
        }

        public SongRequestModel Reject()
        {
            return this with
            {
                State = SongRequestState.Rejected
            };
        }

        public SongRequestModel Cancel()
        {
            return this with
            {
                State = SongRequestState.Canceled
            };
        }
    }
}
