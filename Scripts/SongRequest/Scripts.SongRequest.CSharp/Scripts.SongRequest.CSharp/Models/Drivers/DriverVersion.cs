using System;
using WebDriverManager.Helpers;

namespace Scripts.SongRequest.CSharp.Models.Drivers
{
    public sealed record DriverVersion
    {
        public static DriverVersion Auto = new("Auto");

        public static DriverVersion Latest = new(VersionResolveStrategy.Latest);

        public static DriverVersion MatchingBrowser = new(VersionResolveStrategy.MatchingBrowser);

        public string Value { get; init; }

        public bool HasValue => !string.IsNullOrWhiteSpace(Value);


        public DriverVersion(
            string value)
        {
            Value = value ?? throw new ArgumentNullException(nameof(value));
        }

        public string GetActualValueToUse(bool canAutoResolveVersion)
        {
            if (this != Auto)
            {
                return Value;
            }

            // If it is Auto version, we should convert it to one of the possible to use values.
            return canAutoResolveVersion
                ? MatchingBrowser.Value
                : Latest.Value;
        }
    }
}
