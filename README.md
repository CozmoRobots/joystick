# Cozmo Xbox One Controller Interface
## Overview
This is a Python project that allows a user to connect an Xbox One controller to a Windows PC and control a Cozmo robot
using that controller via the Cozmo SDK mode from a compatible mobile device.

## Installation
To run this project:

1. Clone this repository from the terminal with `git clone https://github.com/mudathirmahgoub/joystick.git` or download it into a zip file by clicking:
[link](https://github.com/mudathirmahgoub/joystick/archive/master.zip)
2. Navigate to the directory where you cloned the repo or unzipped the repository.
3. Install the required dependencies with `pip install -r requirements.txt`.
4. Execute `python xbox_controller.py` from the terminal to establish a connect to the robot from your mobile device and begin using the controller.

**Note: The driver used for this project is only compatible with Windows and therefore this interface will only work for Windows devices connected to an Xbox One controller.**

## Dependencies
* [Xbox Controller Module](https://github.com/r4dian/Xbox-360-Controller-for-Python)
* [Cozmo SDK](http://cozmosdk.anki.com/docs/)