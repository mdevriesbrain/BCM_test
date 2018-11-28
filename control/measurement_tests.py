
from tests.bcm_analog_tests import A4_20MaIn1AnalogInput, A4_20MaIn2AnalogInput, AnalogInputMeasurement
from tests.bcm_digital_tests import DigitalInputMeasurement, DigitalOutputMeasurement, DigitalOutputMeasurement0
from tests.bcm_digital_tests import DigitalEstop1Measurement, DigitalEstop2Measurement, DigitalEstop3Measurement, DigitalEstop4Measurement
from tests.bcm_usb_tests import DUTUsbVerify, DUTUsbChkSum, DUTUsbPerformance
from tests.bcm_power_tests import DutKeySenseMeasurement
from tests.bcm_misc import DUTEthVerify, DUTEthPing, DUTLidarPing, DUTImuVerify, DUTImuGyroVerify, DUTBiosVerify, DUTEeprogram

def measurement_tests(meas_assets):

    # Define all the BCM Automated tests
    measurements_list = \
    [
        # First verify the Key-sensevoltage
        DutKeySenseMeasurement(meas_assets, 'DUT1', 'POWER_SUPPLY1', 'MUX2', 'KEY_SENSE_2', slot=2, channel=2, bit=1),

        # Update the DUT Mac address (all 8)
        #Y DUTEeprogram(meas_assets, 'DUT1', 'EEPROM_1'),

        # Verify the DUT Bios string
        DUTBiosVerify(meas_assets, 'DUT1', 'BIOS_1'),

        # This test will verify the existence of USB devices on the DUT
        DUTUsbVerify(meas_assets, 'DUT1', 'USB_VERIFY_1'),

        #The USB Performance tests MUST be run before the USB Chksum test because
        #the performance test is generating the file used by chksum.

        # These tests will verify the performance on each USB device
        #Y DUTUsbPerformance(meas_assets, 'DUT1', 'USB_PERFORM_1'),
        #Y DUTUsbPerformance(meas_assets, 'DUT1', 'USB_PERFORM_2'),
        #Y DUTUsbPerformance(meas_assets, 'DUT1', 'USB_PERFORM_3'),
        #Y DUTUsbPerformance(meas_assets, 'DUT1', 'USB_PERFORM_4'),
        #Y DUTUsbPerformance(meas_assets, 'DUT1', 'USB_PERFORM_5'),

        # These tests will verify the chksum on each USB device
        #Y DUTUsbChkSum(meas_assets, 'DUT1', 'USB_CKSUM_1'),
        #Y DUTUsbChkSum(meas_assets, 'DUT1', 'USB_CKSUM_2'),
        #Y DUTUsbChkSum(meas_assets, 'DUT1', 'USB_CKSUM_3'),
        #Y DUTUsbChkSum(meas_assets, 'DUT1', 'USB_CKSUM_4'),
        #Y DUTUsbChkSum(meas_assets, 'DUT1', 'USB_CKSUM_5'),

        # This test will verify the IMU/Gyro output on the DUT
        DUTImuVerify(meas_assets, 'DUT1', 'IMU_1'),
        DUTImuGyroVerify(meas_assets, 'DUT1', 'IMU_GYRO_1'),

        # These tests will verify ('ifconfig' on the DUT) the DUT IP Addresses
        DUTEthVerify(meas_assets, 'DUT1', 'FRONT_IFM_1'),
        DUTEthVerify(meas_assets, 'DUT1', 'RIGHT_IFM_1'),
        DUTEthVerify(meas_assets, 'DUT1', 'LEFT_IFM_1'),
        DUTEthVerify(meas_assets, 'DUT1', 'SWITCH_1'),
        DUTEthVerify(meas_assets, 'DUT1', 'SERVICE_1'),
        
        # These tests will 'ping' the DUT IP Addresses from the Test PC to verify they are active
        DUTEthPing(meas_assets, 'DUT1', 'FRONT_IFM_2'),
        DUTEthPing(meas_assets, 'DUT1', 'RIGHT_IFM_2'),
        DUTEthPing(meas_assets, 'DUT1', 'LEFT_IFM_2'),
        DUTEthPing(meas_assets, 'DUT1', 'SWITCH_2'),
        DUTEthPing(meas_assets, 'DUT1', 'SERVICE_2'),

        # These tests will 'ping' the USB/E-net adaptor from the DUT to verify the service line is active
        DUTLidarPing(meas_assets, 'DUT1', 'PL_LIDAR_1'),
        DUTLidarPing(meas_assets, 'DUT1', 'SL_LIDAR_1'),
        
        #
        # Verify the DUT Analog Input Tests (34903A - slot1, 34907A - slot2)
        #
        A4_20MaIn1AnalogInput(meas_assets, 'DUT1', '_4_20MA_IN_1_1', 'MUX2', voltage=0.3, slot1=1, ch1=1, slot2=2, ch2=4),
        A4_20MaIn1AnalogInput(meas_assets, 'DUT1', '_4_20MA_IN_1_2', 'MUX2', voltage=1.5, slot1=1, ch1=1, slot2=2, ch2=4),
        A4_20MaIn1AnalogInput(meas_assets, 'DUT1', '_4_20MA_IN_2_1', 'MUX2', voltage=0.3, slot1=1, ch1=1, slot2=2, ch2=4),
        A4_20MaIn2AnalogInput(meas_assets, 'DUT1', '_4_20MA_IN_2_2', 'MUX2', voltage=1.5, slot1=1, ch1=1, slot2=2, ch2=4),
        AnalogInputMeasurement(meas_assets, 'DUT1', 'STER_CUR_1', 'MUX2', voltage=-5, slot=2, channel=5),
        AnalogInputMeasurement(meas_assets, 'DUT1', 'STER_CUR_2', 'MUX2', voltage=5, slot=2, channel=5),

        # Define the DUT Digital Input Tests, MUX2, Slot2 (34907A), Channel1, bits 0-7
        DigitalInputMeasurement(meas_assets, 'DUT1', 'ENCODER1_ACH_MINUS_1', 'MUX2', slot=2, channel=1, bit=0),
        DigitalInputMeasurement(meas_assets, 'DUT1', 'ENCODER1_ACH_PLUS_1', 'MUX2', slot=2, channel=1, bit=1),
        DigitalInputMeasurement(meas_assets, 'DUT1', 'ENCODER1_BCH_MINUS_1', 'MUX2', slot=2, channel=1, bit=2),
        DigitalInputMeasurement(meas_assets, 'DUT1', 'ENCODER1_BCH_PLUS_1', 'MUX2', slot=2, channel=1, bit=3),
        DigitalInputMeasurement(meas_assets, 'DUT1', 'ENCODER2_ACH_MINUS_1', 'MUX2', slot=2, channel=1, bit=4),
        DigitalInputMeasurement(meas_assets, 'DUT1', 'ENCODER2_ACH_PLUS_1', 'MUX2', slot=2, channel=1, bit=5),
        DigitalInputMeasurement(meas_assets, 'DUT1', 'ENCODER2_BCH_MINUS_1', 'MUX2', slot=2, channel=1, bit=6),
        DigitalInputMeasurement(meas_assets, 'DUT1', 'ENCODER2_BCH_PLUS_1', 'MUX2', slot=2, channel=1, bit=7),
        
        # Define the DUT Digital Input Tests, MUX2, Slot2 (34907A), Channel2, bits 2-4
        DigitalInputMeasurement(meas_assets, 'DUT1', 'ABSOLUTE_ENC_SPI_MISO_MINUS_1', 'MUX2', slot=2, channel=2, bit=2),
        DigitalInputMeasurement(meas_assets, 'DUT1', 'ABSOLUTE_ENC_SPI_MISO_PLUS_1', 'MUX2', slot=2, channel=2, bit=3),
        DigitalInputMeasurement(meas_assets, 'DUT1', 'STER_FLT_1', 'MUX2', slot=2, channel=2, bit=4),

        # These are special case Digital Output Tests (using both the 34907A & 34908A)
        DigitalEstop1Measurement(meas_assets, 'DUT1', 'ESTOP1_OUT_1', 'MUX2', slot1=2, channel1=2, bit1=0, slot2=3, channel2=5),
        DigitalEstop2Measurement(meas_assets, 'DUT1', 'ESTOP1_OUT_2', 'MUX2', slot1=2, channel1=2, bit1=0, slot2=3, channel2=5),
        DigitalEstop3Measurement(meas_assets, 'DUT1', 'ESTOP1_OUT_3', 'MUX2', slot1=2, channel1=2, bit1=1, slot2=3, channel2=5),
        DigitalEstop4Measurement(meas_assets, 'DUT1', 'ESTOP1_OUT_4', 'MUX2', slot1=2, channel1=2, bit1=1, slot2=3, channel2=5),

        #
        # Verify the DUT Digital Output Tests (34908A)
        #
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'C_ANH_1', 'MUX2', slot=3, channel=1),
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'C_ANH_2', 'MUX2', slot=3, channel=2),
        DigitalOutputMeasurement0(meas_assets, 'DUT1', 'C_ANL_1', 'MUX2', slot=3, channel=3),
        DigitalOutputMeasurement0(meas_assets, 'DUT1', 'C_ANL_2', 'MUX2', slot=3, channel=4),
        #LCD DigitalOutputMeasurement(meas_assets, 'DUT1', 'LVDS_BL_CTL_1', 'MUX2', slot=3, channel=6),
        #LCD DigitalOutputMeasurement(meas_assets, 'DUT1', 'LVDS_BL_EN_1', 'MUX2', slot=3, channel=7),
        #FUTURE DigitalOutputMeasurement(meas_assets, 'DUT1', 'MCU_I2C_SCL_1', 'MUX2', slot=3, channel=8),
        #FUTURE DigitalOutputMeasurement(meas_assets, 'DUT1', 'MCU_I2C_SDA_1', 'MUX2', slot=3, channel=9),
        
        # This test should be a Load test because the is NO setup required on the DUT for this test to run
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'MASTER_POWER_OUT_1', 'MUX2', slot=3, channel=10),
        
        # Positive test
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'RLAY12_1_MINUS_1', 'MUX2', slot=3, channel=11),
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'RLAY12_1_PLUS_1', 'MUX2', slot=3, channel=12),
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'RLAY12_2_MINUS_1', 'MUX2', slot=3, channel=13),
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'RLAY12_2_PLUS_1', 'MUX2', slot=3, channel=14),

        # Negative test
        DigitalOutputMeasurement0(meas_assets, 'DUT1', 'RLAY12_1_MINUS_2', 'MUX2', slot=3, channel=11),
        DigitalOutputMeasurement0(meas_assets, 'DUT1', 'RLAY12_1_PLUS_2', 'MUX2', slot=3, channel=12),
        DigitalOutputMeasurement0(meas_assets, 'DUT1', 'RLAY12_2_MINUS_2', 'MUX2', slot=3, channel=13),
        DigitalOutputMeasurement0(meas_assets, 'DUT1', 'RLAY12_2_PLUS_2', 'MUX2', slot=3, channel=14),

        # Positive test
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'RLAY24_1_MINUS_1', 'MUX2', slot=3, channel=15),
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'RLAY24_1_PLUS_1', 'MUX2', slot=3, channel=16),
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'RLAY24_2_MINUS_1', 'MUX2', slot=3, channel=17),
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'RLAY24_2_PLUS_1', 'MUX2', slot=3, channel=18),
        
        # Negative test
        DigitalOutputMeasurement0(meas_assets, 'DUT1', 'RLAY24_1_MINUS_2', 'MUX2', slot=3, channel=15),
        DigitalOutputMeasurement0(meas_assets, 'DUT1', 'RLAY24_1_PLUS_2', 'MUX2', slot=3, channel=16),
        DigitalOutputMeasurement0(meas_assets, 'DUT1', 'RLAY24_2_MINUS_2', 'MUX2', slot=3, channel=17),
        DigitalOutputMeasurement0(meas_assets, 'DUT1', 'RLAY24_2_PLUS_2', 'MUX2', slot=3, channel=18),

        DigitalOutputMeasurement0(meas_assets, 'DUT1', 'ABSOLUTE_ENC_SPI_CLK_MINUS_1', 'MUX2', slot=3, channel=19),
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'ABSOLUTE_ENC_SPI_CLK_MINUS_2', 'MUX2', slot=3, channel=19),
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'ABSOLUTE_ENC_SPI_CLK_PLUS_1', 'MUX2', slot=3, channel=20),
        DigitalOutputMeasurement0(meas_assets, 'DUT1', 'ABSOLUTE_ENC_SPI_CLK_PLUS_2', 'MUX2', slot=3, channel=20),
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'STER_PWMA_1', 'MUX2', slot=3, channel=21),
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'STER_ENA_1', 'MUX2', slot=3, channel=22),
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'STER_MTR_DIS_1', 'MUX2', slot=3, channel=23),
        DigitalOutputMeasurement(meas_assets, 'DUT1', 'STER_PWMB_1', 'MUX2', slot=3, channel=24),

        #FUTURE DigitalOutputMeasurement(meas_assets, 'DUT1', 'USBEX_3N_1', 'MUX2', slot=3, channel=25),
        #FUTURE DigitalOutputMeasurement(meas_assets, 'DUT1', 'USBEX_3P_1', 'MUX2', slot=3, channel=26),
        #FUTURE DigitalOutputMeasurement(meas_assets, 'DUT1', 'USBEX_4N_1', 'MUX2', slot=3, channel=27),
        #FUTURE DigitalOutputMeasurement(meas_assets, 'DUT1', 'USBEX_4P_1', 'MUX2', slot=3, channel=28),
    ]

    # Set the initial test count
    testCount = 0

    # Now run the DUT Digital and Analog tests
    for meas in measurements_list:
        testCount += 1
        meas.run()
    
    #print "Measurement Tests:%d" % (testCount)
    return testCount
