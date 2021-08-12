using System;

namespace Scripts.SongRequest.CSharp.Models.Requests
{
    public sealed record SongRequestNumber
    {
        public const string RawAllValue = "All";
        public const int AllValue = -1;

        public static SongRequestNumber All { get; } = new(AllValue);

        public int Value { get; init; }

        public bool IsAll => Value == AllValue;


        public SongRequestNumber(
            int value)
        {
            Value = value;
        }

        public static SongRequestNumber Parse(
            string rawValue)
        {
            return InternalParse(rawValue, defaultValue: null);
        }

        public static SongRequestNumber TryParse(
            string rawValue,
            SongRequestNumber defaultValue)
        {
            return InternalParse(rawValue, defaultValue);
        }

        private static SongRequestNumber InternalParse(
            string rawValue,
            SongRequestNumber? defaultValue)
        {
            if (StringComparer.OrdinalIgnoreCase.Equals(rawValue, RawAllValue))
            {
                return All;
            }

            if (!int.TryParse(rawValue, out int result))
            {
                if (defaultValue is not null)
                {
                    return defaultValue;
                }

                string message = $"Invalid request number: '{rawValue}'.";
                throw new ArgumentException(message, nameof(rawValue));
            }

            return new SongRequestNumber(result);
        }
    }
}
