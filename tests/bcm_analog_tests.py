import os, sys
import time

from polish import Measurement
from control.bcm_interface import ReadADC, ReadDUT, WriteDUT


class AnalogInputMeasurement(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''
    text_str = "AI "
    scale = 10.0

    def __init__(self, meas_assets, dut_name, test_point_name, mux_name, voltage, slot, channel, sleep_time=3):
        self._meas_assets = meas_assets
        self._dut_name = dut_name
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.test_id = test_point_name
        self.mux_name = mux_name
        self.voltage = voltage
        self.sleep_time = sleep_time
        self.slotChan = (slot*100) + channel
        super(AnalogInputMeasurement, self).__init__(meas_assets)

    # Setup the measurement
    def setup(self):
        self.mux = self.instruments[self.mux_name]
        self.mux.display_text(self.text_str+str(self.slotChan))
        self.mux.set_dac_out(self.slotChan, self.voltage)
        time.sleep(self.sleep_time)

    # Read the Analog value from the DUT and validate
    def measure(self):
        result, value = ReadADC(self._meas_assets, self._dut_name, self.test_id).run()

        # Since I can't return float create it from the response before validating
        new_value = float(value)/self.scale

        # Verify the result of reading the DUT
        self.test_points[self.test_point_name].execute(new_value)

    # Now turn the Analog input off
    def tear_down(self):
        self.mux.set_dac_out(self.slotChan, self.OFF)
        self.mux.display_clear()


class A4_20MaIn1AnalogInput(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''
    text_str = "AI "
    scale = 10.0

    def __init__(self, meas_assets, dut_name, test_point_name, mux_name, voltage, slot1, ch1, slot2, ch2, sleep_time=3):
        self._meas_assets = meas_assets
        self._dut_name = dut_name
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.test_id = test_point_name
        self.mux_name = mux_name
        self.voltage = voltage
        self.sleep_time = sleep_time
        self.slot1Chan1 = (slot1*100) + ch1
        self.slot2Chan2 = (slot2*100) + ch2
        super(A4_20MaIn1AnalogInput, self).__init__(meas_assets)

    # Setup the measurement
    def setup(self):
        self.mux = self.instruments[self.mux_name]
        self.mux.display_text(self.text_str+str(self.slot1Chan1)+str(self.slot2Chan2))
        self.mux.open_relay(self.slot1Chan1)
        self.mux.set_dac_out(self.slot2Chan2, self.voltage)
        time.sleep(self.sleep_time)

    # Read the Analog value from the DUT and validate
    def measure(self):
        result, value = ReadADC(self._meas_assets, self._dut_name, self.test_id).run()
        
        # Since I can't return float create it from the response before validating
        # In this case 3.3v is returned as 33 but I want 3.3
        new_value = float(value)/self.scale

        # Verify the result of reading the DUT
        self.test_points[self.test_point_name].execute(new_value)

    # Now turn the Analog input off
    def tear_down(self):
        self.mux.set_dac_out(self.slot2Chan2, self.OFF)
        self.mux.close_relay(self.slot1Chan1)
        self.mux.display_clear()

class A4_20MaIn2AnalogInput(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''
    text_str = "AI "
    scale = 10.0

    def __init__(self, meas_assets, dut_name, test_point_name, mux_name, voltage, slot1, slot2, ch1, ch2, sleep_time=3):
        self._meas_assets = meas_assets
        self._dut_name = dut_name
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.test_id = test_point_name
        self.mux_name = mux_name
        self.voltage = voltage
        self.sleep_time = sleep_time
        self.slot1Chan1 = (slot1*100) + ch1
        self.slot2Chan2 = (slot2*100) + ch2
        super(A4_20MaIn2AnalogInput, self).__init__(meas_assets)

    # Setup the measurement
    def setup(self):
        self.mux = self.instruments[self.mux_name]
        self.mux.display_text(self.text_str+str(self.slot1Chan1)+str(self.slot2Chan2))
        self.mux.close_relay(self.slot1Chan1)
        self.mux.set_dac_out(self.slot2Chan2, self.voltage)
        time.sleep(self.sleep_time)

    # Read the Analog value from the DUT and validate
    def measure(self):
        result, value = ReadADC(self._meas_assets, self._dut_name, self.test_id).run()
        
        # Since I can't return float create it from the response before validating
        # In this case 3.3v is returned as 33 but I want 3.3
        new_value = float(value)/self.scale

        # Verify the result of reading the DUT
        self.test_points[self.test_point_name].execute(new_value)

    # Now turn the Analog input off
    def tear_down(self):
        self.supply.set_dac_out(self.slot2Chan2, self.OFF)
        self.supply.open_relay(self.slot1Chan1)
        self.supply.display_clear()


