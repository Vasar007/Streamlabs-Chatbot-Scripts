namespace Acolyte.Common
{
    // TODO: replace with version from Acolyte package.
    public enum ExitCode
    {
        Success = 0,
        Fail = -1
    }

    public static class ExitCodes
    {
        public const int Success = (int) ExitCode.Success;
        public const int Fail = (int) ExitCode.Fail;
    }
}
