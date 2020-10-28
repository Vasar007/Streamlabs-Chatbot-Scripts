import os
import codecs
import json

import config
import helpers


class ScoreSettings(object):

    def __init__(self, Parent=None, settingsfile=None):
        if (settingsfile is None):
            self._set_default()
        else:
            try:
                if os.path.isfile(settingsfile):
                    with codecs.open(settingsfile, encoding="utf-8-sig",
                                     mode="r") as f:
                        self.__dict__ = json.load(f, encoding="utf-8")
                else:
                    self._set_default()
            except Exception as ex:
                if Parent is not None:
                    helpers.log(Parent, "Failed to load setting: " + str(ex))
                self._set_default()

    def Reload(self, jsondata):
        self.__dict__ = json.loads(jsondata, encoding="utf-8")

    def Save(self, settingsfile, Parent):
        try:
            helpers.save_json(self.__dict__, settingsfile)

            with codecs.open(settingsfile.replace("json", "js"),
                             encoding="utf-8-sig", mode="w+") as f:
                content = (
                    "var settings = {0};".format(
                        json.dumps(self.__dict__, encoding="utf-8")
                    )
                )
                f.write(content)
        except Exception as ex:
            helpers.log(Parent, "Failed to save settings to file: " + str(ex))

    def _set_default(self):
        self.CommandGetScore = config.CommandGetScore
        self.CommandNewScore = config.CommandNewScore
        self.CommandUpdateScore = config.CommandUpdateScore
        self.CommandResetScore = config.CommandResetScore
        self.CommandReloadScore = config.CommandReloadScore
        self.Permission = config.Permission
        self.PermissionInfo = config.PermissionInfo
