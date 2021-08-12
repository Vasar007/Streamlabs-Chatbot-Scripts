using System;
using System.Collections.Generic;
using System.Linq;

namespace Scripts.SongRequest.CSharp.Models.Settings
{
    public sealed record WebDriverType
    {
        public const string RawEdgeDriver = "Edge";
        public static WebDriverType EdgeDriver { get; } = new(RawEdgeDriver);

        public const string RawChromeDriver = "Chromium/Chrome";
        public static WebDriverType ChromeDriver { get; } = new(RawChromeDriver);

        public const string RawFirefoxDriver = "Firefox";
        public static WebDriverType FirefoxDriver { get; } = new(RawFirefoxDriver);

        public const string RawOperaDriver = "Opera";
        public static WebDriverType OperaDriver { get; } = new(RawOperaDriver);

        private static readonly IReadOnlyList<string> _validDriverTypes = new List<string>
        {
            RawEdgeDriver,
            RawChromeDriver,
            RawFirefoxDriver,
            RawOperaDriver
        }.AsReadOnly();

        public string Value { get; init; }


        private WebDriverType(
            string value)
        {
            Value = value ?? throw new ArgumentNullException(nameof(value));
        }

        public static WebDriverType Wrap(
            string rawValue)
        {
            if (!_validDriverTypes.Contains(rawValue, StringComparer.OrdinalIgnoreCase))
            {
                throw new ArgumentException($"Invalid driver type: '{rawValue}'.", nameof(rawValue));
            }

            return new WebDriverType(rawValue);
        }
    }
}
