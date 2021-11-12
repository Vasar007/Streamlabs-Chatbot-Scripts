using System;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Runtime.InteropServices;
using WebDriverManager.Services;
using WebDriverManager.Services.Impl;

namespace Scripts.SongRequest.CSharp.Web.Drivers.Custom
{
    internal sealed class CustomBinaryService : IBinaryService
    {
        // Based on "WebDriverManager.Services.Impl.BinaryService" class.

        private sealed class ExposedBinaryService : BinaryService
        {
            public ExposedBinaryService()
            {
            }

            public string UnZip_Exposed(string path, string destination, string name)
            {
                return UnZip(path, destination, name);
            }

            public void UnZipTgz_Exposed(string gzArchiveName, string destination)
            {
                UnZipTgz(gzArchiveName, destination);
            }

            public void RemoveZip_Exposed(string path)
            {
                RemoveZip(path);
            }
        }

        private readonly ExposedBinaryService _internalService;

        public IWebProxy Proxy
        {
            get => _internalService.Proxy;
            set => _internalService.Proxy = value;
        }

        public CustomBinaryService()
        {
            _internalService = new ExposedBinaryService();
        }

        [Obsolete("binaryName parameter is redundant, use SetupBinary(url, zipDestination, binDestination)")]
        public string SetupBinary(string url, string zipDestination, string binDestination, string binaryName)
        {
            return SetupBinary(url, zipDestination, binDestination);
        }

        public string SetupBinary(string url, string zipPath, string binaryPath)
        {
            string directoryName = Path.GetDirectoryName(zipPath);
            string directoryName2 = Path.GetDirectoryName(binaryPath);
            string fileName = Path.GetFileName(binaryPath);

            Directory.CreateDirectory(directoryName);
            zipPath = DownloadZip(url, zipPath);
            string text = Path.Combine(directoryName, "staging");
            string text2 = Path.Combine(text, fileName);
            Directory.CreateDirectory(text);
            if (zipPath.EndsWith(".exe", StringComparison.OrdinalIgnoreCase))
            {
                File.Copy(zipPath, text2);
            }
            else if (zipPath.EndsWith(".zip", StringComparison.OrdinalIgnoreCase))
            {
                _internalService.UnZip_Exposed(zipPath, text2, fileName);
            }
            else if (zipPath.EndsWith(".tar.gz", StringComparison.OrdinalIgnoreCase))
            {
                _internalService.UnZipTgz_Exposed(zipPath, text2);
            }

            if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux) || RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
            {
                Process.Start("chmod", "+x " + text2)?.WaitForExit();
            }

            Directory.CreateDirectory(directoryName2);
            Exception? innerException = null;
            try
            {
                string[] files = Directory.GetFiles(text);
                string[] array = files;
                foreach (string text3 in array)
                {
                    string fileName2 = Path.GetFileName(text3);
                    string destFileName = Path.Combine(directoryName2, fileName2);
                    File.Copy(text3, destFileName, overwrite: true);
                }
            }
            catch (Exception ex)
            {
                innerException = ex;
            }

            try
            {
                if (Directory.Exists(text))
                {
                    Directory.Delete(text, recursive: true);
                }
            }
            catch (Exception ex2)
            {
                Console.Error.WriteLine(ex2.ToString());
            }

            try
            {
                _internalService.RemoveZip_Exposed(zipPath);
            }
            catch (Exception ex3)
            {
                Console.Error.WriteLine(ex3.ToString());
            }

            if (!Directory.Exists(directoryName2))
            {
                throw new Exception("Error writing " + directoryName2, innerException);
            }

            return binaryPath;
        }

        public string DownloadZip(string url, string destination)
        {
            if (File.Exists(destination))
            {
                return destination;
            }

            if (Proxy != null)
            {
                using var webClient = new WebClient
                {
                    Proxy = Proxy
                };
                webClient.DownloadFile(new Uri(url), destination);
            }
            else
            {
                using var webClient2 = new WebClient();
                webClient2.DownloadFile(new Uri(url), destination);
            }

            return destination;
        }
    }
}
