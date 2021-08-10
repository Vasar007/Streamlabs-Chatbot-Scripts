using System;

namespace Scripts.SongRequest.TestConsoleApp.Logging
{
    internal sealed class ConsoleColorScope : IDisposable
    {
        private readonly ConsoleColor _resetColor;

        public ConsoleColorScope(ConsoleColor consoleColor, ConsoleColor resetColor = ConsoleColor.White)
        {
            if (!Enum.IsDefined(typeof(ConsoleColor), consoleColor))
            {
                throw new ArgumentOutOfRangeException(nameof(consoleColor));
            }

            if (!Enum.IsDefined(typeof(ConsoleColor), resetColor))
            {
                throw new ArgumentOutOfRangeException(nameof(resetColor));
            }

            _resetColor = resetColor;
            Console.ForegroundColor = consoleColor;
        }

        #region IDisposable Members

        private bool _disposed;

        public void Dispose()
        {
            if (_disposed)
            {
                return;
            }

            Console.ForegroundColor = _resetColor;

            _disposed = true;
        }

        #endregion
    }
}
