# ============================================================================
# Copyright 2018 BRAIN Corporation. All rights reserved. This software is
# provided to you under BRAIN Corporation's Beta License Agreement and
# your use of the software is governed by the terms of that Beta License
# Agreement, found at http://www.braincorporation.com/betalicense.
# ============================================================================

import logging
import sys
import os
import argparse
import paramiko
import time
import subprocess

from polish import Measurement
from polish.mfg_common.logging_setup import get_logger

class BCM(object):
    #
    # Define some const's for this app
    #
    WRITE_CMD = 0x01
    READ_CMD = 0x02
    ADC_CMD = 0x03
    BANK_STR = ['A', 'B', 'C', 'D', 'E', 'F']
    CMD = 'production_test.py'
    BIOS_VERIFY_CMD = 'bios_verify.py'
    EE_PROM_CMD = 'eeprom_program.py'
    IFCONFIG_CMD = 'ifconfig_iperf.py'
    IMU_CONFIG_CMD = 'imu_verify.py'
    IMU_GYRO_CONFIG_CMD = 'check_gyro_system.py'
    USB_CMD = 'usb_verify.py'
    USB_CHKSUM_CMD = 'usb_chksum.py'
    USB_PERFORM_CMD = 'usb_perform.py'
    CMD_PATH = '/opt/shining_software/catkin_ws/src/lowsheen/src/production'

    def __init__(self, ip, user, password, debug=False):

        _ip = ip
        _user = user
        _passwd = password

        self._debug = debug
        self._test_result = False
        self._test_value = 0
        self._connect = True
        self._lines = None
        self._errors = None
                
        # Get access to the 'polish' logger
        self._logger = get_logger(__file__)

        if (self._debug):
            self._logger.setLevel(level=logging.DEBUG)

        self._logger.debug("Connect: IP:%s", _ip,)
            
        #key = paramiko.RSAKey.from_private_key_file(BCM.KEY_FILE)
        #key = paramiko.DSSKey.from_private_key_file(BCM.KEY_FILE)
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #self._ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
        
        #if (self._debug):
        #    print "INFO:Connecting to " + _ip

        try:
            self._ssh.connect(_ip, username=_user, password=_passwd)
            #self._ssh.connect(_ip, username=_user, pkey=key)
        except Exception as e:
            self._connect = False
            self._logger.exception("%s", e)
        
    def isConnected(self):
        return self._connect

    # Execute the remote command and return the result
    def _run(self, cmd, args, debug=False):

        self._lines = None
        self._errors = None
        self._debug = debug

        self._logger.debug("Cmd:%s", cmd)
        self._logger.debug("Args:%s", args)
        
        # Run the remote shell script and get output/results
        stdin, stdout, stderr = self._ssh.exec_command('/usr/bin/python '+cmd+args)

        # Wait for the command to terminate
        while not stdout.channel.exit_status_ready() and not stdout.channel.recv_ready():
            time.sleep(1)
 
        self._lines = stdout.readlines()
        self._errors = stderr.readlines()

        # Any output from the DUT os comes through 'stderr' from the SSH portal
        for e_row in self._errors:
            self._logger.warn("SYS:" + e_row.strip("\r\n"))

        # Any output from the script executed on the DUT comes through 'stdout' from the SSH portal
        for l_row in self._lines:
            self._logger.info("APP:" + l_row.strip("\r\n"))
            
            # This is looking for the string "PASS XX" where XX is the value returned
            if ('PASS' in l_row):
                self._test_result = True
                tempVal = int(l_row[5])

                #
                # NOTE: There is a limitation on the DUT that prevents me from printing 'float' variables. So
                #       I'll multiple the DUT result by 10 and cast to integer. Then on receiving this value if
                #       it's 2 digits then create the appropiate value.
                #

                # Check if this is a 2 digit response
                if ((len(l_row.strip("\r\n")) > 6)):
                    tempVal *= 10
                    tempVal += int(l_row[6])

                # Save the return value for test result return
                self._test_value = tempVal

        return self._test_result, self._test_value

    def performanceUSB(self, indev, file, passwd, debug=False):

        # Build the SSH remote command to be executed
        cmd = self.CMD_PATH + '/' + self.USB_PERFORM_CMD
        args = ' -i ' + str(indev) + ' -p ' + str(passwd) + ' -o ' + str(file)

        # Execute the remote command with arguments and return the results
        return self._run(cmd, args, debug)

    def biosverify(self, bios):

        # Build the SSH remote command to be executed
        cmd = self.CMD_PATH + '/' + self.BIOS_VERIFY_CMD
        args = ' -b ' + bios

        # Execute the remote command with arguments and return the results
        return self._run(cmd, args)

    def eeprogram(self, mac_addr, passwd):

        # Build the SSH remote command to be executed
        cmd = self.CMD_PATH + '/' + self.EE_PROM_CMD
        args = ' -m ' + mac_addr + ' -p ' + passwd

        # Execute the remote command with arguments and return the results
        return self._run(cmd, args)

    def imuconfig(self, debug=False):

        # Build the SSH remote command to be executed
        cmd = self.CMD_PATH + '/' + self.IMU_CONFIG_CMD
        args = ' '

        # Execute the remote command with arguments and return the results
        return self._run(cmd, args, debug)

    def imugyroconfig(self, debug=False):

        # Build the SSH remote command to be executed
        cmd = self.CMD_PATH + '/' + self.IMU_GYRO_CONFIG_CMD
        args = ' '

        # Execute the remote command with arguments and return the results
        return self._run(cmd, args, debug)

    def ifconfig(self, host=None, debug=False):

        # Build the SSH remote command to be executed
        cmd = self.CMD_PATH + '/' + self.IFCONFIG_CMD

        if host is not None:
            args = ' -f ' + str(host)
        else:
            args = ' '

        # Execute the remote command with arguments and return the results
        return self._run(cmd, args, debug)

    def chksumUSB(self, file, debug=False):

        # Build the SSH remote command to be executed
        cmd = self.CMD_PATH + '/' + self.USB_CHKSUM_CMD
        args = ' -f ' + str(file)

        # Execute the remote command with arguments and return the results
        return self._run(cmd, args, debug)

    def readUSB(self, debug=False):

        # Build the SSH remote command to be executed
        cmd = BCM.CMD_PATH + '/' + BCM.USB_CMD
        args = ' '

        # Execute the remote command with arguments and return the results
        return self._run(cmd, args, debug)
    
    def readADC(self, pin, bank, func, arg, debug=False):

        # Build the SSH remote command to be executed
        cmd = BCM.CMD_PATH + '/' + BCM.CMD

        # Build the SSH remote command arguments
        args = ' -p ' + str(pin) + ' -b ' + bank + ' -f ' + str(func) + ' -a'

        # Debug...
        if (debug):
            args += ' -d'

        # Execute the remote command with arguments and return the results
        return self._run(cmd, args, debug)
    
    def readPin(self, pin, bank, func, arg, debug=False):

        # Build the SSH remote command to be executed
        cmd = BCM.CMD_PATH + '/' + BCM.CMD

        # Build the SSH remote command arguments
        args = ' -p ' + str(pin) + ' -b ' + bank + ' -f ' + str(func) + ' -r'

        # Debug...
        if (debug):
            args += ' -d'

        # Execute the remote command with arguments and return the results
        return self._run(cmd, args, debug)
    
    def writePin(self, pin, bank, func, arg, debug=False):

        # Build the SSH remote command to be executed
        cmd = BCM.CMD_PATH + '/' + BCM.CMD

        # Build the SSH remote command arguments
        args = ' -p ' + str(pin) + ' -b ' + bank + ' -f ' + str(func) + ' -w ' + str(arg)

        # Debug...
        if (debug):
            args += ' -d'

        # Execute the remote command with arguments and return the results
        return self._run(cmd, args, debug)
    
