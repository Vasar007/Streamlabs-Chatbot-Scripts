﻿using System;
using System.Collections.Generic;
using Acolyte.Common;
using Scripts.SongRequest.CSharp.Core.Models;
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
            using var scrapper = HttpWebScrapperFactory.Create(settings, Logger);

            scrapper.OpenUrl();

            var userId = new UserId("TestUserId");
            const int number = 1;

            var request = SongRequestModel.CreateNew(userId, TestConfig.SongLink, number);
            request = request.Approve();
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
    }
}
