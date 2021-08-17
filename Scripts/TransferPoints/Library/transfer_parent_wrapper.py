# -*- coding: utf-8 -*-


class TransferParentWrapper(object):
    r"""
    "Parent" object wrapper.
    """

    def __init__(self, Parent):
        self._Parent = Parent

    # Messages And Events.

    def send_stream_message(self, message):
        r"""
        Sends message to the stream chat.

        void SendStreamMessage(string message)
        """
        self._Parent.SendStreamMessage(message)

    def send_stream_whisper(self, target_id, message):
        r"""
        Sends whisper message to the stream chat (only applicable on Twitch).

        void SendStreamWhisper(string target, string message)
        """
        self._Parent.SendStreamWhisper(target_id, message)

    def send_twitch_message(self, message):
        r"""
        Sends message to the Twitch chat (only if the user has set up
        the bot for Twitch).

        void SendTwitchMessage(string message)
        """
        self._Parent.SendTwitchMessage(message)

    def send_twitch_whisper(self, target_id, message):
        r"""
        Sends whisper message to the Twitch chat (only if the user has set up
        the bot for Twitch).

        void SendTwitchWhisper(string target, string message)
        """
        self._Parent.SendTwitchWhisper(target_id, message)

    def send_discord_message(self, message):
        r"""
        Sends message to Discord (only if the user has set up the bot for
        Discord).

        void SendDiscordMessage(string message)
        """
        self._Parent.SendDiscordMessage(message)

    def send_discord_dm(self, target_id, message):
        r"""
        Sends DMs to users on Discord.

        void SendDiscordDM(string target, string message)
        """
        self._Parent.SendDiscordDM(target_id, message)

    def broadcast_ws_event(self, event_name, json_data):
        r"""
        Sends an event to connected overlays.

        void BroadcastWsEvent(string eventName, string jsonData)
        """
        self._Parent.BroadcastWsEvent(event_name, json_data)

    # Currency Manipulation.

    def add_points(self, user_id, amount):
        r"""
        Adds currency to a single user.

        bool AddPoints(string userid, long amount)
        """
        return self._Parent.AddPoints(user_id, amount)

    def remove_points(self, user_id, amount):
        r"""
        Removes currency from a single user.

        bool RemovePoints(string userid, long amount)
        """
        return self._Parent.RemovePoints(user_id, amount)

    def add_points_with_name(self, user_id, user_name, amount):
        r"""
        Adds currency to a single user.

        bool AddPoints(string userid, string username, long amount)
        """
        return self._Parent.AddPoints(user_id, user_name, amount)

    def remove_points_with_name(self, user_id, user_name, amount):
        r"""
        Removes currency from a single user.

        bool RemovePoints(string userid, string username, long amount)
        """
        return self._Parent.RemovePoints(user_id, user_name, amount)

    def add_points_all(self, data):
        r"""
        Synchronously adds currency to the several users.

        Returns a list of user IDs that could not receive currency because they
        were not in chat.

        List\<string userid> AddPointsAll(PythonDictionary<string userid, long amount> data)
        """
        return self._Parent.AddPointsAll(data)

    def add_points_all_async(self, data, callback):
        r"""
        Asynchronously adds currency to the several users.

        Callback will receive a list of user IDs that could not receive currency
        because they were not in chat. The same value will be return from
        function.

        List\<string userid> AddPointsAllAsync(PythonDictionary<string userid, long amount> data, Action<List\<string userid>> callback)
        """
        return self._Parent.AddPointsAllAsync(data, callback)

    def remove_points_all(self, data):
        r"""
        Synchronously removes currency from the several users.

        Returns a list of user IDs that could not lose currency because they were
        not in chat.

        List\<string userid> RemovePointsAll(PythonDictionary<string userid, long amount> data)
        """
        return self._Parent.RemovePointsAll(data)

    def remove_points_all_async(self, data, callback):
        r"""
        Asynchronously removes currency to the several users.

        Callback will receive a list of user IDs that could not lose currency
        because they were not in chat. The same value will be return from
        function.

        List\<string userid> RemovePointsAllAsync(PythonDictionary<string userid, long amount> data, Action<List\<string userid>> callback)
        """
        return self._Parent.RemovePointsAllAsync(data, callback)

    def get_points(self, user_id):
        r"""
        Retrieves single user's currency.

        long GetPoints(string userid)
        """
        return self._Parent.GetPoints(user_id)

    def get_hours(self, user_id):
        r"""
        Retrieves single user's hours watched.

        long GetHours(string userid)
        """
        return self._Parent.GetHours(user_id)

    def get_rank(self, user_id):
        r"""
        Retrieves single user's rank.

        string GetRank(string userid)
        """
        return self._Parent.GetRank(user_id)

    def get_top_currency(self, top):
        r"""
        Retrieves Top-X users based on currency.

        PythonDictionary<string userid, long amount> GetTopCurrency(int top)
        """
        return self._Parent.GetTopCurrency(top)

    def get_top_hours(self, top):
        r"""
        Retrieves Top-X Users based on hours watched.

        PythonDictionary<string userid, long amount> GetTopHours(int top)
        """
        return self._Parent.GetTopHours(top)

    def get_points_all(self, user_ids):
        r"""
        Retrieves several user's points.

        Note: "user_ids" should be .NET "System.Collections.Generic.List"
        collection.

        PythonDictionary<string userid, long amount> GetPointsAll(List\<string> userids)
        """
        return self._Parent.GetPointsAll(user_ids)

    def get_ranks_all(self, user_ids):
        r"""
        Retrieves several user's ranks.

        Note: "user_ids" should be .NET "System.Collections.Generic.List"
        collection.

        PythonDictionary<string userid, long amount> GetRanksAll(List\<string> userids)
        """
        return self._Parent.GetRanksAll(user_ids)

    def get_hours_all(self, user_ids):
        r"""
        Retrieves several user's hours.

        Note: "user_ids" should be .NET "System.Collections.Generic.List"
        collection.

        PythonDictionary<string userid, long amount> GetHoursAll(List\<string> userids)
        """
        return self._Parent.GetHoursAll(user_ids)

    def get_currency_users(self, user_ids):
        r"""
        Retrieves several user's currency information.

        Note: "user_ids" should be .NET "System.Collections.Generic.List"
        collection.

        List\<Currency> GetCurrencyUsers(List\<string> userids)

        Currency Object:

        | Variable                      | Usage           |
        | ----------------------------- | --------------- |
        | string UserId                 | obj.UserId      |
        | string UserName               | obj.UserName    |
        | long Points                   | obj.Points      |
        | long TimeWatched (In Minutes) | obj.TimeWatched |
        | string Rank                   | obj.Rank        |
        """
        return self._Parent.GetCurrencyUsers(user_ids)

    # Permissions.

    def has_permission(self, user_id, permission, info):
        r"""
        Checks permissions.

        bool HasPermission(string userid, string permission, string info)
        """
        return self._Parent.HasPermission(user_id, permission, info)

    # Viewers.

    def get_viewer_list(self):
        r"""
        Retrieves the viewerlist.

        List\<string userid> GetViewerList()
        """
        return self._Parent.GetViewerList()

    def get_active_users(self):
        r"""
        Retrieves all active users.

        List\<string userid> GetActiveUsers()
        """
        return self._Parent.GetActiveUsers()

    def get_random_active_user(self):
        r"""
        Retrieves a single random active user.

        string GetRandomActiveUser()
        """
        return self._Parent.GetRandomActiveUser()

    def get_display_name(self, user_id):
        r"""
        Retrieves a single user display name.

        string GetDisplayName(string userId)
        """
        return self._Parent.GetDisplayName(user_id)

    def get_display_names(self, user_ids):
        r"""
        Retrieves the several user display names.

        Note: "user_ids" should be .NET "System.Collections.Generic.List"
        collection.

        PythonDictionary<string userid, string username> GetDisplayNames(List\<string> userIds)
        """
        return self._Parent.GetDisplayNames(user_ids)

    # Cooldown Management.

    def add_cooldown(self, script_name, command, seconds):
        r"""
        Adds a command to the cooldown manager.

        void AddCooldown(string scriptName, string command, int seconds)
        """
        self._Parent.AddCooldown(script_name, command, seconds)

    def is_on_cooldown(self, script_name, command):
        r"""
        Checks if the command is on cooldown.

        bool IsOnCooldown(string scriptName, string command)
        """
        return self._Parent.IsOnCooldown(script_name, command)

    def get_cooldown_duration(self, script_name, command):
        r"""
        Retrieves the remaining cooldown duration.

        int GetCooldownDuration(string scriptName, string command)
        """
        return self._Parent.GetCooldownDuration(script_name, command)

    def add_user_cooldown(self, script_name, command, user_id, seconds):
        r"""
        Adds a user cooldown to a command.

        void AddUserCooldown(string scriptName, string command, string userid, int seconds)
        """
        self._Parent.AddUserCooldown(script_name, command, user_id, seconds)

    def is_on_user_cooldown(self, script_name, command, user_id):
        r"""
        Checks if a command is on user cooldown.

        bool IsOnUserCooldown(string scriptName, string command, string userid)
        """
        return self._Parent.IsOnUserCooldown(script_name, command, user_id)

    def get_user_cooldown_duration(self, script_name, command, user_id):
        r"""
        Retrieves the remaining user cooldown duration.

        bool GetUserCooldownDuration(string scriptName, string command, string userid)
        """
        return self._Parent.GetUserCooldownDuration(script_name, command, user_id)

    # OBS Management.

    def set_obs_current_scene(self, scene_name, callback=None):
        r"""
        Changes scene on OBS.

        Callback will receive the JSON string that OBS returns.

        void SetOBSCurrentScene(string sceneName, Action\<string> callback = null)
        """
        self._Parent.SetOBSCurrentScene(scene_name, callback)

    def set_obs_source_render(self, source, render, scene_name=None, callback=None):
        r"""
        Shows/Hides a source in OBS.

        Callback will receive the JSON string that OBS returns.

        void SetOBSSourceRender(string source, bool render, string sceneName = null, Action\<string> callback = null)
        """
        self._Parent.SetOBSSourceRender(source, render, scene_name, callback)

    def stop_obs_streaming(self, callback=None):
        r"""
        Stops the stream.

        Callback will receive the JSON string that OBS returns.

        void StopOBSStreaming(Action\<string> callback = null)
        """
        self._Parent.StopOBSStreaming(callback)

    def get_obs_special_sources(self, callback=None):
        r"""
        Retrieves all audio sources.

        Callback will receive the JSON string that OBS returns.

        void GetOBSSpecialSources(Action\<string> callback)
        """
        self._Parent.GetOBSSpecialSources(callback)

    def get_obs_volume(self, source, callback=None):
        r"""
        Retrieves the volume of an OBS source.

        Callback will receive the JSON string that OBS returns.

        void GetOBSVolume(string source, Action\<string> callback = null)
        """
        self._Parent.GetOBSVolume(source, callback)

    def set_obs_volume(self, source, volume, callback=None):
        r"""
        Controls the volume of an OBS source.

        Callback will receive the JSON string that OBS returns.

        void SetOBSVolume(string source, double volume, Action\<string> callback = null)
        """
        self._Parent.SetOBSVolume(source, volume, callback)

    def get_obs_mute(self, source, callback=None):
        r"""
        Mutes a specific source in OBS.

        Callback will receive the JSON string that OBS returns.

        void GetOBSMute(string source, Action\<string> callback)
        """
        self._Parent.GetOBSMute(source, callback)

    def set_obs_mute(self, source, mute, callback=None):
        r"""
        Toggles the mute state of a specific OBS source.

        Callback will receive the JSON string that OBS returns.

        void SetOBSMute(string source, bool mute, Action\<string> callback = null)
        """
        self._Parent.SetOBSMute(source, mute, callback)

    def toggle_obs_mute(self, source, callback=None):
        r"""
        Toggles mute of a specific OBS source.

        Callback will receive the JSON string that OBS returns.

        void ToggleOBSMute(string source, Action\<string> callback = null)
        """
        self._Parent.ToggleOBSMute(source, callback)

    # API Requests.

    def get_request(self, url, headers):
        r"""
        Sends HTTP GET request.

        string GetRequest(string url, PythonDictionary headers)
        """
        return self._Parent.GetRequest(url, headers)

    def post_request(self, url, headers, content, isJsonContent=True):
        r"""
        Sends HTTP POST request.

        string PostRequest(string url, PythonDictionary headers, PythonDictionary content, bool isJsonContent = true)
        """
        return self._Parent.PostRequest(url, headers, content, isJsonContent)

    def delete_request(self, url, headers):
        r"""
        Sends HTTP DELETE request.

        string DeleteRequest(string url, PythonDictionary headers)
        """
        return self._Parent.DeleteRequest(url, headers)

    def put_request(self, url, headers, content, isJsonContent=True):
        r"""
        Sends HTTP PUT request.

        string PutRequest(string url, PythonDictionary headers, PythonDictionary content, bool isJsonContent = true)
        """
        return self._Parent.PutRequest(url, headers, content, isJsonContent)

    # Stream Information.

    def is_live(self):
        r"""
        Checks if the stream is live.

        bool IsLive()
        """
        return self._Parent.IsLive()

    # GameWisp Information.

    def get_gw_tier_level(self, user_id):
        r"""
        Retrieves a user's GameWisp Sub Tier.

        int GetGwTierLevel(string user)
        """
        return self._Parent.GetGwTierLevel(user_id)

    # Miscellaneous.

    def get_random(self, min_, max_):
        r"""
        Gets a random number.

        int GetRandom(int min, int max)
        """
        return self._Parent.GetRandom(min_, max_)

    def get_streaming_service(self):
        r"""
        Retrieves the streaming platform that the Chatbot is being used on.

        string GetStreamingService()
        """
        return self._Parent.GetStreamingService()

    def get_channel_name(self):
        r"""
        Gets the stream's channel name (only applicable to Twitch).

        string GetChannelName()
        """
        return self._Parent.GetChannelName()

    def get_currency_name(self):
        r"""
        Retrieves the stream's currency name.

        string GetCurrencyName()
        """
        return self._Parent.GetCurrencyName()

    def log(self, script_name, message):
        r"""
        Logs information to the Bot's Log Window.

        void Log(string scriptName, string message)
        """
        self._Parent.Log(script_name, message)

    def play_sound(self, file_path, volume):
        r"""
        Attempts to play a sound if possible.

        bool PlaySound(string filePath, float volume)
        """
        return self._Parent.PlaySound(file_path, volume)

    def get_queue(self, max_):
        r"""
        Retrieves X amount of users that are in the queue at the moment.

        PythonDictionary<int position, string userid> GetQueue(int max)
        """
        return self._Parent.GetQueue(max_)

    # Song Queue Playlist Information.

    def get_song_queue(self, max_):
        r"""
        Retrieves the next X amount of songs in the queue.

        List\<Song> GetSongQueue(int max)

        Song Object:

        | Variable               | Usage               |
        | ---------------------- |-------------------- |
        | string Title           | obj.Title           |
        | string RequestedBy     | obj.RequestedBy     |
        | string RequestedByName | obj.RequestedByName |
        | string ID              | obj.ID              |
        | string URL             | obj.URL             |
        """
        return self._Parent.GetSongQueue(max_)

    def get_song_playlist(self, max_):
        r"""
        Retrieves the next X amount of songs in the playlist.

        List\<Song> GetSongPlaylist(int max)

        Song Object:

        | Variable               | Usage               |
        | ---------------------- |-------------------- |
        | string Title           | obj.Title           |
        | string RequestedBy     | obj.RequestedBy     |
        | string RequestedByName | obj.RequestedByName |
        | string ID              | obj.ID              |
        | string URL             | obj.URL             |
        """
        return self._Parent.GetSongPlaylist(max_)

    def get_now_playing(self):
        r"""
        Gets the current song that's playing.

        KeyValuePair<string title, string requestedBy> GetNowPlaying()
        """
        return self._Parent.GetNowPlaying()