'''
This functions (WriteDUT1) will open an SSH connection to the DUT and command it to
write a pin value and return the value written.
'''
class WriteDUT(object):
    
    def __init__(self, meas_assets, dut_name, test_id, value, sleep_time=1):
        self.dut_comms = meas_assets.dut_comms
        self.test_config = meas_assets.test_config
        self.dut_name = dut_name
        self.test_id = test_id
        self.value = value
        self.sleep_time = sleep_time
        self._logger = get_logger(__file__)

    def run(self):
        '''
        First I need to get the info to open the SSH port to the DUT
        '''
        _name = self.dut_comms[self.dut_name]._name
        _ip = self.dut_comms[self.dut_name]._ip
        _user = self.dut_comms[self.dut_name]._user
        _passwd = self.dut_comms[self.dut_name]._passwd
        _debug = bool(self.dut_comms[self.dut_name]._debug)

        '''
        Now open the connection (SSH) to the DUT
        '''
        _dut = BCM(ip=_ip, user=_user, password=_passwd, debug=_debug)

        result = False
        value = 0

        # Verify the DUT is connected...
        if _dut.isConnected():

            self._logger.info("Connected...")

            cmd = self.test_config[self.test_id]._cmd
           
            # Call the Write command for the Pin and Bank provided to set the output
            if str(cmd) == 'W':
                '''
                Now that I have a connection gather the info needed to command the DUT to either
                drive a specified pin high or read the specified pin.
                '''
                pin = self.test_config[self.test_id]._pin
                bank = self.test_config[self.test_id]._bank
                func = self.test_config[self.test_id]._func
                arg = self.value
                debug = bool(self.test_config[self.test_id]._debug)

                result, value = _dut.writePin(pin, bank.upper(), func, arg, debug)
            
            else:
                self._logger.warn("%s:Cmd: %s NOT VALID for W", self.test_id, str(cmd))
                result, value = True, 0

            # If the DUT is connected then close the connection
            _dut._ssh.close()

        else:

            self._logger.error("NOT CONNECTED...")

        # Present the results
        if (result):
            self._logger.info("PASS %d", value)

        else:
            self._logger.error("FAIL")

        return result, value

