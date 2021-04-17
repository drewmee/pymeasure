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

import ast
import binascii
import struct

from pymeasure.instruments import Instrument

from .adapters import SpectralProductsUSBAdapter


# Grating installed:
# AG2400-00240-303
# Should have:
# AG1200-00400-303
class SpectralProductsCM110(Instrument):
    """Represents the Spectral Products CM110 Compact 1/8m Monochromator.
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

    @staticmethod
    def _process_query_response(r):
        if isinstance(r, str):
            r = ast.literal_eval(r)

        response_bytearray = [i for i in bytearray(r)]
        print(response_bytearray)
        high_byte = binascii.hexlify(struct.pack("B", response_bytearray[0]))
        low_byte = binascii.hexlify(struct.pack("B", response_bytearray[1]))
        status_byte = response_bytearray[-2]
        end_byte = response_bytearray[-1]

        if status_byte >= 128:
            raise Exception("Incorrect status byte received.")
        if end_byte != 24:
            raise Exception("Incorrect end byte received.")

        # decoded_msg = int((high_byte + low_byte).decode("ascii"), 16)
        decoded_msg = int((high_byte + low_byte), 16)
        return decoded_msg

    def _process_wavelength_encoding(wl):
        return tuple(i for i in bytearray(struct.pack(">H", wl)))

    echo = Instrument.measurement(
        "27",
        """ The ECHO command is used to verify communications with the CM110/112. """,
        get_process=lambda x: int(binascii.hexlify(ast.literal_eval(x)), 16),
    )

    serial_number = Instrument.measurement(
        "56\t19",
        """ Get the serial number of the CM110/112. """,
        get_process=lambda x: SpectralProductsCM110._process_query_response(x),
    )

    wavelength = Instrument.control(
        "56\t0",
        "16\t%s\t%s",
        """ Controls the wavelength setting. """,
        get_process=lambda x: SpectralProductsCM110._process_query_response(x),
        set_process=lambda x: SpectralProductsCM110._process_wavelength_encoding(x),
        check_set_errors=True,
    )

    wavelength_units = Instrument.measurement(
        "56\t14",
        """ This command displays the number of gratings. """,
        get_process=lambda x: SpectralProductsCM110._process_query_response(x),
        values=["Microns", "Nanometers", "Angstroms"],
        map_values=True,
    )
    '''
    wavelength_units = Instrument.control(
        "56\t14", "50\t%s"
        """ This command displays the number of gratings. """,
        get_process=lambda x: SpectralProductsCM110._process_query_response(x),
        values=["Microns", "Nanometers", "Angstroms"],
        map_values=True,
    )
    '''
    number_of_gratings = Instrument.measurement(
        "56\t13",
        """ This command displays the current units. """,
        get_process=lambda x: SpectralProductsCM110._process_query_response(x),
    )
    '''
    grating = Instrument.control(
        "56\t4",
        "26\t%s",
        """ Controls the wavelength setting. """,
        get_process=lambda x: SpectralProductsCM110._process_query_response(x),
        set_process=lambda x: SpectralProductsCM110._process_wavelength_encoding(x),
        check_set_errors=True,
    )
    '''

    def __init__(self, port, grating_ruling=2400):
        super(SpectralProductsCM110, self).__init__(
            SpectralProductsUSBAdapter(port),
            "Spectral Products CM110 Compact 1/8m Monochromator",
        )
        self.grating_ruling = grating_ruling

    def check_errors(self):
        response = self.read()

    def query(self, query_byte):
        start_byte = "56"
        query = "\t".join([start_byte, query_byte])
        response = self.ask(query)
        response_bytearray = [i for i in bytearray(response)]
        status_byte = response_bytearray[-1]
        if status_byte != 24:
            raise Exception("Incorrect status byte received.")

        high_byte = binascii.hexlify(struct.pack("B", response_bytearray[0]))
        low_byte = binascii.hexlify(struct.pack("B", response_bytearray[1]))
        # decoded_msg = int((high_byte + low_byte).decode("ascii"), 16)
        decoded_msg = int((high_byte + low_byte), 16)
        return decoded_msg

    def reset(self):
        self.write("255\t255\t255")
