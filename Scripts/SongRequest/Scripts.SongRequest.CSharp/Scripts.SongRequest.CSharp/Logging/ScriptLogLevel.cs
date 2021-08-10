namespace Scripts.SongRequest.CSharp.Logging
{
    /// <summary>
    /// Logging levels for messages.
    /// </summary>
    /// <remarks>
    /// Values are set according to
    /// <see href="https://docs.python.org/3/library/logging.html#logging-levels" />
    /// </remarks>
    public enum ScriptLogLevel : int
    {
        NotSet = 0,
        Debug = 10,
        Info = 20,
        Warning = 30,
        Error = 40,
        Off = 50 // Allow to print only fatal messages.
    }
}
