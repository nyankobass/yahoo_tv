"""
program_data.api
~~~~~~~~~~~~
:copyright: (c) 2018 by nyankobass.
:license: MIT, see LICENSE for more details.
"""


class ProgramData:
    def __init__(self, time: str, title: str, ch_num: int):
        self.time = time
        self.title = title
        self.ch_num = ch_num

    def __str__(self):
        return (self.time + " : " + self.title + " : " + str(self.ch_num))
