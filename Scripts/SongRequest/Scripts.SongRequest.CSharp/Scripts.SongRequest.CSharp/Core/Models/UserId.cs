using System;

namespace Scripts.SongRequest.CSharp.Core.Models
{
    public sealed record UserId
    {
        public static UserId Empty { get; } = new(string.Empty);

        public string Value { get; init; }

        public bool HasValue => !string.IsNullOrWhiteSpace(Value);


        public UserId(
            string value)
        {
            Value = value ?? throw new ArgumentNullException(nameof(value));
        }
    }
}
