using System;
using Scripts.SongRequest.CSharp.Logging;

namespace Scripts.SongRequest.TestConsoleApp.Logging
{
    internal sealed class ConsoleLogger : IScriptLogger
    {
        public ConsoleLogger()
        {
        }

        public void Critical(string message)
        {
            using var colorScope = new ConsoleColorScope(ConsoleColor.DarkRed);

            Console.Error.WriteLine($"Critical: {message}");
        }

        public void Debug(string message)
        {
            using var colorScope = new ConsoleColorScope(ConsoleColor.Cyan);

            Console.Out.WriteLine($"Debug: {message}");
        }

        public void Error(string message)
        {
            using var colorScope = new ConsoleColorScope(ConsoleColor.Red);

            Console.Error.WriteLine($"Error: {message}");
        }

        public void Exception(Exception ex, string? message)
        {
            using var colorScope = new ConsoleColorScope(ConsoleColor.Red);

            if (message is null)
            {
                Console.Error.WriteLine($"Exception: {ex.Message}{Environment.NewLine}{ex}");
            }
            else
            {
                Console.Error.WriteLine($"Exception: {message}{Environment.NewLine}{ex}");
            }
        }

        public void Info(string message)
        {
            using var colorScope = new ConsoleColorScope(ConsoleColor.Green);

            Console.Out.WriteLine($"Info: {message}");
        }

        public void Log(ScriptLogLevel logLevel, string message)
        {
            switch (logLevel)
            {
                case ScriptLogLevel.NotSet:
                    throw new ArgumentException("Log level is not set.", nameof(logLevel));

                case ScriptLogLevel.Debug:
                    Debug(message);
                    break;

                case ScriptLogLevel.Info:
                    Info(message);
                    break;

                case ScriptLogLevel.Warning:
                    Warning(message);
                    break;

                case ScriptLogLevel.Error:
                    Error(message);
                    break;

                case ScriptLogLevel.Off:
                    break;

                default:
                    throw new ArgumentOutOfRangeException(
                        nameof(logLevel), logLevel, $"Unexpected log level: '{logLevel.ToString()}'."
                    );
            }
        }

        public void Warning(string message)
        {
            using var colorScope = new ConsoleColorScope(ConsoleColor.Yellow);

            Console.Out.WriteLine($"Warning: {message}");
        }
    }
}
