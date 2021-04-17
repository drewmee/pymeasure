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

import time

import pytest
from pymeasure.instruments.spectralproducts.spectralproductsCM110 import (
    SpectralProductsCM110,
)

# pytest.skip('Only work with connected hardware', allow_module_level=True)


class TestSpectralProductsCM110:
    """
    Unit tests for SpectralProductsCM110 class.

    This test suite, needs the following setup to work properly:
        - A SpectralProductsCM110 device should be powered and connected to the computer
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.cm110 = SpectralProductsCM110("/dev/monochrom_usb")

    def test_echo(self):
        response = self.cm110.echo
        assert response == 27

    def test_serial_number(self):
        response = self.cm110.serial_number
        assert response == 23721

    def test_grooves(self):
        return

    def test_blaze(self):
        return

    def test_number_of_gratings(self):
        response = self.cm110.number_of_gratings
        assert response == 1

    def test_reset(self):
        self.cm110.reset()
        time.sleep(10)
        assert self.cm110.wavelength == 0

    def test_wavelength(self):
        self.cm110.wavelength = 0
        assert self.cm110.wavelength == 0

        self.cm110.wavelength = 1
        assert self.cm110.wavelength == 1

    def test_wavelength_units(self):
        response = self.cm110.wavelength_units
        assert response == "Nanometers"

    def test_scan_speed(self):
        return
        self.cm110.scan_speed = somevalue
        assert self.cm110.scan_speed == somevalue

    def test_step_size(self):
        return

    def test_scan(self):
        return

    """
    def test_query(self):
        response = self.cm110.query("4")
        print(response)
    """
