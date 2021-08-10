using System;

namespace Scripts.SongRequest.CSharp.Core.Models
{
    public sealed record FileName
    {
        public string Value { get; init; }

        public bool HasValue => !string.IsNullOrWhiteSpace(Value);


        public FileName(
            string value)
        {
            Value = value ?? throw new ArgumentNullException(nameof(value));
        }
    }
}