'''
This functions (ReadDUT1) will open an SSH connection to the DUT and commanding it to 
read a pin value and return the result.
'''
class ReadDUT(object):

    def __init__(self, meas_assets, dut_name, test_id, sleep_time=1):
        self.dut_comms = meas_assets.dut_comms
        self.test_config = meas_assets.test_config
        self.dut_name = dut_name
        self.test_id = test_id
        self.sleep_time = sleep_time
        self._logger = get_logger(__file__)

    def run(self):
        '''
        First I need to get the info to open the SSH port to the DUT
        '''
        _name = self.dut_comms[self.dut_name]._name
        _ip = self.dut_comms[self.dut_name]._ip
        _user = self.dut_comms[self.dut_name]._user
        _passwd = self.dut_comms[self.dut_name]._passwd
        _debug = bool(self.dut_comms[self.dut_name]._debug)

        '''
        Now open the connection (SSH) to the DUT
        '''
        _dut = BCM(ip=_ip, user=_user, password=_passwd, debug=_debug)
        result = False
        value = 0

        # Verify the DUT is connected...
        if _dut.isConnected():

            self._logger.info("Connected...")
            cmd = self.test_config[self.test_id]._cmd
           

            # Call the Write command for the Pin and Bank provided to set the output
            if str(cmd) == 'R':
                '''
                Now that I have a connection gather the info needed to command the DUT to either
                drive a specified pin high or read the specified pin.
                '''
                pin = self.test_config[self.test_id]._pin
                bank = self.test_config[self.test_id]._bank
                func = self.test_config[self.test_id]._func
                arg = 0
                debug = bool(self.test_config[self.test_id]._debug)

                result, value = _dut.readPin(pin, bank.upper(), func, arg, debug)

            else:
                self._logger.error("%s:Cmd: %s NOT VALID for R", self.test_id, str(cmd))
                result, value = False, 0

            # If the DUT is connected then close the connection
            _dut._ssh.close()

        else:

            self._logger.error("NOT CONNECTED...")

        # Present the results
        if (result):
            self._logger.info("PASS %d", value)

        else:
            self._logger.error("FAIL")

        return result, value


