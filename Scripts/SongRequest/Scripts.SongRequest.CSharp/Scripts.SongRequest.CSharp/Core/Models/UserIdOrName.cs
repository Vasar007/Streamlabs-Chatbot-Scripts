using System;

namespace Scripts.SongRequest.CSharp.Core.Models
{
    public sealed record UserIdOrName
    {
        public string Value { get; init; }

        public bool HasValue => !string.IsNullOrWhiteSpace(Value);


        public UserIdOrName(
            string value)
        {
            Value = value ?? throw new ArgumentNullException(nameof(value));
        }

        public UserId AsId()
        {
            return new UserId(Value);
        }

        public UserName AsName()
        {
            return new UserName(Value);
        }
    }
}
