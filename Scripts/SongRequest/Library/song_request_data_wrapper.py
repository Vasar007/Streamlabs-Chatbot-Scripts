# -*- coding: utf-8 -*-


class SongRequestDataWrapper(object):
    r"""
    "Data" object wrapper.
    """

    def __init__(self, data):
        self.data = data

    @property
    def user_id(self):
        return self.data.User

    @property
    def user_name(self):
        return self.data.UserName

    @property
    def message(self):
        return self.data.Message

    @property
    def raw_data(self):
        return self.data.RawData

    @property
    def service_type(self):
        return self.data.ServiceType

    # Functions to retrive common info about message.

    def is_chat_message(self):
        r"""
        Checks if the incoming data is a chat message.

        bool IsChatMessage()
        """
        return self.data.IsChatMessage()

    def is_raw_data(self):
        r"""
        Checks if the incoming data is raw unparsed data.

        bool IsRawData()
        """
        return self.data.IsRawData()

    def is_from_twitch(self):
        r"""
        Checks if the message came from Twitch chat.

        bool IsFromTwitch()
        """
        return self.data.IsFromTwitch()

    def is_from_youtube(self):
        r"""
        Checks if the message came from Youtube chat.

        bool IsFromYoutube()
        """
        return self.data.IsFromYoutube()

    def is_from_mixer(self):
        r"""
        Checks if the message came from Mixer chat.

        bool IsFromMixer()
        """
        return self.data.IsFromMixer()

    def is_from_discord(self):
        r"""
        Checks if the message came from Discord.

        bool IsFromDiscord()
        """
        return self.data.IsFromDiscord()

    def is_whisper(self):
        r"""
        Checks if the message is a whisper/DM.

        bool IsWhisper()
        """
        return self.data.IsWhisper()

    # Functions to retrive parameters data from message.

    def get_param(self, id_):
        r"""
        Retrieves a parameter at the specified index.

        string GetParam(int id)
        """
        return self.data.GetParam(id_)

    def get_param_count(self):
        r"""
        Retrieves the total amount of parameters.

        int GetParamCount()
        """
        return self.data.GetParamCount()
