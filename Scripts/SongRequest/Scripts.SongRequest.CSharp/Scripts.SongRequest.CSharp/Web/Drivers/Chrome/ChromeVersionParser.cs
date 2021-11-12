using System;
using System.Linq;

namespace Scripts.SongRequest.CSharp.Web.Drivers.Chrome
{
    public static class ChromeVersionParser
    {
        public static string ParseBrowserVersionFromRegistry(string rawValue)
        {
            return rawValue
               .Split(new[] { " " }, StringSplitOptions.RemoveEmptyEntries)
               .Last();
        }

        public static string ParseDriverVersion(string rawValue)
        {
            return rawValue
               .Split(new[] { " " }, StringSplitOptions.RemoveEmptyEntries)
               .ElementAt(1);
        }
    }
}
