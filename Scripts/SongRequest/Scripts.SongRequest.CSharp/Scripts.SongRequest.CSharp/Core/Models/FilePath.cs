using System;

namespace Scripts.SongRequest.CSharp.Core.Models
{
    public sealed record FilePath
    {
        public static string AutoDetectPath { get; } = "Auto";

        public string Value { get; init; }

        public bool HasValue => !string.IsNullOrWhiteSpace(Value);


        public FilePath(
            string value)
        {
            Value = value ?? throw new ArgumentNullException(nameof(value));
        }

        public bool IsAutoDetect()
        {
            return StringComparer.OrdinalIgnoreCase.Equals(Value, AutoDetectPath);
        }
    }
}
