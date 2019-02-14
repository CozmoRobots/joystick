import cozmo
import socket
from socket import error as socket_error
from cozmo.util import degrees, distance_mm, speed_mmps
from cozmo.robot import MIN_HEAD_ANGLE, MAX_HEAD_ANGLE, MIN_LIFT_HEIGHT, MAX_LIFT_HEIGHT

def parse_message(message):
    """
    Converts a message of the form "name;char1;char2;x;y" into a list [name, char1, char2, x, y]
    where x, y are integers, or a message of the form "name;head_value;tractor_value" into a list of
    [name,head_value,tractor_value] where head_value and tractor_value are floating numbers
    Raises:
        ValueError: If message is not a valid form
    :param message: a string of the form 'name;char1;char2;x;y' or 'name;head_value;tractor_value
    :return: a list of 5 elements [name, char1, char2, x, y] or 3 elements [name,head_value,tractor_value]
    """
    parts = message.split(';')
    # validate message size
    if len(parts) not in [3, 5]:
        raise ValueError("The message {0} should contain 5 parts separated by semicolons".format(message))

    if len(parts) == 5:
        name, char1, char2, x, y = parts

        # validate char1
        if char1 not in ['F', 'B']:
            raise ValueError("char1 {0} should either be 'F' or 'B'".format(char1))

        # validate char2
        if char2 not in ['L', 'R']:
            raise ValueError("char2 {0} should either be 'L' or 'R'".format(char2))

        # validate x
        try:
            x = int(x)
        except ValueError:
            raise ValueError("Invalid x value: '{0}'".format(x))

        # validate y
        try:
            y = int(y)
        except ValueError:
            raise ValueError("Invalid y value: '{0}'".format(y))

        return [name, char1, char2, x, y]
    else:
        name, head_value, tractor_value = parts
        # validate head_value
        try:
            head_value = float(head_value)
        except ValueError:
            raise ValueError("Invalid head value value: '{0}'".format(head_value))

        # validate tractor_value
        try:
            tractor_value = float(tractor_value)
        except ValueError:
            raise ValueError("Invalid tractor value: '{0}'".format(tractor_value))

        return [name, head_value, tractor_value]


def cozmo_program(robot: cozmo.robot.Robot):

    client_socket = None
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket_error as msg:
        robot.say_text("socket failed" + str(msg)).wait_for_completed()
        quit()

    # ip = "10.0.1.10"
    ip = "127.0.0.1"
    port = 5000
    
    try:
        client_socket.connect((ip, port))
    except socket_error:
        robot.say_text("socket failed to bind").wait_for_completed()
        quit()

    connected = True
    # robot.say_text("ready").wait_for_completed()
    
    # set cozmo name
    cozmo_name = 'CozmoName'
    # robot.say_text(cozmo_name, duration_scalar=0.5).wait_for_completed()
    while connected:
        byte_data = client_socket.recv(4048)
        message = byte_data.decode('utf-8')
        if not message:
            connected = False
            client_socket.close()
            quit()
        else:
            print(message)
            if len(message.split(';')) not in [3, 5]:
                continue
            instructions = parse_message(message)
            # check the name:
            if instructions[0] == cozmo_name:
                print(instructions)
                if len(instructions) == 5:
                    # we know that this is a message involving movement
                    _, char1, char2, x, y = instructions
                    # next, we will want to move forward or backward, if the x distance is not 0
                    if x != 0:
                        # first, just move if 'F' and turn 180 degrees for 'B'
                        if char1 == 'B':
                            robot.turn_in_place(degrees(180)).wait_for_completed()
                        robot.drive_straight(distance_mm(x), speed_mmps(150), False).wait_for_completed()

                    # then, we will want to turn left or right, if the y distance is not 0
                    if y != 0:
                        if char2 == 'L':
                            robot.turn_in_place(degrees(90)).wait_for_completed()
                        else:
                            robot.turn_in_place(degrees(-90)).wait_for_completed()
                        robot.drive_straight(distance_mm(y), speed_mmps(150), False).wait_for_completed()

                elif len(instructions) == 3:
                    # this is where we move the tractor or the head
                    _, head_value, tractor_value = instructions

                    # set the head angle
                    if MIN_HEAD_ANGLE <= degrees(head_value) <= MAX_HEAD_ANGLE:
                        head_action = robot.set_head_angle(degrees(head_value))
                    else:
                        print("Head angle {0} should be between {1} and {2}"
                              .format(degrees(head_value), MIN_HEAD_ANGLE, MAX_HEAD_ANGLE))

                    # set the lift height
                    if 0 <= tractor_value <= 1:
                        lift_action = robot.set_lift_height(tractor_value, in_parallel=True)
                    else:
                        print("Lift height {0} should be between {1} and {2}"
                              .format(tractor_value, 0, 1))

                    if head_action:
                        head_action.wait_for_completed()
                    if lift_action:
                        lift_action.wait_for_completed()

                client_socket.sendall(b"Done")


cozmo.run_program(cozmo_program)
