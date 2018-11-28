import os, sys
import time
import logging

#non standard path management because demo is inside the polish package
sys.path.append(os.path.abspath(os.path.join('..')))

from polish import default_setup
from polish import generate_default_report

from control.bcm_power import DutPower, DutKeySenseOn, DutKeySenseOff
from tests.bcm_power_tests import DutCurrentMeasurement, DutVoltageMeasurement
from tests.bcm_analog_tests import A4_20MaIn1AnalogInput, A4_20MaIn2AnalogInput, AnalogInputMeasurement
from tests.bcm_digital_tests import DigitalInputMeasurement, DigitalOutputMeasurement
from tests.bcm_usb_tests import DUTUsbVerify, DUTUsbChkSum, DUTUsbPerformance
from tests.bcm_misc import DUTEthVerify, DUTImuVerify, DUTImuGyroVerify, DUTBiosVerify, DUTEeprogram
from tests.bcm_load_tests import LoadMeasurement

if __name__ == '__main__':

    '''
    This script is called by passing it three files.
    - an environment config ini file, which contains information about the specific test station
    - a test config ini file which contains information about this test
    - a limits csv file which conatins config information for each test point and limtis for each
    EXAMPLE: python "script_name".py env.ini test.ini limits.csv
    '''
    script_name, env_conf_filename, test_conf_filename, limits_csv_filename = sys.argv

    polish_logger, env_config, test_config, test_point_map, meas_assets = \
            default_setup(env_conf_filename, test_conf_filename, limits_csv_filename)
    
    # Power Off the DUT with the Power Off and Key Sense objects
    DutKeySenseOff(meas_assets, 'POWER_SUPPLY1', 'MUX2', slot=2, channel=2, bit=0, sleep_time=10).run()
    DutPower(meas_assets, 'POWER_SUPPLY1', voltage=0, current=0).run()

