using System;

namespace Scripts.SongRequest.CSharp.Logging
{
    public interface IScriptLogger
    {
        void Log(ScriptLogLevel logLevel, string message);
        void Debug(string message);
        void Info(string message);
        void Warning(string message);
        void Error(string message);
        void Critical(string message);
        void Exception(Exception ex, string? message);
    }
}
