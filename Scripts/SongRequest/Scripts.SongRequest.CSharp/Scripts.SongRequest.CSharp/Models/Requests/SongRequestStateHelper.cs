using System;
using System.Collections.Generic;
using System.Linq;

namespace Scripts.SongRequest.CSharp.Models.Requests
{
    public static class SongRequestStateHelper
    {
        public static IReadOnlyList<SongRequestState> GetAllValues()
        {
            return Enum.GetValues(typeof(SongRequestState))
                .Cast<SongRequestState>()
                .ToList()
                .AsReadOnly();
        }
    }
}