'''
This functions (ReadDUT1) will open an SSH connection to the DUT and commanding it to 
read a pin value and return the result.
'''
class ReadADC(object):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''

    def __init__(self, meas_assets, dut_name, test_id, sleep_time=1):
        self.dut_comms = meas_assets.dut_comms
        self.test_config = meas_assets.test_config
        self.dut_name = dut_name
        self.test_id = test_id
        self.sleep_time = sleep_time
        self._logger = get_logger(__file__)

    def run(self):
        '''
        First I need to get the info to open the SSH port to the DUT
        '''
        _name = self.dut_comms[self.dut_name]._name
        _ip = self.dut_comms[self.dut_name]._ip
        _user = self.dut_comms[self.dut_name]._user
        _passwd = self.dut_comms[self.dut_name]._passwd
        _debug = bool(self.dut_comms[self.dut_name]._debug)

        '''
        Now open the connection (SSH) to the DUT
        '''
        _dut = BCM(ip=_ip, user=_user, password=_passwd, debug=_debug)
        result = False
        value = 0

        # Verify the DUT is connected...
        if _dut.isConnected():

            self._logger.info("Connected...")
            cmd = self.test_config[self.test_id]._cmd
           
            # Call the Write command for the Pin and Bank provided to set the output
            if str(cmd) == 'A':
                '''
                Now that I have a connection gather the info needed to command the DUT to either
                drive a specified pin high or read the specified pin.
                '''
                pin = self.test_config[self.test_id]._pin
                bank = self.test_config[self.test_id]._bank
                func = self.test_config[self.test_id]._func
                arg = 0
                debug = bool(self.test_config[self.test_id]._debug)

                result, value = _dut.readADC(pin, bank.upper(), func, arg, debug)

            else:
                self._logger.error("%s:Cmd: %s NOT VALID for A", self.test_id, str(cmd))
                result, value = False, 0

            # If the DUT is connected then close the connection
            _dut._ssh.close()

        else:

            self._logger.error("NOT CONNECTED...")

        # Present the results
        if (result):
            self._logger.info("PASS %d", value)

        else:
            self._logger.error("FAIL")

        return result, int(value)


'''
This functions (CheckUsb) will open an SSH connection to the DUT and commanding it to 
read a pin value and return the result.
'''
class USBverify(object):
    # Identify all the different types of USB devices we might find
    USB_STR = [\
        'SanDisk Corp. Cruzer Blade',\
        'STMicroelectronics',\
        'Realtek Semiconductor Corp.',\
        'ASIX Electronics Corp.',\
        'D-WAV Scientific Co.',\
       'Logitech, Inc. Unifying Receiver']

    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''

    def __init__(self, meas_assets, dut_name, sleep_time=1):
        self.dut_comms = meas_assets.dut_comms
        self.test_config = meas_assets.test_config
        self.dut_name = dut_name
        self.sleep_time = sleep_time
        self._logger = get_logger(__file__)

    def run(self):
        '''
        First I need to get the info to open the SSH port to the DUT
        '''
        _name = self.dut_comms[self.dut_name]._name
        _ip = self.dut_comms[self.dut_name]._ip
        _user = self.dut_comms[self.dut_name]._user
        _passwd = self.dut_comms[self.dut_name]._passwd
        _debug = bool(self.dut_comms[self.dut_name]._debug)

        '''
        Now open the connection (SSH) to the DUT
        '''
        _dut = BCM(ip=_ip, user=_user, password=_passwd, debug=_debug)
        result = False
        value = 0

        # Verify the DUT is connected...
        if _dut.isConnected():

            self._logger.info("Connected...")
           
            '''
            Now that I have a connection gather the info needed to command the DUT to either
            drive a specified pin high or read the specified pin.
            '''
            # Call the Read/Write command for the Pin and Bank provided
            result, value = _dut.readUSB(_debug)
            value = 0

            # Look for the USB devices that match the list and count
            for row in _dut._lines:
                for usb in self.USB_STR:
                    if usb in row:
                        value += 1

            # If the DUT is connected then close the connection
            _dut._ssh.close()

        else:

            self._logger.error("NOT CONNECTED...")

        # Present the results
        if (result):
            self._logger.info("PASS %d", value)

        else:
            self._logger.error("FAIL")

        return result, int(value)


