import os, sys
import time
import subprocess

from polish import Measurement


class DutCurrentMeasurement(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''
    def __init__(self, meas_assets, test_point_name, supply, sleep_time=1):
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.supply_name = supply
        self.sleep_time = sleep_time
        Measurement.__init__(self, meas_assets)

    def setup(self):
        self.supply = self.instruments[self.supply_name]

    def measure(self):
        '''
        The measure method is intended to collect data and use that data to execute() test points.
        Here we look up the power supply instrument, use it to get the current,
        and execute the init_current_1 test point.
        When executed the test point checks the current against the limits file passed in as limits_csv_filename.
        See polish/measurement/measurement.py
        see polish/test_point/test_point.py
        '''
        curr = self.supply.measure_current()
        self.test_points[self.test_point_name].execute(curr)
        time.sleep(self.sleep_time)

    def tear_down(self):
        pass


class DutVoltageMeasurement(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''
    def __init__(self, meas_assets, test_point_name, supply, sleep_time=1):
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.supply_name = supply
        self.sleep_time = sleep_time
        Measurement.__init__(self, meas_assets)

    def setup(self):
        self.supply = self.instruments[self.supply_name]

    def measure(self):
        '''
        The measure method is intended to collect data and use that data to execute() test points.
        Here we look up the power supply instrument, use it to get the current,
        and execute the init_current_1 test point.
        When executed the test point checks the current against the limits file passed in as limits_csv_filename.
        See polish/measurement/measurement.py
        see polish/test_point/test_point.py
        '''
        curr = self.supply.measure_voltage()
        self.test_points[self.test_point_name].execute(curr)
        time.sleep(self.sleep_time)

    def tear_down(self):
        pass

class DutKeySenseMeasurement(Measurement):
    '''
    A job is the basic unit of work in an ATE test based on the polish library.
    Jobs do necessary tasks that are not linked to the collection of data.
    Each job should be as limited in scope as possible.
    See polish/measurement/measurement.py
    '''
    ping_start_str = 'Reply from '
    ping_end_str = ': bytes=32 time'
    waitTime = 90

    def __init__(self, meas_assets, dut_name, supply_name, mux_name, test_point_name, slot, channel, bit, sleep_time=3):
        self._dut_name = dut_name
        self._supply_name = supply_name
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.test_id = test_point_name
        self._mux_name = mux_name
        self._slot = (slot*100)
        self._channel = channel
        self.slotChan = self._slot + self._channel
        self._bit = 1<<bit
        self._sleep_time = sleep_time
        super(DutKeySenseMeasurement, self).__init__(meas_assets)

    def setup(self):
        self.supply = self.instruments[self._supply_name]

        # Get the 'Host' IP address so we can 'ping' the DUT to ensure it's running...
        host = self.dut_comms[self._dut_name]._ip

        self.cmd = 'ping -n 1 ' + host
        self.ping_str = self.ping_start_str + str(host) + self.ping_end_str
        self.result = False

    def measure(self):
        #
        # NOTE: Since I don't know if the DUT is alive yet I'll try to "ping" it for 2min (or till it answers)
        #       before reading the Key Sense current.
        #
        startTime = time.time()

        while True:
            #
            # NOTE: During testing I found that the 'ping' command would throw an exception during startup.
            #       Since this does NOT indicate a failure (yet) I'm catching it and allowing the processing
            #       to continue until either the 'ping' is successfull or it times out.
            #
            try:
                result = subprocess.check_output(self.cmd, stderr=subprocess.STDOUT)

                # Check the 'ping' result
                if self.ping_str in result:

                    # Set my result, this test passed...
                    self.result = True
                    break

                if ((time.time() - startTime) > self.waitTime):
                    print "TIMEOUT waiting for reply from %s" % (str(self.dut_comms[self._dut_name]._ip))
                    break
                else:
                    time.sleep(self._sleep_time)
            except:
                pass

        self.test_points[self.test_point_name].execute(int(self.result), raiseOnFail=True)

    def tear_down(self):
        pass







