using System;
using System.IO;
using System.Net;
using Scripts.SongRequest.CSharp.Core.Models;
using WebDriverManager.DriverConfigs;
using WebDriverManager.Helpers;
using WebDriverManager.Services;
using WebDriverManager.Services.Impl;

namespace Scripts.SongRequest.CSharp.Web.Drivers.Custom
{
    internal sealed class CustomDriverManager
    {
        // Based on "WebDriverManager.DriverManager" class.

        private static readonly object Object = new();

        private IBinaryService _binaryService;
        private readonly IVariableService _variableService;
        private readonly FilePath _driverPath;
        private readonly FileName _driverExecutableName;


        public CustomDriverManager(
            IBinaryService binaryService,
            IVariableService variableService,
            FilePath driverPath,
            FileName driverExecutableName)
        {
            _binaryService = binaryService ?? throw new ArgumentNullException(nameof(binaryService));
            _variableService = variableService ?? throw new ArgumentNullException(nameof(variableService));
            _driverPath = driverPath ?? throw new ArgumentNullException(nameof(driverPath));
            _driverExecutableName = driverExecutableName ?? throw new ArgumentNullException(nameof(driverExecutableName));
        }

        public static CustomDriverManager Create(
            FilePath driverPath,
            FileName driverExecutableName)
        {
            return new CustomDriverManager(
                binaryService: new CustomBinaryService(),
                variableService: new VariableService(),
                driverPath: driverPath,
                driverExecutableName: driverExecutableName
            );
        }

        public CustomDriverManager WithProxy(IWebProxy proxy)
        {
            _binaryService = new BinaryService
            {
                Proxy = proxy ?? throw new ArgumentNullException(nameof(proxy))
            };
            return this;
        }

        public string ConstructFullDriverPath()
        {
            return Path.Combine(
                _driverPath.Value, _driverExecutableName.GetFullFilename()
            );
        }

        public string SetUpDriver(string url, string binaryPath)
        {
            lock (Object)
            {
                return SetUpDriverImpl(url, binaryPath);
            }
        }

        public string SetUpDriver(
            IDriverConfig config,
            string version = VersionResolveStrategy.Latest,
            Architecture architecture = Architecture.Auto)
        {
            lock (Object)
            {
                architecture = architecture.Equals(Architecture.Auto)
                    ? ArchitectureHelper.GetArchitecture()
                    : architecture;
                version = GetVersionToDownload(config, version);

                string url = architecture.Equals(Architecture.X32)
                    ? config.GetUrl32()
                    : config.GetUrl64();
                url = UrlHelper.BuildUrl(url, version);

                string binDestination = ConstructFullDriverPath();

                return SetUpDriverImpl(url, binDestination);
            }
        }

        private string SetUpDriverImpl(string url, string binaryPath)
        {
            string zipDestination = FileHelper.GetZipDestination(url);
            binaryPath = _binaryService.SetupBinary(url, zipDestination, binaryPath);

            _variableService.SetupVariable(binaryPath);
            return binaryPath;
        }

        private static string GetVersionToDownload(IDriverConfig config, string version)
        {
            return version switch
            {
                VersionResolveStrategy.MatchingBrowser => config.GetMatchingBrowserVersion(),
                VersionResolveStrategy.Latest => config.GetLatestVersion(),

                _ => version
            };
        }
    }
}
