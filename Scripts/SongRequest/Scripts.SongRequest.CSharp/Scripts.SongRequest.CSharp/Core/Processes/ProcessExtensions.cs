using System;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;

namespace Scripts.SongRequest.CSharp.Core.Processes
{
    public static class ProcessExtensions
    {
        public static TimeSpan DefaultDelay { get; } = TimeSpan.FromMilliseconds(100);


        public static async Task WaitForExitAsync(this Process process, TimeSpan delay,
            CancellationToken cancellationToken)
        {
            if (process is null)
            {
                throw new ArgumentNullException(nameof(process));
            }

            while (!process.HasExited)
            {
                await Task.Delay(delay, cancellationToken);
            }
        }

        public static Task WaitForExitAsync(this Process process, TimeSpan delay)
        {
            return process.WaitForExitAsync(delay, CancellationToken.None);
        }

        public static Task WaitForExitAsync(this Process process,
            CancellationToken cancellationToken)
        {
            return process.WaitForExitAsync(DefaultDelay, cancellationToken);
        }

        public static Task WaitForExitAsync(this Process process)
        {
            return process.WaitForExitAsync(DefaultDelay, CancellationToken.None);
        }
    }
}