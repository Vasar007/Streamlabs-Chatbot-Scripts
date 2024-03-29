﻿using System;

namespace Scripts.SongRequest.CSharp.Core.Models
{
    public sealed record HttpLink
    {
        public string Value { get; init; }

        public bool HasValue => !string.IsNullOrWhiteSpace(Value);


        public HttpLink(
            string value)
        {
            Value = value ?? throw new ArgumentNullException(nameof(value));
        }
    }
}
