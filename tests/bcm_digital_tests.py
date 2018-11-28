import os, sys
import time

from polish import Measurement
from control.bcm_interface import ReadADC, ReadDUT, WriteDUT

class DigitalInputMeasurement(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''
    text_str = "DI "
    ON = 1
    OFF = 0

    def __init__(self, meas_assets, dut_name, test_point_name, mux, slot, channel, bit, sleep_time=1):
        self._meas_assets = meas_assets
        self._dut_name = dut_name
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.mux_name = mux
        self.test_id = test_point_name
        self.slot = slot
        self.slotChan = (slot*100) + channel
        self.bit = 1<<bit
        self.sleep_time = sleep_time
        super(DigitalInputMeasurement, self).__init__(meas_assets)

    # Setup the measurement
    def setup(self):
        self.mux = self.instruments[self.mux_name]
        self.mux.display_text(self.text_str+str(self.slotChan))

        # If this is working with Slot 2, Chan 2 (202) then remember to keep bit 1 ON (it's the key-sense)
        if self.slotChan == 202:
            self.bit |= 1<<1

        self.mux.set_dio_out(self.slotChan, self.bit)
        time.sleep(self.sleep_time)

    # Read the Digital value from the DUT and validate
    def measure(self):
        #import code
        #code.interact(local = locals())
        #pip install pyreadline
        #>>>import readline, rlcompleter
        #>>>readline.parse_and_bind('tab:complete')
        result, value = ReadDUT(self._meas_assets, self._dut_name, self.test_id).run()
        self.test_points[self.test_point_name].execute(value)
        time.sleep(self.sleep_time)

    # Now turn the Digital output off
    def tear_down(self):

        # If this is working with Slot 2, Chan 2 (202) then remember to keep bit 1 ON (it's the key-sense)
        if self.slotChan == 202:
            self.bit = 1<<1
        else:
            self.bit = self.OFF
        self.mux.set_dio_out(self.slotChan, self.bit)
        self.mux.display_clear()


class DigitalOutputMeasurement(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''
    text_str = "DO "
    ON = 1
    OFF = 0

    def __init__(self, meas_assets, dut_name, test_point_name, mux, slot, channel, sleep_time=1):
        self._meas_assets = meas_assets
        self._dut_name = dut_name
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.test_id = test_point_name
        self.mux_name = mux
        self.sleep_time = sleep_time
        self.slotChan = (slot*100) + channel
        super(DigitalOutputMeasurement, self).__init__(meas_assets)

    # Setup the measurement
    def setup(self):
        self.mux = self.instruments[self.mux_name]
        self.mux.display_text(self.text_str+str(self.slotChan))

    # Read the Digital output from the DUT and validate
    def measure(self):
        WriteDUT(self._meas_assets, self._dut_name, self.test_id, self.ON).run()
        time.sleep(self.sleep_time)

        # Verify the result of reading the DUT output voltage
        curr = self.mux.measure_vdc(self.slotChan)
        self.test_points[self.test_point_name].execute(abs(curr))
        time.sleep(self.sleep_time)

    # Now turn the Digital output off
    def tear_down(self):
        WriteDUT(self._meas_assets, self._dut_name, self.test_id, self.OFF).run()
        self.mux.display_clear()

class DigitalOutputMeasurement0(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''
    text_str = "DO "
    ON = 1
    OFF = 0

    def __init__(self, meas_assets, dut_name, test_point_name, mux, slot, channel, sleep_time=1):
        self._meas_assets = meas_assets
        self._dut_name = dut_name
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.test_id = test_point_name
        self.mux_name = mux
        self.sleep_time = sleep_time
        self.slotChan = (slot*100) + channel
        super(DigitalOutputMeasurement0, self).__init__(meas_assets)

    # Setup the measurement
    def setup(self):
        self.mux = self.instruments[self.mux_name]
        self.mux.display_text(self.text_str+str(self.slotChan))

    # Read the Digital output from the DUT and validate
    def measure(self):
        WriteDUT(self._meas_assets, self._dut_name, self.test_id, self.OFF).run()
        time.sleep(self.sleep_time)

        # Verify the result of reading the DUT output voltage
        curr = self.mux.measure_vdc(self.slotChan)
        self.test_points[self.test_point_name].execute(abs(curr))
        time.sleep(self.sleep_time)

    # Now turn the Digital output off
    def tear_down(self):
        self.mux.display_clear()

class DigitalEstop1Measurement(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''
    text_str = "DO "
    ON = 1
    OFF = 0

    def __init__(self, meas_assets, dut_name, test_point_name, mux, slot1, channel1, bit1, slot2, channel2, sleep_time=1):
        self._meas_assets = meas_assets
        self._dut_name = dut_name
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.test_id1 = test_point_name
        self.test_id2 = 'ESTOP_IN_1'
        self.test_id3 = 'ESTOP2_OUT_1'
        self.mux_name = mux
        self.sleep_time = sleep_time
        self.slotChan1 = (slot1*100) + channel1
        self.slotChan2 = (slot2*100) + channel2
        self.bit = bit1
        super(DigitalEstop1Measurement, self).__init__(meas_assets)

    # Setup the measurement
    def setup(self):
        # If this is working with Slot 2, Chan 2 (202) then remember to keep bit 1 ON (it's the key-sense)
        if self.slotChan1 == 202:
            self.bit |= 1<<1

        self.mux = self.instruments[self.mux_name]
        self.mux.display_text('DIDO'+str(self.slotChan1)+str(self.slotChan2))
        self.mux.set_dio_out(self.slotChan1, self.bit)
        time.sleep(self.sleep_time)

    # Read the Digital output from the DUT and validate
    def measure(self):
        WriteDUT(self._meas_assets, self._dut_name, self.test_id1, self.OFF).run()
        time.sleep(self.sleep_time)
        
        # Start with a bad value
        curr = -0.1

        # Read the state of the first pin
        result, value = ReadDUT(self._meas_assets, self._dut_name, self.test_id2).run()

        # Verify the pin state is low
        if result & value == 0:
            # Read the state of the second pin
            result, value = ReadDUT(self._meas_assets, self._dut_name, self.test_id3).run()
                
            # Verify the pin state is low
            if result & value == 0:
                # Read the DUT output voltage
                curr = abs(self.mux.measure_vdc(self.slotChan2))

        # Verify the result of reading the DUT output voltage
        self.test_points[self.test_point_name].execute(curr)
        time.sleep(self.sleep_time)

    # Now turn the Digital output off
    def tear_down(self):
        # If this is working with Slot 2, Chan 2 (202) then remember to keep bit 1 ON (it's the key-sense)
        if self.slotChan1 == 202:
            self.bit = 1<<1

        self.mux.set_dio_out(self.slotChan1, self.bit)
        self.mux.display_clear()

class DigitalEstop2Measurement(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''
    text_str = "DO "
    ON = 1
    OFF = 0

    def __init__(self, meas_assets, dut_name, test_point_name, mux, slot1, channel1, bit1, slot2, channel2, sleep_time=1):
        self._meas_assets = meas_assets
        self._dut_name = dut_name
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.test_id1 = test_point_name
        self.test_id2 = 'ESTOP_IN_2'
        self.test_id3 = 'ESTOP2_OUT_2'
        self.mux_name = mux
        self.sleep_time = sleep_time
        self.slotChan1 = (slot1*100) + channel1
        self.slotChan2 = (slot2*100) + channel2
        self.bit = bit1
        super(DigitalEstop2Measurement, self).__init__(meas_assets)

    # Setup the measurement
    def setup(self):
        # If this is working with Slot 2, Chan 2 (202) then remember to keep bit 1 ON (it's the key-sense)
        if self.slotChan1 == 202:
            self.bit |= 1<<1

        self.mux = self.instruments[self.mux_name]
        self.mux.display_text('DIDO'+str(self.slotChan1)+str(self.slotChan2))
        self.mux.set_dio_out(self.slotChan1, self.bit)
        time.sleep(self.sleep_time)

    # Read the Digital output from the DUT and validate
    def measure(self):
        WriteDUT(self._meas_assets, self._dut_name, self.test_id1, self.ON).run()
        time.sleep(self.sleep_time)

        # Start with a bad value
        curr = -0.1

        # Read the state of the first pin
        result, value = ReadDUT(self._meas_assets, self._dut_name, self.test_id2).run()

        # Verify the pin state is clear
        if result & value == self.OFF:
            # Read the state of the second pin
            result, value = ReadDUT(self._meas_assets, self._dut_name, self.test_id3).run()
                
            # Verify the pin state is low
            if result & value == self.OFF:
                # Read the DUT output voltage
                curr = abs(self.mux.measure_vdc(self.slotChan2))

        # Verify the result of reading the DUT output voltage
        self.test_points[self.test_point_name].execute(curr)
        time.sleep(self.sleep_time)

    # Now turn the Digital output off
    def tear_down(self):
        # If this is working with Slot 2, Chan 2 (202) then remember to keep bit 1 ON (it's the key-sense)
        if self.slotChan1 == 202:
            self.bit = 1<<1

        self.mux.set_dio_out(self.slotChan1, self.bit)

        WriteDUT(self._meas_assets, self._dut_name, self.test_id1, self.OFF).run()
        self.mux.display_clear()

class DigitalEstop3Measurement(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''
    text_str = "DO "
    ON = 1
    OFF = 0

    def __init__(self, meas_assets, dut_name, test_point_name, mux, slot1, channel1, bit1, slot2, channel2, sleep_time=1):
        self._meas_assets = meas_assets
        self._dut_name = dut_name
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.test_id1 = test_point_name
        self.test_id2 = 'ESTOP_IN_3'
        self.test_id3 = 'ESTOP2_OUT_3'
        self.mux_name = mux
        self.sleep_time = sleep_time
        self.slotChan1 = (slot1*100) + channel1
        self.slotChan2 = (slot2*100) + channel2
        self.bit = bit1
        super(DigitalEstop3Measurement, self).__init__(meas_assets)

    # Setup the measurement
    def setup(self):
        # If this is working with Slot 2, Chan 2 (202) then remember to keep bit 1 ON (it's the key-sense)
        if self.slotChan1 == 202:
            self.bit |= 1<<1

        self.mux = self.instruments[self.mux_name]
        self.mux.display_text('DIDO'+str(self.slotChan1)+str(self.slotChan2))
        self.mux.set_dio_out(self.slotChan1, self.bit)
        time.sleep(self.sleep_time)

    # Read the Digital output from the DUT and validate
    def measure(self):
        WriteDUT(self._meas_assets, self._dut_name, self.test_id1, self.OFF).run()
        time.sleep(self.sleep_time)

        # Start with a bad value
        curr = -0.1

        # Read the state of the first pin
        result, value = ReadDUT(self._meas_assets, self._dut_name, self.test_id2).run()

        # Verify the pin state is set
        if result & value == self.ON:
            # Read the state of the second pin
            result, value = ReadDUT(self._meas_assets, self._dut_name, self.test_id3).run()
                
            # Verify the pin state is set
            if result & value == self.ON:
                # Read the DUT output voltage
                curr = abs(self.mux.measure_vdc(self.slotChan2))

        # Verify the result of reading the DUT output voltage
        self.test_points[self.test_point_name].execute(curr)
        time.sleep(self.sleep_time)

    # Now turn the Digital output off
    def tear_down(self):
        # If this is working with Slot 2, Chan 2 (202) then remember to keep bit 1 ON (it's the key-sense)
        if self.slotChan1 == 202:
            self.bit = 1<<1

        self.mux.set_dio_out(self.slotChan1, self.bit)
        self.mux.display_clear()

class DigitalEstop4Measurement(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''
    text_str = "DO "
    ON = 1
    OFF = 0

    def __init__(self, meas_assets, dut_name, test_point_name, mux, slot1, channel1, bit1, slot2, channel2, sleep_time=1):
        self._meas_assets = meas_assets
        self._dut_name = dut_name
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.test_id1 = test_point_name
        self.test_id2 = 'ESTOP_IN_4'
        self.test_id3 = 'ESTOP2_OUT_4'
        self.mux_name = mux
        self.sleep_time = sleep_time
        self.slotChan1 = (slot1*100) + channel1
        self.slotChan2 = (slot2*100) + channel2
        self.bit = bit1
        super(DigitalEstop4Measurement, self).__init__(meas_assets)

    # Setup the measurement
    def setup(self):
        # If this is working with Slot 2, Chan 2 (202) then remember to keep bit 1 ON (it's the key-sense)
        if self.slotChan1 == 202:
            self.bit |= 1<<1

        self.mux = self.instruments[self.mux_name]
        self.mux.display_text('DIDO'+str(self.slotChan1)+str(self.slotChan2))
        self.mux.set_dio_out(self.slotChan1, self.bit)
        time.sleep(self.sleep_time)

    # Read the Digital output from the DUT and validate
    def measure(self):
        WriteDUT(self._meas_assets, self._dut_name, self.test_id1, self.ON).run()
        time.sleep(self.sleep_time)

        # Start with a bad value
        curr = -0.1

        # Read the state of the first pin
        result, value = ReadDUT(self._meas_assets, self._dut_name, self.test_id2).run()

        # Verify the pin state is set
        if result & value == self.ON:
            # Read the state of the second pin
            result, value = ReadDUT(self._meas_assets, self._dut_name, self.test_id3).run()
                
            # Verify the pin state is clear
            if result & value == self.OFF:
                # Read the DUT output voltage
                curr = abs(self.mux.measure_vdc(self.slotChan2))

        # Verify the result of reading the DUT output voltage
        self.test_points[self.test_point_name].execute(abs(curr))
        time.sleep(self.sleep_time)

    # Now turn the Digital output off
    def tear_down(self):
        # If this is working with Slot 2, Chan 2 (202) then remember to keep bit 1 ON (it's the key-sense)
        if self.slotChan1 == 202:
            self.bit = 1<<1

        self.mux.set_dio_out(self.slotChan1, self.bit)

        WriteDUT(self._meas_assets, self._dut_name, self.test_id1, self.OFF).run()
        self.mux.display_clear()

