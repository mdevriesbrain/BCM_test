from tests.bcm_power_tests import DutCurrentMeasurement, DutVoltageMeasurement
from tests.bcm_load_tests import LoadMeasurement

def test_20v_load(meas_assets):

    # Define the BCM Load tests for 20v (this set of tests are run first)
    list_20v_load = \
    [
        #
        # First Verify the Power Supply output to the DUT
        #
        DutCurrentMeasurement(meas_assets, 'DUT_CURRENT_1', 'POWER_SUPPLY1'),
        DutVoltageMeasurement(meas_assets, 'DUT_VOLTAGE_1', 'POWER_SUPPLY1'),

        #
        # Verify the DUT Load Tests
        #

        #
        # NOTE: The order of the cards is Multi1 is slot2, Multi2 is slot1
        #

        # Define the Mux 1 Slot 1 (34901A) tests first for 20v supply
        LoadMeasurement(meas_assets, 'P5VG_1', 'MUX1', slot=1, channel=1),
        LoadMeasurement(meas_assets, 'STEERING_P5VH_1', 'MUX1', slot=1, channel=2),
        LoadMeasurement(meas_assets, 'ABSOLUTE_ENCODER_P5VI_1', 'MUX1', slot=1, channel=3),
        LoadMeasurement(meas_assets, 'TRACTION_ENCODER_P5VJ_1', 'MUX1', slot=1, channel=4),
        LoadMeasurement(meas_assets, 'P5VK_1', 'MUX1', slot=1, channel=5),
        #LCD LoadMeasurement(meas_assets, 'TOUCH_PANEL_P5VL_1', 'MUX1', slot=1, channel=6),
        LoadMeasurement(meas_assets, 'EXT_LTE_MODEM__USB_5V_1A_1', 'MUX1', slot=1, channel=7),
        LoadMeasurement(meas_assets, 'USB_5V_1B_1', 'MUX1', slot=1, channel=8),

        # Now define Mux 1 the Slot 2 (34901A) tests for 20v supply
        LoadMeasurement(meas_assets, 'FAN_P12VA_1', 'MUX1', slot=2, channel=1),
        LoadMeasurement(meas_assets, 'SLANTED_LIDAR_P12VB_1', 'MUX1', slot=2, channel=2),
        LoadMeasurement(meas_assets, 'P12VC_1', 'MUX1', slot=2, channel=3),
        LoadMeasurement(meas_assets, 'H_LIDAR_P12VD_1', 'MUX1', slot=2, channel=4),
        #LCD LoadMeasurement(meas_assets, 'LCD_POWER_P12VE_1', 'MUX1', slot=2, channel=5),
        LoadMeasurement(meas_assets, 'P24VA_1', 'MUX1', slot=2, channel=6),
        LoadMeasurement(meas_assets, 'IFM_RIGHT_P24VB_1', 'MUX1', slot=2, channel=7),
        LoadMeasurement(meas_assets, 'IFM_FRONT_P24VC_1', 'MUX1', slot=2, channel=8),
        LoadMeasurement(meas_assets, 'IFM_LEFT_P24VD_1', 'MUX1', slot=2, channel=9),
        LoadMeasurement(meas_assets, 'STEERING_3V_P3V3A_1', 'MUX1', slot=2, channel=10),
        LoadMeasurement(meas_assets, 'STRT_PAUSE_P3V3B_1', 'MUX1', slot=2, channel=11),
        #LCD LoadMeasurement(meas_assets, 'DISPLAY_P3V3C_1', 'MUX1', slot=2, channel=12),
        LoadMeasurement(meas_assets, 'FRONT_CAM_P5VA_1', 'MUX1', slot=2, channel=13),
        LoadMeasurement(meas_assets, 'RIGHT_CAM_P5VB_1', 'MUX1', slot=2, channel=14),
        LoadMeasurement(meas_assets, 'LEFT_CAM_P5VC_1', 'MUX1', slot=2, channel=15),
        LoadMeasurement(meas_assets, 'P5VD_1', 'MUX1', slot=2, channel=16),
        LoadMeasurement(meas_assets, 'P5VE_1', 'MUX1', slot=2, channel=17),
        LoadMeasurement(meas_assets, 'P5VF_1', 'MUX1', slot=2, channel=18),
    ]

    # Set the initial test count
    testCount = 0

    # Now run the 20v Load tests
    for meas in list_20v_load:
        testCount += 1
        meas.run()
    
    return testCount