class USBchkSum(object):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''

    def __init__(self, meas_assets, dut_name, test_id, sleep_time=1):
        self.dut_comms = meas_assets.dut_comms
        self.test_config = meas_assets.test_config
        self.test_id = test_id
        self.dut_name = dut_name
        self.sleep_time = sleep_time
        self._logger = get_logger(__file__)

    def run(self):
        '''
        First I need to get the info to open the SSH port to the DUT
        '''
        _name = self.dut_comms[self.dut_name]._name
        _ip = self.dut_comms[self.dut_name]._ip
        _user = self.dut_comms[self.dut_name]._user
        self._passwd = self.dut_comms[self.dut_name]._passwd
        _debug = bool(self.dut_comms[self.dut_name]._debug)

        '''
        Now open the connection (SSH) to the DUT
        '''
        _dut = BCM(ip=_ip, user=_user, password=self._passwd, debug=_debug)
        result = False
        value = 0

        # Verify the DUT is connected...
        if _dut.isConnected():

            self._logger.info("Connected...")
           
            '''
            Now that I have a connection gather the info needed to command the DUT to either
            drive a specified pin high or read the specified pin.
            '''
            _file = self.test_config[self.test_id]._bank
            _debug = bool(self.test_config[self.test_id]._debug)

            _dut.chksumUSB(file=_file, debug=_debug)

            # First verify the result string contains "PASS"
            for row in _dut._lines:
                if 'PASS' in row:
                    result = True
                else:
                    line = row.split()
                    value = int(line[0])

            # If the DUT is connected then close the connection
            _dut._ssh.close()

        else:

            self._logger.error("NOT CONNECTED...")

        # Present the results
        if result:
            self._logger.info("PASS %d", value)

        else:
            self._logger.error("FAIL")

        return result, int(value)

class USBperformance(object):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''

    def __init__(self, meas_assets, dut_name, test_id, sleep_time=1):
        self.dut_comms = meas_assets.dut_comms
        self.test_config = meas_assets.test_config
        self.test_id = test_id
        self.dut_name = dut_name
        self.sleep_time = sleep_time
        self._logger = get_logger(__file__)

    def run(self):
        '''
        First I need to get the info to open the SSH port to the DUT
        '''
        _name = self.dut_comms[self.dut_name]._name
        _ip = self.dut_comms[self.dut_name]._ip
        _user = self.dut_comms[self.dut_name]._user
        self._passwd = self.dut_comms[self.dut_name]._passwd
        _debug = bool(self.dut_comms[self.dut_name]._debug)

        '''
        Now open the connection (SSH) to the DUT
        '''
        _dut = BCM(ip=_ip, user=_user, password=self._passwd, debug=_debug)
        result = False
        value = 0.0

        # Verify the DUT is connected...
        if _dut.isConnected():

            self._logger.info("Connected...")
           
            '''
            Now that I have a connection gather the info needed to command the DUT to either
            drive a specified pin high or read the specified pin.
            '''
            _dev = self.test_config[self.test_id]._pin
            _ofile = self.test_config[self.test_id]._bank
            _debug = bool(self.test_config[self.test_id]._debug)

            # Call the Read/Write command for the Pin and Bank provided
            _dut.performanceUSB(indev=_dev, file=_ofile, passwd=self._passwd, debug=_debug)

            # First verify the result string contains "PASS"
            for row in _dut._lines:
                if 'PASS' in row:
                    result = True

            # Now get the performance data
            if result:
                for row in _dut._errors:
                    if 'copied' in row:
                        line = row.split()
                        value = float(line[7])

            # If the DUT is connected then close the connection
            _dut._ssh.close()

        else:

            self._logger.error("NOT CONNECTED...")

        # Present the results
        if result:
            self._logger.info("PASS %d", value)

        else:
            self._logger.error("FAIL")

        return result, float(value)


