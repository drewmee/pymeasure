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

    '''
    def test_tmp(self):
        
        for grating in [1,2]:
            flag = 0
            
            self.cm110.grating = grating
            print("GRATING:", self.cm110.grating)
            
            self.cm110.wavelength = 0
            print("WAVELENGTH:", self.cm110.wavelength)

            #for j, i in enumerate(range(320, 720+10, 2)):
            for j, i in enumerate(range(180, 680, 10)):
                print(j,i)
                self.cm110.wavelength = i
                time.sleep(0.1)
                wl = self.cm110.wavelength
                try:
                    assert wl == i
                except:
                    print("WTF",i,wl)
                    if not flag:
                        self.cm110.adapter.connection.flush()
                        self.cm110.adapter.connection.reset_input_buffer()
                        self.cm110.adapter.connection.reset_output_buffer()
                        self.cm110.reset()
                        flag = 1
        return

        for j in range(5):
            for i in [i for i in range(350, 720+20, 20)]:
                self.cm110.wavelength = i
                time.sleep(0.1)
                wl = self.cm110.wavelength
                try:
                    assert wl == i
                except:
                    print("WTF",i,wl)
    '''
    def test_echo(self):
        assert self.cm110.echo() == 27

    def test_serial_number(self):
        assert self.cm110.serial_number == 23721

    def test_reset(self):
        self.cm110.reset()
        assert self.cm110.wavelength == 0

    def test_number_of_gratings(self):
        assert self.cm110.number_of_gratings == 2

    def test_grating(self):
        for grating_number in [1,2]:
            self.cm110.grating = grating_number
            assert self.cm110.grating == grating_number

    def test_grooves(self):
        self.cm110.grating = 1
        assert self.cm110.grooves == 2400

        self.cm110.grating = 2
        assert self.cm110.grooves == 300

    def test_blaze(self):
        assert self.cm110.blaze

    def test_wavelength_units(self):
        self.cm110.wavelength_units = "Nanometers"
        assert self.cm110.wavelength_units == "Nanometers"

        self.cm110.wavelength_units = "Microns"
        assert self.cm110.wavelength_units == "Microns"

        self.cm110.wavelength_units = "Angstroms"
        assert self.cm110.wavelength_units == "Angstroms"

    def test_gratings_and_wavelengths(self):
        if self.cm110.wavelength_units != "Nanometers":
            self.cm110.wavelength_units = "Nanometers"

        if self.cm110.wavelength != 0:
            self.cm110.reset()

        for grating_number in [1,2]:
            self.cm110.grating = grating_number
            assert self.cm110.grating == grating_number
            
            for wl in range(320, 730, 5):
                self.cm110.wavelength = wl
                time.sleep(0.1)
                assert self.cm110.wavelength == wl

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
