using System;
using System.Threading.Tasks;

namespace Scripts.SongRequest.CSharp.Core.Threading
{
    public static class TaskExtensions
    {
        public static bool IsCompletedSuccessfully(this Task task)
        {
            if (task is null)
            {
                throw new ArgumentNullException(nameof(task));
            }

            return task.Status == TaskStatus.RanToCompletion &&
                   !task.IsFaulted &&
                   !task.IsCanceled;
        }
    }
}