class ImuInterface(object):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''

    def __init__(self, meas_assets, dut_name, test_id, sleep_time=1):
        self.dut_comms = meas_assets.dut_comms
        self.test_config = meas_assets.test_config
        self.test_id = test_id
        self.dut_name = dut_name
        self.sleep_time = sleep_time
        self._logger = get_logger(__file__)

    def run(self):
        '''
        First I need to get the info to open the SSH port to the DUT
        '''
        _name = self.dut_comms[self.dut_name]._name
        _ip = self.dut_comms[self.dut_name]._ip
        _user = self.dut_comms[self.dut_name]._user
        _passwd = self.dut_comms[self.dut_name]._passwd
        _debug = bool(self.dut_comms[self.dut_name]._debug)

        '''
        Now open the connection (SSH) to the DUT
        '''
        _dut = BCM(ip=_ip, user=_user, password=_passwd, debug=_debug)
        result = False
        value = 0

        # Verify the DUT is connected...
        if _dut.isConnected():

            self._logger.info("Connected...")
           
            _dut.imuconfig(debug=_debug)

            # First verify the result string contains "PASS"
            for row in _dut._lines:
                if 'PASS' in row:
                    result = True
            
            # If the DUT is connected then close the connection
            _dut._ssh.close()

        else:

            self._logger.error("NOT CONNECTED...")

        # Present the results
        if result:
            self._logger.info("PASS %d", value)

        else:
            self._logger.error("FAIL")

        return result, value


class ImuGyroInterface(object):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''

    def __init__(self, meas_assets, dut_name, test_id, sleep_time=1):
        self.dut_comms = meas_assets.dut_comms
        self.test_config = meas_assets.test_config
        self.test_id = test_id
        self.dut_name = dut_name
        self.sleep_time = sleep_time
        self._logger = get_logger(__file__)

    def run(self):
        '''
        First I need to get the info to open the SSH port to the DUT
        '''
        _name = self.dut_comms[self.dut_name]._name
        _ip = self.dut_comms[self.dut_name]._ip
        _user = self.dut_comms[self.dut_name]._user
        _passwd = self.dut_comms[self.dut_name]._passwd
        _debug = bool(self.dut_comms[self.dut_name]._debug)

        '''
        Now open the connection (SSH) to the DUT
        '''
        _dut = BCM(ip=_ip, user=_user, password=_passwd, debug=_debug)
        result = False
        value = 0

        # Verify the DUT is connected...
        if _dut.isConnected():

            self._logger.info("Connected...")
           
            _dut.imuconfig(debug=_debug)

            # First verify the result string contains "PASS"
            for row in _dut._lines:
                if 'PASS' in row:
                    result = True
            
            # If the DUT is connected then close the connection
            _dut._ssh.close()

        else:

            self._logger.error("NOT CONNECTED...")

        # Present the results
        if result:
            self._logger.info("PASS %d", value)

        else:
            self._logger.error("FAIL")

        return result, value


