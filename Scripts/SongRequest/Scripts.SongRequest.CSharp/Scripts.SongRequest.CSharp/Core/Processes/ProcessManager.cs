using System.IO;
using System.Threading.Tasks;

namespace Scripts.SongRequest.CSharp.Core.Processes
{
    public sealed class ProcessManager
    {
        public ProcessManager()
        {
        }

        private static ProcessLaunchContext CreateContextForOpenFile(FileInfo file)
        {
            return ProcessLaunchContext.Create(
                file: file,
                args: null,
                showWindow: true,
                useShellExecute: true
            );
        }

        public void OpenFileWithAssociatedApp(FileInfo file)
        {
            var launchContext = CreateContextForOpenFile(file);

            using var runner = ProgramRunner.RunProgram(launchContext);
            runner.Wait();
        }

        public async Task OpenFileWithAssociatedAppAsync(FileInfo file)
        {
            var launchContext = CreateContextForOpenFile(file);

            using var runner = ProgramRunner.RunProgram(launchContext);
            await runner.WaitAsync();
        }

        private static ProcessLaunchContext CreateContextForGetOutput(string fileName, string? args)
        {
            return ProcessLaunchContext.Create(
                fileName: fileName,
                args: args,
                showWindow: false,
                useShellExecute: false
            );
        }

        public string GetOutput(string fileName, string? args)
        {
            var launchContext = CreateContextForGetOutput(fileName, args);

            using var runner = ProgramRunner.RunProgram(launchContext);
            runner.Wait();

            return runner.GetAllOutput();
        }

        public async Task<string> GetOutputAsync(string fileName, string? args)
        {
            var launchContext = CreateContextForGetOutput(fileName, args);

            using var runner = ProgramRunner.RunProgram(launchContext);
            await runner.WaitAsync();

            return await runner.GetAllOutputAsync();
        }
    }
}
