using System;

namespace Scripts.SongRequest.CSharp.Core.Helpers
{
    public static class DateTimeHelper
    {
        public static string ToSimpleString(this DateTime dateTime)
        {
            return dateTime.ToString("dd/MM/yyyy HH:mm:ss");
        }

        public static string ToLocalSimpleString(this DateTime dateTime)
        {
            return dateTime.ToLocalTime().ToSimpleString();
        }
    }
}