class Ifconfig(object):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''

    def __init__(self, meas_assets, dut_name, test_id, host=None, sleep_time=1):
        self.dut_comms = meas_assets.dut_comms
        self.test_config = meas_assets.test_config
        self.test_id = test_id
        self.dut_name = dut_name
        self.sleep_time = sleep_time
        self.host = host
        self._logger = get_logger(__file__)

    def run(self):
        '''
        First I need to get the info to open the SSH port to the DUT
        '''
        _name = self.dut_comms[self.dut_name]._name
        _ip = self.dut_comms[self.dut_name]._ip
        _user = self.dut_comms[self.dut_name]._user
        _passwd = self.dut_comms[self.dut_name]._passwd
        _debug = bool(self.dut_comms[self.dut_name]._debug)

        '''
        Now open the connection (SSH) to the DUT
        '''
        _dut = BCM(ip=_ip, user=_user, password=_passwd, debug=_debug)
        result = False
        result1 = False
        result2 = False
        value = 0

        # Verify the DUT is connected...
        if _dut.isConnected():

            self._logger.info("Connected...")
           
            _dut.ifconfig(host=self.host, debug=_debug)

            host = self.test_config[self.test_id]._pin
            connection = self.test_config[self.test_id]._func

            # First verify the result string contains "PASS"
            for row in _dut._lines:
                if 'PASS' in row:
                    result1 = True

            # Verify the specified IP address is found
            if result1:
                for index, row in enumerate(_dut._lines):
                    words = str(row.split())
                    # Find the row with the connection name on it
                    if connection in words:
                        # The next row contains the ip addr so split that row into words
                        words = _dut._lines[index+1].split()
                        dontcare,ipAddr = words[1].split(':')

                        # Verify the IP addr matches
                        result = True if ipAddr in host else False

            # If the DUT is connected then close the connection
            _dut._ssh.close()

        else:

            self._logger.error("NOT CONNECTED...")

        # Present the results
        if result:
            value = 1
            self._logger.info("PASS %d", value)

        else:
            self._logger.error("FAIL")

        return result, value


class LidarPing(object):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''

    def __init__(self, meas_assets, dut_name, test_id, sleep_time=1):
        self.dut_comms = meas_assets.dut_comms
        self.test_config = meas_assets.test_config
        self.test_id = test_id
        self.dut_name = dut_name
        self.sleep_time = sleep_time
        self._logger = get_logger(__file__)

    def run(self):
        '''
        First I need to get the info to open the SSH port to the DUT
        '''
        _name = self.dut_comms[self.dut_name]._name
        _ip = self.dut_comms[self.dut_name]._ip
        _user = self.dut_comms[self.dut_name]._user
        _passwd = self.dut_comms[self.dut_name]._passwd
        _debug = bool(self.dut_comms[self.dut_name]._debug)
        _host = self.test_config[self.test_id]._pin

        '''
        Now open the connection (SSH) to the DUT
        '''
        _dut = BCM(ip=_ip, user=_user, password=_passwd, debug=_debug)
        result = False
        value = 0

        # Verify the DUT is connected...
        if _dut.isConnected():

            self._logger.info("Connected...")
           
            _dut.ifconfig(host=_host, debug=_debug)

            # First verify the result string contains "PASS"
            for row in _dut._lines:
                if 'PASS' in row:
                    result = True
            
            # If the DUT is connected then close the connection
            _dut._ssh.close()

        else:

            self._logger.error("NOT CONNECTED...")

        # Present the results
        if result:
            self._logger.info("PASS %d", value)

        else:
            self._logger.error("FAIL")

        return result, value


class BiosVerify(object):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''

    def __init__(self, meas_assets, dut_name, test_id, sleep_time=1):
        self.dut_comms = meas_assets.dut_comms
        self.test_config = meas_assets.test_config
        self.test_id = test_id
        self.dut_name = dut_name
        self.sleep_time = sleep_time
        self._logger = get_logger(__file__)

    def run(self):
        '''
        First I need to get the info to open the SSH port to the DUT
        '''
        _name = self.dut_comms[self.dut_name]._name
        _ip = self.dut_comms[self.dut_name]._ip
        _user = self.dut_comms[self.dut_name]._user
        _passwd = self.dut_comms[self.dut_name]._passwd
        _debug = bool(self.dut_comms[self.dut_name]._debug)

        '''
        Now open the connection (SSH) to the DUT
        '''
        _dut = BCM(ip=_ip, user=_user, password=_passwd, debug=_debug)
        result = False
        value = 0

        # Verify the DUT is connected...
        if _dut.isConnected():

            self._logger.info("Connected...")
           
            '''
            Now that I have a connection gather the info needed to command the DUT to either
            drive a specified pin high or read the specified pin.
            '''
            bios = self.test_config[self.test_id]._func
            _dut.biosverify(bios)

            # First verify the result string contains "PASS"
            for row in _dut._lines:
                if 'PASS' in row:
                    result = True
                    value = 1
            
            # If the DUT is connected then close the connection
            _dut._ssh.close()

        else:

            self._logger.error("NOT CONNECTED...")

        # Present the results
        if result:
            self._logger.info("PASS %d", value)

        else:
            self._logger.error("FAIL")

        return result, value



