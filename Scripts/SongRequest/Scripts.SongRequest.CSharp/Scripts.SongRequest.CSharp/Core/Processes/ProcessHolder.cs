using System;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;
using Scripts.SongRequest.CSharp.Core.Threading;

namespace Scripts.SongRequest.CSharp.Core.Processes
{
    public sealed class ProcessHolder : IDisposable
    {
        private readonly Process _process;

        private bool _disposed;


        private ProcessHolder(Process process)
        {
            _process = process ?? throw new ArgumentNullException(nameof(process));
        }

        public static ProcessHolder Start(ProcessLaunchContext launchContext)
        {
            if (launchContext is null)
            {
                throw new ArgumentNullException(nameof(launchContext));
            }

            return new ProcessHolder(StartProgram(launchContext));
        }

        #region IDisposable Implementation

        public void Dispose()
        {
            if (_disposed)
            {
                return;
            }

            // TODO: process should be killed if desktop application will be terminated.
            Kill();
            _process.Dispose();

            _disposed = true;
        }

        #endregion

        public void WaitForExit()
        {
            if (_process.HasExited)
            {
                return;
            }

            _process.WaitForExit();
        }

        public bool WaitForExit(TimeSpan delay)
        {
            if (_process.HasExited)
            {
                return true;
            }

            var miliseconds = (int) delay.TotalMilliseconds;
            return _process.WaitForExit(miliseconds);
        }

        public Task WaitForExitAsync()
        {
            if (_process.HasExited)
            {
                return Task.CompletedTask;
            }

            return _process.WaitForExitAsync();
        }

        public async Task<bool> WaitForExitAsync(TimeSpan delay)
        {
            if (_process.HasExited)
            {
                return true;
            }

            try
            {
                using var cts = new CancellationTokenSource(delay);
                Task waitingTask = _process.WaitForExitAsync(cts.Token);

                await waitingTask;
                return waitingTask.IsCompletedSuccessfully();
            }
            catch (TaskCanceledException)
            {
                return false;
            }
        }

        public void Kill()
        {
            if (_process.HasExited)
            {
                return;
            }

            _process.Kill();
        }

        public void CheckExecutionStatus()
        {
            if (!_process.StartInfo.RedirectStandardError)
            {
                return;
            }

            const int exitSuccess = (int) ExitCode.EXIT_SUCCESS;

            string error = _process.StandardError.ReadToEnd();
            if (_process.ExitCode != exitSuccess)
            {
                throw new ApplicationException($"Exception occured during process execution: {error}");
            }
        }

        public async Task CheckExecutionStatusAsync()
        {
            if (!_process.StartInfo.RedirectStandardError)
            {
                return;
            }

            const int exitSuccess = (int) ExitCode.EXIT_SUCCESS;

            string error = await _process.StandardError.ReadToEndAsync();
            if (_process.ExitCode != exitSuccess)
            {
                throw new ApplicationException($"Exception occured during process execution: {error}");
            }
        }

        public string GetAllOutput()
        {
            return _process.StandardOutput.ReadToEnd();
        }

        public Task<string> GetAllOutputAsync()
        {
            return _process.StandardOutput.ReadToEndAsync();
        }

        private static Process StartProgram(ProcessLaunchContext launchContext)
        {
            ProcessStartInfo starterInfo = launchContext.CreateStartInfo();

            return Process.Start(starterInfo);
        }
    }
}