def test_36v_load(meas_assets):

    # Define the BCM Load tests for 36v (this test is run second after the 20v tests)
    list_36v_load = \
    [
        #
        # First Verify the Power Supply output to the DUT
        #
        DutCurrentMeasurement(meas_assets, 'DUT_CURRENT_2', 'POWER_SUPPLY1'),
        DutVoltageMeasurement(meas_assets, 'DUT_VOLTAGE_2', 'POWER_SUPPLY1'),

        #
        # Verify the DUT Load Tests
        #

        #
        # NOTE: The order of the cards is Multi1 is slot2, Multi2 is slot1
        #

        # Define the Mux 1 Slot 1 (34901A) tests first for 36v supply
        LoadMeasurement(meas_assets, 'P5VG_2', 'MUX1', slot=1, channel=1),
        LoadMeasurement(meas_assets, 'STEERING_P5VH_2', 'MUX1', slot=1, channel=2),
        LoadMeasurement(meas_assets, 'ABSOLUTE_ENCODER_P5VI_2', 'MUX1', slot=1, channel=3),
        LoadMeasurement(meas_assets, 'TRACTION_ENCODER_P5VJ_2', 'MUX1', slot=1, channel=4),
        LoadMeasurement(meas_assets, 'P5VK_2', 'MUX1', slot=1, channel=5),
        #LCD LoadMeasurement(meas_assets, 'TOUCH_PANEL_P5VL_2', 'MUX1', slot=1, channel=6),
        LoadMeasurement(meas_assets, 'EXT_LTE_MODEM__USB_5V_1A_2', 'MUX1', slot=1, channel=7),
        LoadMeasurement(meas_assets, 'USB_5V_1B_2', 'MUX1', slot=1, channel=8),
        
        # Now define Mux 1 the Slot 2 (34901A) tests for 36v supply
        LoadMeasurement(meas_assets, 'FAN_P12VA_2', 'MUX1', slot=2, channel=1),
        LoadMeasurement(meas_assets, 'SLANTED_LIDAR_P12VB_2', 'MUX1', slot=2, channel=2),
        LoadMeasurement(meas_assets, 'P12VC_2', 'MUX1', slot=2, channel=3),
        LoadMeasurement(meas_assets, 'H_LIDAR_P12VD_2', 'MUX1', slot=2, channel=4),
        #LCD LoadMeasurement(meas_assets, 'LCD_POWER_P12VE_2', 'MUX1', slot=2, channel=5),
        LoadMeasurement(meas_assets, 'P24VA_2', 'MUX1', slot=2, channel=6),
        LoadMeasurement(meas_assets, 'IFM_RIGHT_P24VB_2', 'MUX1', slot=2, channel=7),
        LoadMeasurement(meas_assets, 'IFM_FRONT_P24VC_2', 'MUX1', slot=2, channel=8),
        LoadMeasurement(meas_assets, 'IFM_LEFT_P24VD_2', 'MUX1', slot=2, channel=9),
        LoadMeasurement(meas_assets, 'STEERING_3V_P3V3A_2', 'MUX1', slot=2, channel=10),
        LoadMeasurement(meas_assets, 'STRT_PAUSE_P3V3B_2', 'MUX1', slot=2, channel=11),
        #LCD LoadMeasurement(meas_assets, 'DISPLAY_P3V3C_2', 'MUX1', slot=2, channel=12),
        LoadMeasurement(meas_assets, 'FRONT_CAM_P5VA_2', 'MUX1', slot=2, channel=13),
        LoadMeasurement(meas_assets, 'RIGHT_CAM_P5VB_2', 'MUX1', slot=2, channel=14),
        LoadMeasurement(meas_assets, 'LEFT_CAM_P5VC_2', 'MUX1', slot=2, channel=15),
        LoadMeasurement(meas_assets, 'P5VD_2', 'MUX1', slot=2, channel=16),
        LoadMeasurement(meas_assets, 'P5VE_2', 'MUX1', slot=2, channel=17),
        LoadMeasurement(meas_assets, 'P5VF_2', 'MUX1', slot=2, channel=18),
    ]

    # Set the initial test count
    testCount = 0

    # Now run the 36v Load tests
    for meas in list_36v_load:
        testCount += 1
        meas.run()
    
    return testCount


