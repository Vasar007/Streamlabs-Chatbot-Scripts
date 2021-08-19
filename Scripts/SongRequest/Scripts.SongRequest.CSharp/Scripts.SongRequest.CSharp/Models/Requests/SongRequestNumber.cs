using System;
using Scripts.SongRequest.CSharp.Models.Settings;

namespace Scripts.SongRequest.CSharp.Models.Requests
{
    public sealed record SongRequestNumber
    {
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
            string rawValue,
            ISongRequestScriptSettings settings)
        {
            return InternalParse(rawValue, defaultValue: null, settings);
        }

        public static SongRequestNumber TryParse(
            string rawValue,
            SongRequestNumber defaultValue,
            ISongRequestScriptSettings settings)
        {
            return InternalParse(rawValue, defaultValue, settings);
        }

        private static SongRequestNumber InternalParse(
            string rawValue,
            SongRequestNumber? defaultValue,
            ISongRequestScriptSettings settings)
        {
            if (StringComparer.OrdinalIgnoreCase.Equals(rawValue, settings.ParameterAll))
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
