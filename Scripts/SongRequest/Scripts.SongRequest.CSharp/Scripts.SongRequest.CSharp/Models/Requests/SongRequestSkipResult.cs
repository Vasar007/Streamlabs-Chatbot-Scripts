using System;

namespace Scripts.SongRequest.CSharp.Models.Requests
{
    public sealed record SongRequestSkipResult
    {
        public bool IsSuccess { get; init; }
        public string Description { get; init; }


        private SongRequestSkipResult(
            bool isSuccess,
            string description)
        {
            IsSuccess = isSuccess;
            Description = description ?? throw new ArgumentNullException(nameof(description));
        }

        public static SongRequestSkipResult Success()
        {
            return new SongRequestSkipResult(
                isSuccess: true,
                description: string.Empty
            );
        }

        public static SongRequestSkipResult Fail(
            string description)
        {
            return new SongRequestSkipResult(
                 isSuccess: false,
                description: description
            );
        }
    }
}
