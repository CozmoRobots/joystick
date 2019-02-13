from xinput import *
from xinput import XInputJoystick
import cozmo
from cozmo.util import *

def cozmo_program(robot: cozmo.robot.Robot):

    joysticks = XInputJoystick.enumerate_devices()

    if joysticks:
        print("Number of connected controllers: {0}".format(len(joysticks)))
    else:
        print("No controller is connected. Please connect xbox controller.")
        sys.exit(0)

    joystick = joysticks[0]

    def on_state_changed(state):

        state = struct_dict(state.gamepad)

        def switch_directional_pad(button):
            (left_speed, right_speed) = {
                GAMEPAD_DPAD_UP: (100, 100),
                GAMEPAD_DPAD_DOWN: (-100, -100),
                GAMEPAD_DPAD_LEFT: (0, 100),
                GAMEPAD_DPAD_RIGHT: (100, 0),
            }.get(button, (0, 0))    # 9 is default if x not found
            robot.drive_wheels(left_speed, right_speed)

        switch_directional_pad(state['buttons'])

    joystick.on_state_changed = on_state_changed

    while True:
        joystick.dispatch_events()
        time.sleep(.01)

cozmo.run_program(cozmo_program)