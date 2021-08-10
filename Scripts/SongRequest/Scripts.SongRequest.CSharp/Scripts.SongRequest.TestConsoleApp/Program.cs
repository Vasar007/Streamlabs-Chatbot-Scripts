using System;
using System.Collections.Generic;
using Acolyte.Common;
using Scripts.SongRequest.CSharp.Core.Models;
using Scripts.SongRequest.CSharp.Logging;
using Scripts.SongRequest.CSharp.Web;
using Scripts.SongRequest.TestConsoleApp.Logging;
using Scripts.SongRequest.TestConsoleApp.Mocks;

namespace Scripts.SongRequest.TestConsoleApp
{
    internal static class Program
    {
        private static readonly IScriptLogger Logger = new ConsoleLogger();

        private static int Main(string[] args)
        {
            try
            {
                Console.WriteLine("Console application started.");

                TestMethod(args);
                Console.WriteLine("All tests were performed.");

                return ExitCodes.Success;
            }
            catch (Exception ex)
            {
                string exceptionMessage = $"Exception occurred in {nameof(Main)} method. " +
                                          $"{Environment.NewLine}{ex}";
                Console.WriteLine(exceptionMessage);

                return ExitCodes.Fail;
            }
            finally
            {
                Console.WriteLine("Console application stopped.");
                Console.WriteLine("Press any key to close this window...");
                Console.ReadKey();
            }
        }

        private static void TestMethod(IReadOnlyList<string> args)
        {
            if (args.Count != 1)
            {
                string message = $"Invalid number of arguments: {args.Count.ToString()}.";
                throw new ArgumentException(message, nameof(args));
            }

            var httpLink = new HttpLink(args[0]);

            var settings = TestSettings.MockSettings(httpLink);
            using var scrapper = HttpWebScrapperFactory.Create(
                settings, Logger, TestConfig.BrowserDriverPath, TestConfig.SelectedBrowserDriver
            );

            scrapper.OpenUrl();
        }
    }
}
