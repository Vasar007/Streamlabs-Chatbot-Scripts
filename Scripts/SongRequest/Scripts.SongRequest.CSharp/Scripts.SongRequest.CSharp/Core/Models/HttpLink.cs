using System;

namespace Scripts.SongRequest.CSharp.Core.Models
{
    public sealed record HttpLink
    {
        public string Link { get; init; }


        public HttpLink(
            string link)
        {
            Link = link ?? throw new ArgumentNullException(nameof(link));
        }
    }
}
