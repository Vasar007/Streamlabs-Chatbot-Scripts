using System;
using System.Diagnostics;
using System.IO;
using System.Text;

namespace Scripts.SongRequest.CSharp.Core.Processes
{
    public sealed class ProcessLaunchContext
    {
        public FileInfo? File { get; }

        public string? FileName { get; }

        public string? Args { get; }

        public bool ShowWindow { get; }

        public bool UseShellExecute { get; }


        public bool RedirectStandardOutput => !UseShellExecute;
        public Encoding? StandardOutputEncoding =>
             RedirectStandardOutput
             ? Encoding.UTF8
             : null;

        public bool RedirectStandardError => !UseShellExecute;
        public Encoding? StandardErrorEncoding =>
            RedirectStandardError
            ? Encoding.UTF8
            : null;


        private ProcessLaunchContext(
            FileInfo? file,
            string? fileName,
            string? args,
            bool showWindow,
            bool useShellExecute)
        {
            File = file;
            FileName = fileName;
            Args = args;
            ShowWindow = showWindow;
            UseShellExecute = useShellExecute;
        }

        public static ProcessLaunchContext Create(
            FileInfo file,
            string? args,
            bool showWindow,
            bool useShellExecute)
        {
            if (file is null)
            {
                throw new ArgumentNullException(nameof(file));
            }

            return new ProcessLaunchContext(
                file: file,
                fileName: null,
                args: args,
                showWindow: showWindow,
                useShellExecute: useShellExecute
            );
        }

        public static ProcessLaunchContext Create(
             string fileName,
             string? args,
             bool showWindow,
             bool useShellExecute)
        {
            if (fileName is null)
            {
                throw new ArgumentNullException(nameof(fileName));
            }

            return new ProcessLaunchContext(
                file: null,
                fileName: fileName,
                args: args,
                showWindow: showWindow,
                useShellExecute: useShellExecute
            );
        }

        public ProcessStartInfo CreateStartInfo()
        {
            if (File is null && string.IsNullOrEmpty(FileName))
            {
                throw new InvalidOperationException("Failed to get file name to start.");
            }

            string fileName = File is null ? FileName! : File.FullName;
            string workingDirectory = File is null ? string.Empty : File.Directory.FullName;

            var starterInfo = new ProcessStartInfo(fileName, Args)
            {
                WorkingDirectory = workingDirectory,
                UseShellExecute = UseShellExecute,
                RedirectStandardError = RedirectStandardError,
                StandardErrorEncoding = StandardErrorEncoding,
                RedirectStandardOutput = RedirectStandardOutput,
                StandardOutputEncoding = StandardOutputEncoding
            };

            if (ShowWindow)
            {
                starterInfo.WindowStyle = ProcessWindowStyle.Normal;
                starterInfo.CreateNoWindow = false;
                return starterInfo;
            }

            starterInfo.WindowStyle = ProcessWindowStyle.Hidden;
            starterInfo.CreateNoWindow = true;
            return starterInfo;
        }

        public string ToLogString()
        {
            var sb = new StringBuilder()
                .AppendLine($"[{nameof(ProcessLaunchContext)}]")
                .AppendLine($"File: '{File?.ToString() ?? "NULL"}'")
                .AppendLine($"FileName: '{FileName?.ToString() ?? "NULL"}'")
                .AppendLine($"Args: {Args ?? "NULL"}")
                .AppendLine($"ShowWindow: '{ShowWindow.ToString()}'")
                .AppendLine($"UseShellExecute: '{UseShellExecute.ToString()}'");

            return sb.ToString();
        }
    }
}
