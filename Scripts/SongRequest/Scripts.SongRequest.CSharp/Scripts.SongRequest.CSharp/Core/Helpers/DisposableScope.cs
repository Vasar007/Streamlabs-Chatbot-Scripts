using System;
using System.Collections.Generic;

namespace Scripts.SongRequest.CSharp.Core.Helpers
{
    // TODO: replace with version from Acolyte package.
    public sealed class DisposableScope : IDisposable
    {
        private readonly Stack<IDisposable> _disposables;


        public DisposableScope()
            : this(capacity: 4)
        {
        }

        public DisposableScope(
            int capacity)
        {
            _disposables = new Stack<IDisposable>(capacity);
        }

        public T Capture<T>(T disposable)
            where T : IDisposable
        {
            _disposables.Push(disposable);
            return disposable;
        }

        public void ReleaseAll()
        {
            _disposables.Clear();
        }

        #region IDisposable Implementation

        private bool _disposed;

        public void Dispose()
        {
            if (_disposed)
            {
                return;
            }

            foreach (IDisposable disposable in _disposables)
            {
                try
                {
                    disposable.Dispose();
                }
                catch (Exception)
                {
                    // Ignore.
                }
            }

            _disposed = true;
        }

        #endregion
    }
}
