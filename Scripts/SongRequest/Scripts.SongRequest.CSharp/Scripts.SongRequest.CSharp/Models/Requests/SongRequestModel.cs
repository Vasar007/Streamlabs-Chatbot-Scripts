using System;
using Scripts.SongRequest.CSharp.Core.Models;

namespace Scripts.SongRequest.CSharp.Models.Requests
{
    public sealed record SongRequestModel
    {
        public Guid RequestId { get; init; }
        public UserId UserId { get; init; }
        public HttpLink SongLink { get; init; }
        public int RequestNumber { get; init; }
        public SongRequestState State { get; init; }


        public SongRequestModel(
            Guid requestId,
            UserId userId,
            HttpLink songLink,
            int requestNumber,
            SongRequestState state)
        {
            RequestId = requestId;
            UserId = userId ?? throw new ArgumentNullException(nameof(userId));
            SongLink = songLink ?? throw new ArgumentNullException(nameof(songLink));
            RequestNumber = requestNumber;
            State = state;
        }

        public static SongRequestModel CreateNew(
            UserId userId,
            HttpLink songLink,
            int requestNumber)
        {
            return new SongRequestModel(
                requestId: Guid.NewGuid(),
                userId: userId,
                songLink: songLink,
                requestNumber: requestNumber,
                state: SongRequestState.WaitingForApproval
            );
        }

        public SongRequestModel Approve()
        {
            return this with
            {
                State = SongRequestState.ApprovedAndPending
            };
        }

        public SongRequestModel AddToQueue()
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
                State = SongRequestState.Cancelled
            };
        }
    }
}
