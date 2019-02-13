from xinput import *
import cozmo
from math import *
from cozmo.util import *

directional_pad_speeds = {
    # up, down, left, right
    GAMEPAD_DPAD_UP: (100, 100),
    GAMEPAD_DPAD_DOWN: (-100, -100),
    GAMEPAD_DPAD_LEFT: (0, 100),
    GAMEPAD_DPAD_RIGHT: (100, 0),
    # diagonals
    GAMEPAD_DPAD_UP | GAMEPAD_DPAD_LEFT: (50, 100),
    GAMEPAD_DPAD_UP | GAMEPAD_DPAD_RIGHT: (100, 50),
    GAMEPAD_DPAD_DOWN | GAMEPAD_DPAD_LEFT: (-50, -100),
    GAMEPAD_DPAD_DOWN | GAMEPAD_DPAD_RIGHT: (-100, -50),
}


def normalize_stick(x, y):
    """
    Normalize input values for left and right sticks
    :param x: x value generated by the controller
    :param y: y value generated by the controller
    :return: a tuple containing (normalized x, normalized_y, magnitude, normalized_magnitude)
    """
    # determine how far the controller is pushed
    magnitude = sqrt(x * x + y * y)
    # determine the direction the controller is pushed
    normalized_x, normalized_y = x / magnitude, y / magnitude
    normalized_magnitude = 0
    # check if the controller is outside a circular dead zone
    if magnitude > GAMEPAD_LEFT_THUMB_DEADZONE:
        magnitude = min([magnitude, GAMEPAD_THUMB_MAX])
        magnitude -= GAMEPAD_THUMB_MAX
        normalized_magnitude = magnitude / (GAMEPAD_THUMB_MAX - GAMEPAD_LEFT_THUMB_DEADZONE)
    else:
        magnitude = 0.0

    return normalized_x, normalized_y, magnitude, normalized_magnitude

def cozmo_program(robot: cozmo.robot.Robot):

    joysticks = XInputJoystick.enumerate_devices()

    if joysticks:
        print("Number of connected controllers: {0}".format(len(joysticks)))
    else:
        print("No controller is connected. Please connect xbox controller.")
        sys.exit(0)

    joystick = joysticks[0]

    def on_state_changed(state):

        # directional pad buttons
        state = struct_dict(state.gamepad)
        (left_speed, right_speed) = directional_pad_speeds.get(state['buttons'], (0, 0))
        robot.drive_wheels(left_speed, right_speed)

        # left stick
        left_x, left_y, left_magnitude, _   = normalize_stick(state['l_thumb_x'], state['l_thumb_y'])

        # right stick
        right_x, right_y, right_magnitude, _ = normalize_stick(state['r_thumb_x'], state['r_thumb_y'])

        print("left :{0}, {1}, {2}".format(left_x, left_y, left_magnitude))
        print("right:{0}, {1}, {2}".format(right_x, right_y, right_magnitude))

    joystick.on_state_changed = on_state_changed

    while True:
        joystick.dispatch_events()
        time.sleep(.01)


cozmo.run_program(cozmo_program)
