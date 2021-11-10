# -*- coding: utf-8 -*-


class SongRequestProcessRunner(object):
    r"""
    Wrapper for C# process runner.
    """

    def __init__(self, real_process_runner):
        self._real_process_runner= real_process_runner

    def get_output(self, filename, args=None):
        return self._real_process_runner.GetOutput(filename, args)
