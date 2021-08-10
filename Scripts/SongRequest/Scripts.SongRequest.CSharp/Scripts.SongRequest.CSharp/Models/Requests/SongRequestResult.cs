using System;

namespace Scripts.SongRequest.CSharp.Models.Requests
{
    public sealed record SongRequestResult
    {
        public SongRequestModel SongRequest { get; init; }
        public string Description { get; init; }

        public bool IsSuccess => SongRequest.State == SongRequestState.ApprovedAndAddedSuccessfully;


        private SongRequestResult(
            SongRequestModel songRequest,
            string description)
        {
            SongRequest = songRequest ?? throw new ArgumentNullException(nameof(songRequest));
            Description = description ?? throw new ArgumentNullException(nameof(description));
        }

        public static SongRequestResult Success(
            SongRequestModel songRequest)
        {
            return new SongRequestResult(
                songRequest: songRequest.AddToQueue(),
                description: string.Empty
            );
        }

        public static SongRequestResult Fail(
            SongRequestModel songRequest,
            string description)
        {
            return new SongRequestResult(
                songRequest: songRequest.FailToAdd(),
                description: description
            );
        }
    }
}
