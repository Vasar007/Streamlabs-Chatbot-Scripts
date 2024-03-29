﻿using System;
using Scripts.SongRequest.CSharp.Core.Helpers;
using Scripts.SongRequest.CSharp.Core.Models;

namespace Scripts.SongRequest.CSharp.Models.Requests
{
    public sealed record SongRequestDecision
    {
        public UserData UserData { get; init; }
        public UserIdOrName TargetUserIdOrName { get; init; }
        public SongRequestNumber RequestNumber { get; init; }
        public DateTime ProcessedTimeUtc { get; init; }
        public string Reason { get; init; }

        public string ProcessedTimeUtcAsString => ProcessedTimeUtc.ToLocalSimpleString();


        public SongRequestDecision(
            UserData userData,
            UserIdOrName targetUserIdOrName,
            SongRequestNumber requestNumber,
            DateTime processedTimeUtc,
            string reason)
        {
            if (processedTimeUtc.Kind != DateTimeKind.Utc)
            {
                var message = $"Invalid date time kind: {processedTimeUtc.Kind.ToString()}, expected: Utc.";
                throw new ArgumentException(message);
            }

            UserData = userData ?? throw new ArgumentNullException(nameof(userData));
            TargetUserIdOrName = targetUserIdOrName ?? throw new ArgumentNullException(nameof(targetUserIdOrName));
            RequestNumber = requestNumber ?? throw new ArgumentNullException(nameof(requestNumber));
            ProcessedTimeUtc = processedTimeUtc;
            Reason = reason ?? throw new ArgumentNullException(nameof(reason));
        }

        public static SongRequestDecision CreateWithUtcNow(
            UserData userData,
            UserIdOrName targetUserIdOrName,
            SongRequestNumber requestNumber,
            string reason)
        {
            return new SongRequestDecision(
                userData: userData,
                targetUserIdOrName: targetUserIdOrName,
                requestNumber: requestNumber,
                processedTimeUtc: DateTime.UtcNow,
                reason: reason
            );
        }
    }
}
