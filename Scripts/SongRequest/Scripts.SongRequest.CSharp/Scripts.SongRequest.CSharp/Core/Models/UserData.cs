using System;

namespace Scripts.SongRequest.CSharp.Core.Models
{
    public sealed record UserData
    {
        public static UserData Empty { get; } = new(UserId.Empty, UserName.Empty);

        public UserId Id { get; init; }
        public UserName Name { get; init; }

        public bool HasId => Id.HasValue;
        public bool HasName => Name.HasValue;

        public bool HasValue => HasId || HasName;


        public UserData(
            UserId id,
            UserName name)
        {
            Id = id ?? throw new ArgumentNullException(nameof(id));
            Name = name ?? throw new ArgumentNullException(nameof(name));
        }

        public static UserData Create(
            string rawUserId,
            string rawUserName)
        {
            var userId = new UserId(rawUserId);
            var userName = new UserName(rawUserName);
            return new UserData(userId, userName);
        }

        public static implicit operator bool(UserData userData)
        {
            return userData.HasValue;
        }
    }
}
