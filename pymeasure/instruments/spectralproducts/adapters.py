#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2020 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from pymeasure.adapters import SerialAdapter


class SpectralProductsUSBAdapter(SerialAdapter):
    """ Provides a :class:`SerialAdapter` with the specific baudrate,
    timeout, parity, and byte size for Spectral Products USB communication.

    Initiates the adapter to open serial communcation over
    the supplied port.

    :param port: A string representing the serial port
    """

    def __init__(self, port):
        super(SpectralProductsUSBAdapter, self).__init__(
            port,
            baudrate=9600,
            timeout=15,
            parity='N',
            bytesize=7,
            stopbits=1,
            bytesize=8
        )

    def write(self, command):
        """ Overwrites the :func:`SerialAdapter.write <pymeasure.adapters.SerialAdapter.write>`
        method to automatically append a Unix-style linebreak at the end
        of the command.

        :param command: SCPI command string to be sent to the instrument
        """
        super(SpectralProductsUSBAdapter, self).write(command + "\n")