def test_24v_load(meas_assets):

    # Define the BCM Load tests for 24v (this set of tests is run third after the 20v & 36v tests)
    list_24v_load = \
    [
        #
        # First Verify the Power Supply output to the DUT
        #
        DutCurrentMeasurement(meas_assets, 'DUT_CURRENT_3', 'POWER_SUPPLY1'),
        DutVoltageMeasurement(meas_assets, 'DUT_VOLTAGE_3', 'POWER_SUPPLY1'),

        #
        # Verify the DUT Load Tests
        #

        #
        # NOTE: The order of the cards is Multi1 is slot2, Multi2 is slot1
        #

        # Define the Mux 1 Slot 1 (34901A) tests first for 24v supply
        LoadMeasurement(meas_assets, 'P5VG_3', 'MUX1', slot=1, channel=1),
        LoadMeasurement(meas_assets, 'STEERING_P5VH_3', 'MUX1', slot=1, channel=2),
        LoadMeasurement(meas_assets, 'ABSOLUTE_ENCODER_P5VI_3', 'MUX1', slot=1, channel=3),
        LoadMeasurement(meas_assets, 'TRACTION_ENCODER_P5VJ_3', 'MUX1', slot=1, channel=4),
        LoadMeasurement(meas_assets, 'P5VK_3', 'MUX1', slot=1, channel=5),
        #LCD LoadMeasurement(meas_assets, 'TOUCH_PANEL_P5VL_3', 'MUX1', slot=1, channel=6),
        LoadMeasurement(meas_assets, 'EXT_LTE_MODEM__USB_5V_1A_3', 'MUX1', slot=1, channel=7),
        LoadMeasurement(meas_assets, 'USB_5V_1B_3', 'MUX1', slot=1, channel=8),

        # Now define Mux 1 the Slot 2 (34901A) tests for 24v supply
        LoadMeasurement(meas_assets, 'FAN_P12VA_3', 'MUX1', slot=2, channel=1),
        LoadMeasurement(meas_assets, 'SLANTED_LIDAR_P12VB_3', 'MUX1', slot=2, channel=2),
        LoadMeasurement(meas_assets, 'P12VC_3', 'MUX1', slot=2, channel=3),
        LoadMeasurement(meas_assets, 'H_LIDAR_P12VD_3', 'MUX1', slot=2, channel=4),
        #LCD LoadMeasurement(meas_assets, 'LCD_POWER_P12VE_3', 'MUX1', slot=2, channel=5),
        LoadMeasurement(meas_assets, 'P24VA_3', 'MUX1', slot=2, channel=6),
        LoadMeasurement(meas_assets, 'IFM_RIGHT_P24VB_3', 'MUX1', slot=2, channel=7),
        LoadMeasurement(meas_assets, 'IFM_FRONT_P24VC_3', 'MUX1', slot=2, channel=8),
        LoadMeasurement(meas_assets, 'IFM_LEFT_P24VD_3', 'MUX1', slot=2, channel=9),
        LoadMeasurement(meas_assets, 'STEERING_3V_P3V3A_3', 'MUX1', slot=2, channel=10),
        LoadMeasurement(meas_assets, 'STRT_PAUSE_P3V3B_3', 'MUX1', slot=2, channel=11),
        #LCD LoadMeasurement(meas_assets, 'DISPLAY_P3V3C_3', 'MUX1', slot=2, channel=12),
        LoadMeasurement(meas_assets, 'FRONT_CAM_P5VA_3', 'MUX1', slot=2, channel=13),
        LoadMeasurement(meas_assets, 'RIGHT_CAM_P5VB_3', 'MUX1', slot=2, channel=14),
        LoadMeasurement(meas_assets, 'LEFT_CAM_P5VC_3', 'MUX1', slot=2, channel=15),
        LoadMeasurement(meas_assets, 'P5VD_3', 'MUX1', slot=2, channel=16),
        LoadMeasurement(meas_assets, 'P5VE_3', 'MUX1', slot=2, channel=17),
        LoadMeasurement(meas_assets, 'P5VF_3', 'MUX1', slot=2, channel=18),
    ]

    # Set the initial test count
    testCount = 0

    # Now run the 24v Load tests
    for meas in list_24v_load:
        testCount += 1
        meas.run()
    
    return testCount


