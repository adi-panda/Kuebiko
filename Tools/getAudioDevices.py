import speech_recognition as sr
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #It just works

import settings

def get_microphone_devices():
    devices = sr.Microphone.list_microphone_names()
    print("Available microphone devices:")
    with open("microphone_devices.txt", "w") as file:
        for i, device in enumerate(devices):
            print(f"{(i-1)+1}. {device}")
            file.write(f"{(i-1)+1}. {device}\n")
    print("Microphone devices list has been written to 'microphone_devices.txt'")

    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=int(settings.useDeviceID))
    print("Current Audio device:", microphone.list_microphone_names()[int(settings.useDeviceID)])
    return devices

# Call the function to get microphone devices
get_microphone_devices()
