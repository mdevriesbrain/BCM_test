
import os, sys
import time

from polish import Job, Measurement

class DutPower(Job):
    '''
    A job is the basic unit of work in an ATE test based on the polish library.
    Jobs do necessary tasks that are not linked to the collection of data.
    Each job should be as limited in scope as possible.
    See polish/measurement/measurement.py
    '''
    def __init__(self, meas_assets, supply_name, voltage, current, sleep_time=1):
        self._supply_name = supply_name
        self._voltage = voltage
        self._current = current
        self._sleep_time = sleep_time
        Measurement.__init__(self, meas_assets)

    def job(self):
        '''
        The job method is executed when run() is called.
        See polish/measurement/measurement.py
        '''
        supply = self.instruments[self._supply_name]

        '''
        Either:
            Turns on the power supply cofigured as POWER_SUPPLY1.
            Sets voltage to 24 VDC
            Sets current limit to 2.6 Amps
        Or:
            Turns off the power supply cofigured as POWER_SUPPLY1.
            Sets voltage to 0 VDC
            Sets current limit to 0 Amps
        '''
        if self._voltage:
            supply.set_voltage(self._voltage)
            supply.set_current(self._current)
            supply.output_on()

        else:
            supply.output_off()
            supply.set_voltage(0)
            supply.set_current(0)


class DutKeySenseOn(Job):
    '''
    A job is the basic unit of work in an ATE test based on the polish library.
    Jobs do necessary tasks that are not linked to the collection of data.
    Each job should be as limited in scope as possible.
    See polish/measurement/measurement.py
    '''
    def __init__(self, meas_assets, supply_name, mux_name, slot, channel, bit, sleep_time=1):
        self._supply_name = supply_name
        self._mux_name = mux_name
        self._slot = (slot*100)
        self._channel = channel
        self.slotChan = self._slot + self._channel
        self._bit = 1<<bit
        self._sleep_time = sleep_time
        Measurement.__init__(self, meas_assets)

    def job(self):
        '''
        The job method is executed when run() is called.
        See polish/measurement/measurement.py
        '''
        supply = self.instruments[self._supply_name]
        mux = self.instruments[self._mux_name]
        mux.set_dio_out(self.slotChan, self._bit)
        
        # I need this delay because there is a dip in the current right after power up that I need to ignore...
        time.sleep(self._sleep_time)


class DutKeySenseOff(Job):
    
    limit = 0.5
    shutdownWait = 10

    '''
    A job is the basic unit of work in an ATE test based on the polish library.
    Jobs do necessary tasks that are not linked to the collection of data.
    Each job should be as limited in scope as possible.
    See polish/measurement/measurement.py
    '''
    def __init__(self, meas_assets, supply_name, mux_name, slot, channel, bit, sleep_time=3):
        self._supply_name = supply_name
        self._mux_name = mux_name
        self._slot = (slot*100)
        self._channel = channel
        self.slotChan = self._slot + self._channel
        self._bit = bit
        self._sleep_time = sleep_time
        Measurement.__init__(self, meas_assets)

    def job(self):
        '''
        The job method is executed when run() is called.
        See polish/measurement/measurement.py
        '''
        supply = self.instruments[self._supply_name]
        mux = self.instruments[self._mux_name]
        mux.set_dio_out(self.slotChan, self._bit)
        current = supply.measure_current()

        # Give the DUT some time to start the shutdown...
        time.sleep(self.shutdownWait)

        while True:
            current = supply.measure_current()

            # When the AMP drops below the limit the DUT is powered DOWN
            if current > self.limit:
                time.sleep(self._sleep_time)
            else:
                break

