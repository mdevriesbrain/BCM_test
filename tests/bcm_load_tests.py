import os, sys
import time

from polish import Measurement

class LoadMeasurement(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''
    text_str = "LD Test "

    def __init__(self, meas_assets, test_point_name, mux, slot, channel, sleep_time=1):
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.mux_name = mux
        self.sleep_time = sleep_time
        self.slotChan = (slot*100) + channel
        super(LoadMeasurement, self).__init__(meas_assets)

    def setup(self):
        self.mux = self.instruments[self.mux_name]
        self.mux.display_text(self.text_str+str(self.slotChan))

    def measure(self):
        curr = self.mux.measure_vdc(self.slotChan)
        self.test_points[self.test_point_name].execute(abs(curr))
        time.sleep(self.sleep_time)

    # Now finish the test
    def tear_down(self):
        self.mux.display_clear()
