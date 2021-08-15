using System;
using Scripts.SongRequest.CSharp.Models.Requests;

namespace Scripts.SongRequest.CSharp.Web.Scrapper
{
    public interface IHttpWebScrapper : IDisposable
    {
        void OpenUrl();
        void Refresh();
        SongRequestResult Process(SongRequestModel songRequest);
        SongRequestSkipResult Skip(bool shouldSkipAll);
    }
}
