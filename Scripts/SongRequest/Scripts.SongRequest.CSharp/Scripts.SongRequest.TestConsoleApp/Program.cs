using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Acolyte.Common;
using Scripts.SongRequest.CSharp.Core.Models;
using Scripts.SongRequest.CSharp.Core.Processes;
using Scripts.SongRequest.CSharp.Logging;
using Scripts.SongRequest.CSharp.Models.Requests;
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
                }
                TestGetChromeVersionViaProcess();
                TestGetChromeDriverVersionViaProcess();

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
            string output = ProcessManager.GetOutput(fileName, args);

            Logger.Info($"Result of the output: {output}");

            string finalResult = output.Split(" ", StringSplitOptions.RemoveEmptyEntries).Last();
            Logger.Info($"Final result: {finalResult}");
        }

        private static void TestGetChromeDriverVersionViaProcess()
        {
            string fileName = "C:\\Program Files\\Common Files\\Webdrivers\\chromedriver.exe";
            string args = "-v";
            string output = ProcessManager.GetOutput(fileName, args);

            Logger.Info($"Result of the output: {output}");

            string finalResult = output.Split(" ", StringSplitOptions.RemoveEmptyEntries).ElementAt(1);
            Logger.Info($"Final result: {finalResult}");
        }
    }
}
