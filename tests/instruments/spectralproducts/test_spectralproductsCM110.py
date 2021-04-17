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
        assert self.cm110.echo == 27

    def test_serial_number(self):
        assert self.cm110.serial_number == 23721

    def test_reset(self):
        self.cm110.reset()
        assert self.cm110.wavelength == 0

    def test_grooves(self):
        assert self.cm110.grooves == 2400

    def test_blaze(self):
        assert self.cm110.blaze

    def test_number_of_gratings(self):
        assert self.cm110.number_of_gratings == 1

    def test_grating(self):
        self.cm110.grating = 2
        assert self.cm110.grating == 2

        self.cm110.grating = 1
        assert self.cm110.grating == 1

    def test_wavelength_units(self):
        self.cm110.wavelength_units = "Nanometers"
        assert self.cm110.wavelength_units == "Nanometers"

        self.cm110.wavelength_units = "Microns"
        assert self.cm110.wavelength_units == "Microns"

        self.cm110.wavelength_units = "Angstroms"
        assert self.cm110.wavelength_units == "Angstroms"

    def test_wavelength(self):
        if self.cm110.wavelength_units != "Angstroms":
            self.cm110.wavelength_units = "Angstroms"
        """
        for i in range(0, 20, 5):
            self.cm110.wavelength = i
            assert self.cm110.wavelength == i
        """

        self.cm110.reset()
        assert self.cm110.wavelength == 0

        # self.cm110.wavelength = 0
        # assert self.cm110.wavelength == 0

        self.cm110.wavelength = 6800
        assert self.cm110.wavelength == 6800

        self.cm110.wavelength = 7500
        assert self.cm110.wavelength == 7500

        # Out of range
        # self.cm110.wavelength = 7510
        # assert self.cm110.wavelength == 7510

    def test_step_size(self):
        assert self.cm110.step_size

    def test_scan_speed(self):
        assert self.cm110.scan_speed

    def test_scan(self):
        return

    """
    def test_query(self):
        response = self.cm110.query("4")
        print(response)
    """
