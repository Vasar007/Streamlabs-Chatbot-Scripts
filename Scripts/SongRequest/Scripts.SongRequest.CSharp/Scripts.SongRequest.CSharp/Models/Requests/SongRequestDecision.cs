using System;
using Scripts.SongRequest.CSharp.Core.Models;

namespace Scripts.SongRequest.CSharp.Models.Requests
{
    public sealed record SongRequestDecision
    {
        public UserData UserData { get; init; }
        public UserIdOrName TargetUserIdOrName { get; init; }
        public SongRequestNumber RequestNumber { get; init; }


        public SongRequestDecision(
            UserData userData,
            UserIdOrName targetUserIdOrName,
            SongRequestNumber requestNumber)
        {
            UserData = userData ?? throw new ArgumentNullException(nameof(userData));
            TargetUserIdOrName = targetUserIdOrName ?? throw new ArgumentNullException(nameof(targetUserIdOrName));
            RequestNumber = requestNumber ?? throw new ArgumentNullException(nameof(requestNumber));
        }
    }
}
