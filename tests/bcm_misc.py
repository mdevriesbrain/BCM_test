import os, sys
import time
import subprocess

from polish import Measurement
from control.bcm_interface import Ifconfig, LidarPing, ImuInterface, ImuGyroInterface, BiosVerify, Eeprogram

class DUTEeprogram(Measurement):
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
        super(DUTEeprogram, self).__init__(meas_assets)

    # Setup the measurement
    def setup(self):
        pass

    # Read the Digital value from the DUT and validate
    def measure(self):
        result, value = Eeprogram(self._meas_assets, self._dut_name, self.test_id).run()
        self.test_points[self.test_point_name].execute(value)

    # Now turn the Digital output off
    def tear_down(self):
        pass


class DUTBiosVerify(Measurement):
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
        super(DUTBiosVerify, self).__init__(meas_assets)

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
        result, value = BiosVerify(self._meas_assets, self._dut_name, self.test_id).run()
        self.test_points[self.test_point_name].execute(value)

    # Now turn the Digital output off
    def tear_down(self):
        pass

class DUTImuVerify(Measurement):
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
        super(DUTImuVerify, self).__init__(meas_assets)

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
        result, value = ImuInterface(self._meas_assets, self._dut_name, self.test_id).run()
        self.test_points[self.test_point_name].execute(result)

    # Now turn the Digital output off
    def tear_down(self):
        pass

class DUTImuGyroVerify(Measurement):
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
        super(DUTImuGyroVerify, self).__init__(meas_assets)

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
        result, value = ImuGyroInterface(self._meas_assets, self._dut_name, self.test_id).run()
        self.test_points[self.test_point_name].execute(result)

    # Now turn the Digital output off
    def tear_down(self):
        pass

class DUTEthVerify(Measurement):
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
        super(DUTEthVerify, self).__init__(meas_assets)

    # Setup the measurement
    def setup(self):
        pass

    # Read the Digital value from the DUT and validate
    def measure(self):
        result, value = Ifconfig(self._meas_assets, self._dut_name, self.test_id).run()
        self.test_points[self.test_point_name].execute(value)

    # Now turn the Digital output off
    def tear_down(self):
        pass


class DUTEthPing(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''
    ping_start_str = 'Reply from '
    ping_end_str = ': bytes=32 time'
    waitTime = 10

    def __init__(self, meas_assets, dut_name, test_point_name, sleep_time=1):
        self._meas_assets = meas_assets
        self._dut_name = dut_name
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.test_id = test_point_name
        self.sleep_time = sleep_time
        self.test_config = meas_assets.test_config
        super(DUTEthPing, self).__init__(meas_assets)

    # Setup the measurement
    def setup(self):
        host = self.test_config[self.test_id]._pin

        self.cmd = 'ping -n 1 ' + host
        self.ping_str = self.ping_start_str + str(host) + self.ping_end_str
        self.result = False
        
    # Read the Digital value from the DUT and validate
    def measure(self):
        #
        # NOTE: Since I don't know if this IP is alive yet I'll try to "ping" it for a bit (or till it answers).
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
                    print "TIMEOUT waiting for reply from %s" % (str(self.test_config[self.test_id]._pin))
                    break
                else:
                    time.sleep(self._sleep_time)
            except:
                pass

        self.test_points[self.test_point_name].execute(int(self.result), raiseOnFail=True)

    # Now turn the Digital output off
    def tear_down(self):
        pass


class DUTLidarPing(Measurement):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''

    def __init__(self, meas_assets, dut_name, test_point_name, sleep_time=1):
        self._meas_assets = meas_assets
        self._dut_name = dut_name
        self.test_point_name = test_point_name
        self.test_point_uids = (test_point_name,)
        self.test_id = test_point_name
        self.sleep_time = sleep_time
        self.test_config = meas_assets.test_config
        super(DUTLidarPing, self).__init__(meas_assets)

    # Setup the measurement
    def setup(self):
        pass

    # Read the Digital value from the DUT and validate
    def measure(self):
        result, value = LidarPing(self._meas_assets, self._dut_name, self.test_id).run()
        self.test_points[self.test_point_name].execute(int(result))

    # Now turn the Digital output off
    def tear_down(self):
        pass


