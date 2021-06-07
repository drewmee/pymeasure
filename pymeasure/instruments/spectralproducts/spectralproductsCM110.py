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
import time

from pymeasure.instruments import Instrument, validators

from .adapters import SpectralProductsUSBAdapter


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
        r = bytes.fromhex(ast.literal_eval(r)[0])

        response_bytearray = [i for i in bytearray(r)]
        high_byte = binascii.hexlify(struct.pack("B", response_bytearray[0]))
        low_byte = binascii.hexlify(struct.pack("B", response_bytearray[1]))
        status_byte = response_bytearray[-2]
        end_byte = response_bytearray[-1]

        if status_byte >= 128:
            raise Exception("Incorrect status byte received.")
        if end_byte != 24:
            raise Exception("Incorrect end byte received.")

        decoded_msg = int((high_byte + low_byte), 16)
        return decoded_msg

    def _process_wavelength_encoding(wl):
        return tuple(i for i in bytearray(struct.pack(">H", wl)))

    def _process_echo(r):
        r_hex = bytes.fromhex(ast.literal_eval(r)[0])
        return int(binascii.hexlify(r_hex), 16)

    '''
    echo = Instrument.measurement(
        "27",
        """ Verifies communications with the device. """,
        get_process=lambda x: SpectralProductsCM110._process_echo(x),
    )
    '''
    serial_number = Instrument.measurement(
        "56\t19",
        """ Gets the serial number. """,
        get_process=lambda x: SpectralProductsCM110._process_query_response(x),
    )
    wavelength = Instrument.control(
        "56\t0",
        "16\t%s\t%s",
        """ Controls the wavelength setting. """,
        # validator=validators.strict_range,
        # values=[-1, 1]
        get_process=lambda x: SpectralProductsCM110._process_query_response(x),
        set_process=lambda x: SpectralProductsCM110._process_wavelength_encoding(x),
        check_set_errors=True,
    )
    wavelength_units = Instrument.control(
        "56\t14",
        "50\t%d",
        """ Controls the units that wavelength is reported in. """,
        get_process=lambda x: SpectralProductsCM110._process_query_response(x),
        validator=validators.strict_discrete_set,
        values={"Microns": 0, "Nanometers": 1, "Angstroms": 2},
        map_values=True,
        check_set_errors=True,
    )
    number_of_gratings = Instrument.measurement(
        "56\t13",
        """ Get the number of gratings installed in the device. """,
        get_process=lambda x: SpectralProductsCM110._process_query_response(x),
    )
    grating = Instrument.control(
        "56\t4",
        "26\t%s",
        """  Selects the grating to be used. """,
        get_process=lambda x: SpectralProductsCM110._process_query_response(x),
        validator=validators.strict_discrete_set,
        values=[1, 2],
        check_set_errors=True,
    )
    grooves = Instrument.measurement(
        "56\t2",
        """ Gets the grooves/mm of the current grating. """,
        get_process=lambda x: SpectralProductsCM110._process_query_response(x),
    )
    blaze = Instrument.measurement(
        "56\t3",
        """ Get the blaze. """,
        get_process=lambda x: SpectralProductsCM110._process_query_response(x),
    )
    step_size = Instrument.measurement(
        "56\t6",
        """  Get the step size used in scanning. """,
        get_process=lambda x: SpectralProductsCM110._process_query_response(x),
    )
    scan_speed = Instrument.measurement(
        "56\t5",
        """ Get the scan speed used in scanning. """,
        get_process=lambda x: SpectralProductsCM110._process_query_response(x),
    )

    def __init__(self, port, clear_buffer=True):
        super(SpectralProductsCM110, self).__init__(
            SpectralProductsUSBAdapter(port),
            "Spectral Products CM110 Compact 1/8m Monochromator",
        )
        if clear_buffer:
            self.adapter.connection.flush()
            self.adapter.connection.reset_input_buffer()
            self.adapter.connection.reset_output_buffer()

        #self.grating_ruling = grating_ruling
        # Current grating installed: AG2400-00240-303

    def check_errors(self):
        r = self.read()
        r = bytes.fromhex(r[0])
        response_bytearray = [i for i in bytearray(r)]
        status_byte = response_bytearray[-2]
        end_byte = response_bytearray[-1]
        
        if status_byte >= 128:
            raise Exception("Incorrect status byte received.")
        if end_byte != 24:
            raise Exception("Incorrect end byte received.")

    def query(self, query_byte):
        start_byte = "56"
        query = "\t".join([start_byte, query_byte])
        response = self.ask(query)
        decoded_msg = SpectralProductsCM110._process_query_response(response)
        return decoded_msg

    def reset(self, delay=30):
        self.write("255\t255\t255")
        time.sleep(delay)
        
        self.adapter.connection.flush()
        self.adapter.connection.reset_input_buffer()
        self.adapter.connection.reset_output_buffer()


    def echo(self):
        self.write("27")
        
        r = self.adapter.read_echo()
        r = bytes.fromhex(r[0])
        r = bytearray(r)[0]
        
        if r != 27:
            raise Exception("Incorrect echo byte received.")
        
        return r
