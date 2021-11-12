using System;
using System.Collections.Generic;
using System.IO;
using Acolyte.Common;
using Scripts.SongRequest.CSharp.Core.Models;
using Scripts.SongRequest.CSharp.Core.Processes;
using Scripts.SongRequest.CSharp.Logging;
using Scripts.SongRequest.CSharp.Models.Requests;
using Scripts.SongRequest.CSharp.Web.Drivers;
using Scripts.SongRequest.CSharp.Web.Drivers.Chrome;
using Scripts.SongRequest.CSharp.Web.Scrapper;
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
                ConsoleHelper.SetupUnicodeEncoding();
                Console.WriteLine("Console application started.");

                if (args.Length == 1)
                {
                    TestAddSongRequest(args);
                    TestSkipSongRequest(args);
                    TestGetChromeVersionViaProcess();
                    TestGetChromeDriverVersionViaProcess();
                }
                TestGetBrowserDriverUsingProvider();

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

        private static void TestAddSongRequest(IReadOnlyList<string> args)
        {
            var httpLink = ParseIntputLink(args);

            var settings = TestSettings.MockSettings(httpLink);
            using var scrapper = HttpWebScrapperFactory.Create(settings, Logger);

            scrapper.OpenUrl();

            var userData = UserData.Create("TestUserId", "TestUserName");
            var number = SongRequestNumber.All;

            var request = SongRequestModel.CreateNew(userData, TestConfig.SongLink, number);
            request = request.AutoApprove(settings.AutoApproveReason);
            request = request.StartProcessing();
            var result = scrapper.Process(request);

            if (result.IsSuccess)
            {
                Logger.Info("Song request processed successfully!");
            }
            else
            {
                Logger.Error($"Failed to process song request: {result.Description}");
            }
        }

        private static void TestSkipSongRequest(IReadOnlyList<string> args)
        {
            HttpLink httpLink = ParseIntputLink(args);

            var settings = TestSettings.MockSettings(httpLink);
            using var scrapper = HttpWebScrapperFactory.Create(settings, Logger);

            scrapper.OpenUrl();

            var result = scrapper.Skip(shouldSkipAll: true);

            if (result.IsSuccess)
            {
                Logger.Info("Song requests were skipped successfully!");
            }
            else
            {
                Logger.Error($"Failed to skip song requests: {result.Description}");
            }
        }

        private static HttpLink ParseIntputLink(IReadOnlyList<string> args)
        {
            if (args.Count != 1)
            {
                string message = $"Invalid number of arguments: {args.Count.ToString()}.";
                throw new ArgumentException(message, nameof(args));
            }

            var httpLink = new HttpLink(args[0]);
            return httpLink;
        }

        private static void TestGetChromeVersionViaProcess()
        {
            string fileName = "reg.exe";
            string args = "query HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon /v version";

            var manager = new ProcessManager();
            string output = manager.GetOutput(fileName, args);

            Logger.Info($"Result of the output: {output}");

            string finalResult = ChromeVersionParser.ParseBrowserVersionFromRegistry(output);
            Logger.Info($"Final result: {finalResult}");
        }

        private static void TestGetChromeDriverVersionViaProcess()
        {
            string fileName = Path.Combine(
                TestConfig.BrowserDriverPath.Value,
                TestConfig.BrowserDriverExecutableName.GetFullFilename()
            );
            string args = "-v";

            var manager = new ProcessManager();
            string output = manager.GetOutput(fileName, args);

            Logger.Info($"Result of the output: {output}");

            string finalResult = ChromeVersionParser.ParseDriverVersion(output);
            Logger.Info($"Final result: {finalResult}");
        }

        private static void TestGetBrowserDriverUsingProvider()
        {
            var httpLink = new HttpLink("https://www.google.com/");

            var settings = TestSettings.MockSettings(httpLink);

            var driverProvider = DriverProviderFactory.Create(settings, Logger);
            string binaryPath = driverProvider.ProvideBrowserDriver();

            Logger.Info($"Result: {binaryPath}");
        }
    }
}
