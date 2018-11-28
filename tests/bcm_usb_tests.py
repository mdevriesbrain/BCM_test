import os, sys
import time

from polish import Measurement
from control.bcm_interface import USBverify, USBchkSum, USBperformance

class DUTUsbVerify(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''
    text_str = "DI Test "
    ON = 1
    OFF = 0

    def __init__(self, meas_assets, dut_name, test_point_name, sleep_time=0):
        self._meas_assets = meas_assets
        self._dut_name = dut_name
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.test_id = test_point_name
        self.sleep_time = sleep_time
        #Measurement.__init__(self, meas_assets)
        super(DUTUsbVerify, self).__init__(meas_assets)

    # Setup the measurement
    def setup(self):
        pass

    # Read the Digital value from the DUT and validate
    def measure(self):
        #import code
        #code.interact(local = locals())
        #pip install pyreadline
        #>>>import readline, rlcompleter
        #>>>readline.parse_and_bind('tab:complete')
        result, value = USBverify(self._meas_assets, self._dut_name, self.test_id).run()
        self.test_points[self.test_point_name].execute(value)

    # Now turn the Digital output off
    def tear_down(self):
        pass

class DUTUsbChkSum(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''

    def __init__(self, meas_assets, dut_name, test_point_name, sleep_time=0):
        self._meas_assets = meas_assets
        self._dut_name = dut_name
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.test_id = test_point_name
        self.sleep_time = sleep_time
        #Measurement.__init__(self, meas_assets)
        super(DUTUsbChkSum, self).__init__(meas_assets)


    # Setup the measurement
    def setup(self):
        pass

    # Read the Digital value from the DUT and validate
    def measure(self):
        #import code
        #code.interact(local = locals())
        #pip install pyreadline
        #>>>import readline, rlcompleter
        #>>>readline.parse_and_bind('tab:complete')
        result, value = USBchkSum(self._meas_assets, self._dut_name, self.test_id).run()
        self.test_points[self.test_point_name].execute(value)

    # Now turn the Digital output off
    def tear_down(self):
        pass

class DUTUsbPerformance(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''

    def __init__(self, meas_assets, dut_name, test_point_name, sleep_time=0):
        self._meas_assets = meas_assets
        self._dut_name = dut_name
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.test_id = test_point_name
        self.sleep_time = sleep_time
        #Measurement.__init__(self, meas_assets)
        super(DUTUsbPerformance, self).__init__(meas_assets)

    # Setup the measurement
    def setup(self):
        pass

    # Read the Digital value from the DUT and validate
    def measure(self):
        #import code
        #code.interact(local = locals())
        #pip install pyreadline
        #>>>import readline, rlcompleter
        #>>>readline.parse_and_bind('tab:complete')
        result, value = USBperformance(self._meas_assets, self._dut_name, self.test_id).run()
        self.test_points[self.test_point_name].execute(value)

    # Now turn the Digital output off
    def tear_down(self):
        pass





