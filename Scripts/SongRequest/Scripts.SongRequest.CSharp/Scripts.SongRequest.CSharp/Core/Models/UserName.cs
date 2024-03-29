﻿using System;

namespace Scripts.SongRequest.CSharp.Core.Models
{
    public sealed record UserName
    {
        public static UserName Empty { get; } = new(string.Empty);

        public string Value { get; init; }

        public bool HasValue => !string.IsNullOrWhiteSpace(Value);


        public UserName(
            string value)
        {
            Value = value ?? throw new ArgumentNullException(nameof(value));
        }
    }
}
