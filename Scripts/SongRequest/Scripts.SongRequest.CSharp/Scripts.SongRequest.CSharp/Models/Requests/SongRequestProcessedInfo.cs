using System;
using Scripts.SongRequest.CSharp.Core.Helpers;
using Scripts.SongRequest.CSharp.Core.Models;

namespace Scripts.SongRequest.CSharp.Models.Requests
{
    public sealed record SongRequestProcessedInfo
    {
        public UserData UserData { get; init; }
        public DateTime ProcessedTimeUtc { get; init; }
        public string Reason { get; init; }

        public string ProcessedTimeUtcAsString => ProcessedTimeUtc.ToLocalSimpleString();


        public SongRequestProcessedInfo(
            UserData userData,
            DateTime processedTimeUtc,
            string reason)
        {
            if (processedTimeUtc.Kind != DateTimeKind.Utc)
            {
                var message = $"Invalid date time kind: {processedTimeUtc.Kind.ToString()}, expected: Utc.";
                throw new ArgumentException(message);
            }

            UserData = userData ?? throw new ArgumentNullException(nameof(userData));
            ProcessedTimeUtc = processedTimeUtc;
            Reason = reason ?? throw new ArgumentNullException(nameof(reason));
        }

        public static SongRequestProcessedInfo CreateWithUtcNow(
            UserData userData,
            string reason)
        {
            return new SongRequestProcessedInfo(
                userData: userData,
                processedTimeUtc: DateTime.UtcNow,
                reason: reason
            );
        }

        public static SongRequestProcessedInfo CreateWithDecision(
            SongRequestDecision decision)
        {
            decision = decision ?? throw new ArgumentNullException(nameof(decision));

            return new SongRequestProcessedInfo(
                userData: decision.UserData,
                processedTimeUtc: DateTime.UtcNow,
                reason: decision.Reason
            );
        }
    }
}