class Eeprogram(object):
    '''
    A Measurement is an operation with an associated set of test points.
    A measurement's purpose is to collect information from the DUT, fixture, and instruments
    then feed that information to test points.
    The Measurement method is executed when run() is called.
    See polish/measurement/measurement.py
    '''

    def __init__(self, meas_assets, dut_name, test_id, sleep_time=1):
        self.dut_comms = meas_assets.dut_comms
        self.test_config = meas_assets.test_config
        self.test_id = test_id
        self.dut_name = dut_name
        self.sleep_time = sleep_time
        self._logger = get_logger(__file__)

    def run(self):
        '''
        First I need to get the info to open the SSH port to the DUT
        '''
        _name = self.dut_comms[self.dut_name]._name
        _ip = self.dut_comms[self.dut_name]._ip
        _user = self.dut_comms[self.dut_name]._user
        _passwd = self.dut_comms[self.dut_name]._passwd
        _debug = bool(self.dut_comms[self.dut_name]._debug)

        '''
        Now open the connection (SSH) to the DUT
        '''
        _dut = BCM(ip=_ip, user=_user, password=_passwd, debug=_debug)
        result = False
        value = 0

        # Verify the DUT is connected...
        if _dut.isConnected():

            self._logger.info("Connected...")
           
            mac_addr = self.test_config[self.test_id]._func
            _dut.eeprogram(mac_addr, passwd=_passwd)

            # First verify the result string contains "PASS"
            for row in _dut._lines:
                if 'PASS' in row:
                    result = True
                    value = 1
            
            # If the DUT is connected then close the connection
            _dut._ssh.close()

        else:

            self._logger.error("NOT CONNECTED...")

        # Present the results
        if result:
            self._logger.info("PASS %d", value)

        else:
            self._logger.error("FAIL")

        return result, value



if __name__ == '__main__':

    myPin = int(sys.argv[1])            # Pin number must be first
    myBank = str(sys.argv[2])           # Pin bank must be second
    myFunc = int(sys.argv[3])           # Alt Func must be third
    myCmd = str(sys.argv[4])            # Read/Write Cmd must be forth
    myArg = 0
    myDebug = False

    # If this is a Write command then get the write value (it must be forth)        
    if (myCmd.upper() == 'W' and len(sys.argv) > 5):
        myArg = int(sys.argv[5])

        # Check if debug is requested
        if (len(sys.argv) > 6 and (str(sys.argv[6]) == 'D' or str(sys.argv[6]) == 'd')):
            myDebug = True

    # Check if debug is requested
    elif (len(sys.argv) > 5 and (str(sys.argv[5]) == 'D' or str(sys.argv[5]) == 'd')):
        myDebug = True

    # Init some locals
    myIP = BCM.IP_STR
    myUser = BCM.USER_STR
    myPasswd = BCM.PASSWD_STR
    
    # Create the Test instance and run it...
    myBCM = BCM(ip=myIP, user=myUser, password=myPasswd, debug=myDebug)

    # If the SSH connection was successfull
    if (myBCM.isConnected()):

        if (myDebug):
            print "INFO:Connected..."

        # Call the Read/Write command for the Pin and Bank provided
        if (myCmd.upper() == 'W'):
            result, value = myBCM.writePin(myPin, myBank.upper(), myFunc, myArg)
        else:
            result, value = myBCM.readPin(myPin, myBank.upper(), myFunc, myArg)

        # Present the results
        if (result):
            print "PASS", value

        else:
            print "FAIL", 0

    else:
        if (myDebug):
            print "ERROR:NOT CONNECTED..."
        print "FAIL", 0






