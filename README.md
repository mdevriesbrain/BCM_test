# BCM
An ATE platform for Brain Control Module (BCM) hardware manufacturing testing.

By default this test will turn OFF the DUT when finished testing. To change this set the 'SHUT_DOWN_AFTER_TESTING' flag in 'control.constants.py'.
By default this test will stop after the first test failure. To change this set the 'RAISE_ON_FAIL' flag in 'polish.mfg_common.constants.py'.

Use patterns from BCM/BCM_test.py

The IP address's assigned to the USB/Network adaptors:
IFM_FRONT: 192.168.0.100
IFM_LEFT:  192.168.1.100
IFM_RIGHT: 192.168.2.100
H LIDAR:   192.168.3.2
S LIDAR:   192.168.3.3
ACCESS PNL: 192.168.3.100
SERVICE:   192.168.100.100
