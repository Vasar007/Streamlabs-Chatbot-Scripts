using System;

namespace Scripts.SongRequest.CSharp.Core.Models
{
    public sealed record FilePath
    {
        public string Value { get; init; }

        public bool HasValue => !string.IsNullOrWhiteSpace(Value);


        public FilePath(
            string value)
        {
            Value = value ?? throw new ArgumentNullException(nameof(value));
        }
    }
}
