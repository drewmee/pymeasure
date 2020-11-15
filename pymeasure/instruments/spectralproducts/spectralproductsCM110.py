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

from pymeasure.instruments import Instrument

from .adapters import SpectralProductsUSBAdapter


class SpectralProductsCM110(Instrument):
    """ Represents the Spectral Products CM110 Compact 1/8m Monochromator.
    To allow user access to the Spectral Products CM110 in Linux,
    create the file:
    :code:`/etc/udev/rules.d/52-spectralproductsCM110.rules`, with contents:

    .. code-block:: none

        SUBSYSTEM=="tty",ATTRS{idVendor}=="0403",ATTRS{idProduct}=="6001",SYMLINK+="spectralproductsCM110"

    Then reload the udev rules with:

    .. code-block:: bash

        sudo udevadm control --reload-rules
        sudo udevadm trigger

    The device will be accessible through :code:`/dev/spectralproductsCM110`.
    """
    def __init__(self, port):
        super(SpectralProductsCM110, self).__init__(
            SpectralProductsUSBAdapter(port),
            "Spectral Products CM110 Compact 1/8m Monochromator",
        )


