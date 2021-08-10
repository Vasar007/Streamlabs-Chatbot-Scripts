using System;
using System.Text;

namespace Acolyte.Common
{
    // TODO: replace with version from Acolyte package.
    public static class ConsoleHelper
    {
        public static void SetupUnicodeEncoding()
        {
            // Setup encoding.
            Console.InputEncoding = Encoding.Unicode;
            Console.OutputEncoding = Encoding.Unicode;
        }
    }
}
