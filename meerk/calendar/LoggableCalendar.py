# MIT License
#
# Copyright (c) 2018 Alexey Nikitin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from datetime import datetime
from typing import List

from .Calendar import Calendar


class LoggableCalendar(Calendar):

    def __init__(self, origin: Calendar) -> None:
        self.origin = origin
        self.__is_busy: List[bool] = []

    def is_busy(self, time: datetime) -> bool:
        is_busy = self.origin.is_busy(time)
        if not self.__is_busy:
            self.__is_busy = [not is_busy]
        if is_busy and not self.__is_busy[0]:
            print('Busy!')
        elif not is_busy and self.__is_busy[0]:
            print('Available')
        self.__is_busy = [is_busy]
        return is_busy

    def sync(self):
        print('Start calendar syncing...')
        self.origin.sync()
        print('Syncing successful finished!')
