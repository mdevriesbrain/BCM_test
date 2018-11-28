import os, sys
import time
import logging

#non standard path management because demo is inside the polish package
sys.path.append(os.path.abspath(os.path.join('..')))

from polish import default_setup
from polish import generate_default_report

from polish.mfg_common.constants import RAISE_ON_FAIL
from control.constants import SHUT_DOWN_AFTER_TESTING
from control.load_tests import test_20v_load, test_24v_load, test_36v_load
from control.measurement_tests import measurement_tests
from control.bcm_power import DutPower, DutKeySenseOn, DutKeySenseOff
from tests.bcm_power_tests import DutKeySenseMeasurement
from tests.bcm_load_tests import LoadMeasurement


if __name__ == '__main__':

    # Get the time now so I can show how long this script runs...
    start_time = time.time()

    # By default this test will turn OFF the DUT when finished testing. To change this set the 'SHUT_DOWN_AFTER_TESTING' flag in 'control.constants.py'.
    shutDownAfterTest = SHUT_DOWN_AFTER_TESTING

    # By default this test will stop after the first test failure. To change this set the 'RAISE_ON_FAIL' flag in 'polish.mfg_common.constants.py'.
    raiseOnFail = RAISE_ON_FAIL

    # Initialize a count of the Test cases
    testCount = 0

    '''
    This script is called by passing it three files.
    - an environment config ini file, which contains information about the specific test station
    - a test config ini file which contains information about this test
    - a limits csv file which conatins config information for each test point and limtis for each
    EXAMPLE: python "script_name".py env.ini test.ini limits.csv
    '''
    script_name, env_conf_filename, test_conf_filename, limits_csv_filename = sys.argv
    
    # Identify if the DUT will shutdown after testing...
    if shutDownAfterTest:
        print "DUT WILL POWEROFF WHEN TESTING IS COMPLETE..."
    else:
        print "DUT WILL NOT POWEROFF WHEN TESTING IS COMPLETE..."

    # Identify if the Testing will stop at the first error
    if raiseOnFail:
        print "TESTING WILL STOP AFTER FIRST TEST FAILURE..."
    else:
        print "TESTING WILL NOT STOP AFTER ANY TEST FAILURES"

    polish_logger, env_config, test_config, test_point_map, meas_assets = \
            default_setup(env_conf_filename, test_conf_filename, limits_csv_filename)
    
    print 'Begin Testing Board type:%d...' % (meas_assets.dut_comms['DUT1']._version)

    # Next run the measurements
    try:

        #
        # NOTE: After the Power and Key Sense are applied the DUT will still take some time to boot up (approx. 60s).
        #       Currnetly we are running the Load tests (36v, 20v and 24v) before we start testing and these
        #       tests don't communicate with the DUT. But, the Key sense test will "ping" the DUT before checking
        #       the current to ensure the DUT is running before continuing with the testing...
        #
        #       These 2 functions are considered control and are not tests so they are NOT included in the test count.
        #

        # First Power On the DUT (36v) with the Power On and Key Sense objects (these are NOT tests)
        DutPower(meas_assets, 'POWER_SUPPLY1', voltage=36, current=2.6).run()
        DutKeySenseOn(meas_assets, 'POWER_SUPPLY1', 'MUX2', slot=2, channel=2, bit=1).run()

        #
        # NOTE: The following test will "ping" the DUT to ensure it's up and running before allowing the remaining
        #       tests to run.
        #

        # Next verify the Voltage after the 'Key-Sense' was applied
        DutKeySenseMeasurement(meas_assets, 'DUT1', 'POWER_SUPPLY1', 'MUX2', 'KEY_SENSE_1', slot=2, channel=2, bit=1).run()
        testCount = 1

        # Now run the 36v Load tests
        loadTests_36v = test_36v_load(meas_assets)
        testCount += loadTests_36v

        # Now reduce to 20v and run the Load tests again
        # I don't need Key-sense again, it's still on...
        DutPower(meas_assets, 'POWER_SUPPLY1', voltage=20, current=2.6).run()

        # Now run the 20v Load tests
        loadTests_20v = test_20v_load(meas_assets)
        testCount += loadTests_20v
            
        # Now increase to 24v and run ALL the DUT tests (including the Load tests again)
        # I don't need Key-sense again, it's still on...
        DutPower(meas_assets, 'POWER_SUPPLY1', voltage=24, current=2.6).run()

        # Finally run the 24v Load tests
        loadTests_24v = test_24v_load(meas_assets)
        testCount += loadTests_24v

        # And run the rest of the DUT tests
        testCount += measurement_tests(meas_assets)

    # Finally Power Off the DUT and report results
    finally:

        print 'Board type:%d testing complete...' % (meas_assets.dut_comms['DUT1']._version)

        # When requested the DUT will shutdown when ALL tests finish
        if shutDownAfterTest:
            print 'POWEROFF REQUESTED, SHUTTING DOWN NOW...'

            # Power Off the DUT with the Power Off and Key Sense objects
            DutKeySenseOff(meas_assets, 'POWER_SUPPLY1', 'MUX2', slot=2, channel=2, bit=0).run()
            DutPower(meas_assets, 'POWER_SUPPLY1', voltage=0, current=0).run()

        else:
            print 'POWEROFF NOT REQUESTED, LEAVING DUT POWERED ON!!!'

        # Generate the Test PASS/FAIL Report
        generate_default_report(test_point_map)

        # Verify there is 1 Test limit for each Test case
        if (test_point_map.get_count() > testCount):
            print "WARN: Test Coverage %d/%d, Test Cases/Tests run" % (test_point_map.get_count(), testCount)
        else:
            print "Test Cases: %d/%d" % (test_point_map.get_count(), testCount)

        # Either all tests pass or show the number of failures...
        if test_point_map.all_executed_all_pass():
            print 'ALL TESTS PASS'
        else:
            print 'Test Failures %d' % (test_point_map.get_error_count())
        
        print "Test duration:%dsec" % (time.time() - start_time)
