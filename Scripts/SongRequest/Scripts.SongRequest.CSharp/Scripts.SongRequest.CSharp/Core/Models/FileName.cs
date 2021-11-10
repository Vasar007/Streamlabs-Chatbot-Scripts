using System;
using System.IO;
using System.Runtime.InteropServices;

namespace Scripts.SongRequest.CSharp.Core.Models
{
    public sealed record FileName
    {
        public string Value { get; init; }
        public string? Extension { get; init; }

        public bool HasValue => !string.IsNullOrWhiteSpace(Value);


        public FileName(
            string value,
            string? extension)
        {
            Value = value ?? throw new ArgumentNullException(nameof(value));
            Extension = extension;
        }

        /// <summary>
        ///  Returns the filename of the binary for the current platform.
        /// </summary>
        /// <returns>Binary filename.</returns>
        public string GetFullFilename()
        {
            bool shouldAddExtension =
                RuntimeInformation.IsOSPlatform(OSPlatform.Windows) &&
                !StringComparer.OrdinalIgnoreCase.Equals(Extension, Path.GetExtension(Value));

            return shouldAddExtension
                ? Value + Extension
                : Value;
        }
    }
}
