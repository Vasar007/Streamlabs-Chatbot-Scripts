using System;
using System.Threading.Tasks;

namespace Scripts.SongRequest.CSharp.Core.Processes
{
    public sealed class ProgramRunner : IDisposable
    {
        private readonly ProcessHolder _processHolder;

        private bool _disposed;


        public ProgramRunner(ProcessHolder processHolder)
        {
            _processHolder = processHolder ?? throw new ArgumentNullException(nameof(processHolder));
        }

        public static ProgramRunner RunProgram(ProcessLaunchContext launchContext)
        {
            var processHolder = ProcessHolder.Start(launchContext);

            return new ProgramRunner(processHolder);
        }

        public void Wait()
        {
            _processHolder.CheckExecutionStatus();
            _processHolder.WaitForExit();
        }

        public void Wait(TimeSpan delay)
        {
            _processHolder.CheckExecutionStatus();
            _processHolder.WaitForExit(delay);
        }

        public async Task WaitAsync()
        {
            await _processHolder.CheckExecutionStatusAsync();
            await _processHolder.WaitForExitAsync();
        }

        public async Task WaitAsync(TimeSpan delay)
        {
            await _processHolder.CheckExecutionStatusAsync();
            await _processHolder.WaitForExitAsync(delay);
        }

        public string GetAllOutput()
        {
            _processHolder.CheckExecutionStatus();
            return _processHolder.GetAllOutput();
        }

        public async Task<string> GetAllOutputAsync()
        {
            await _processHolder.CheckExecutionStatusAsync();
            return await _processHolder.GetAllOutputAsync();
        }

        #region IDisposable Impelementation

        public void Dispose()
        {
            if (_disposed)
            {
                return;
            }

            _processHolder.Dispose();

            _disposed = true;
        }

        #endregion
    }
}
