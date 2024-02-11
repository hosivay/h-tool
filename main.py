import random
import string
import requests
import os.path
import numpy as np
import cv2
import pyautogui
import subprocess
from gtts import gTTS


def print_intro():
    print("""

HH   HH        TTTTTTT               lll 
HH   HH          TTT    oooo   oooo  lll 
HHHHHHH _____    TTT   oo  oo oo  oo lll 
HH   HH          TTT   oo  oo oo  oo lll 
HH   HH          TTT    oooo   oooo  lll 

H-Tool - v1.0.0
""")


def display_menu():
    print("")
    print("1 - Generate Password")
    print("2 - File Downloader")
    print("3 - ScreenShot")
    print("4 - Text To Speech")
    print("5 - Wifi Password")
    print("8 - exit")
    print("")


def Texttospeech(text):
    tts = gTTS(text)
    tts.save(f'{text}.mp3')
    print("Saved")


def WifiPassword():
    print("")
    systemInfo = ''
    try:
        systemInfo = subprocess.check_output(['uname']).decode('utf-8', errors="backslashreplace").split('\n')
        systemInfo = systemInfo[0]
    except:
        pass
    if systemInfo == "Linux":
        wifiData = subprocess.check_output(['ls', '/etc/NetworkManager/system-connections']).decode('utf-8',
                                                                                                    errors="backslashreplace").split(
            '\n')
        print("Wifiname                       Password")
        print("----------------------------------------")

        for wifiname in wifiData:
            if wifiname != '':
                wifiPass = subprocess.check_output(
                    ['sudo', 'cat', f"/etc/NetworkManager/system-connections/{wifiname}"]).decode('utf-8',
                                                                                                  errors="backslashreplace").split(
                    '\n')
                password = wifiPass[15].strip("psk=");
                print("{:<30} {:<}".format(wifiname, password))
    else:
        wifi = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8',
                                                                                     errors="backslashreplace").split(
            '\n')
        profiles = [i.split(":")[1][1:-1] for i in wifi if "All User Profile" in i]
        for i in profiles:
            try:
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8',
                                                                                                               errors="backslashreplace").split(
                    '\n')
                results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                try:
                    print("{:<30}|  {:<}".format(i, results[0]))
                except:
                    print("{:<30}|  {:<}".format(i, ""))
            except:
                print("{:<30}|  {:<}".format(i, "ENCODING ERROR"))


def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    print(" ")
    print("password : {}".format(password))
    print(" ")


def download_file(url, save_dir):
    response = requests.get(url)
    if response.status_code == 200:
        # Extract file name from URL
        file_name = url.split('/')[-1]
        # Combine save directory and file name
        file_path = os.path.join(save_dir, file_name)

        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Download completed successfully. File saved as: {file_path}")
    else:
        print(f"Failed to download file from {url}. Status code: {response.status_code}")


def main():
    print_intro()

    exitapp = False
    while not exitapp:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            generate_password()

        elif choice == "2":
            linkurl = input("Link file ( example: https://example.com/file_to_download.txt ) : ")
            save_dir = input("Enter the directory where you want to save the file: ")
            download_file(linkurl, save_dir)
        elif choice == "3":
            image = pyautogui.screenshot()
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imwrite("screenshot.png", image)
            print("Saved ScreenShot")
        elif choice == "4":
            linkurl = input("Text : ")
            Texttospeech(linkurl)
        elif choice == "5":
            WifiPassword()
        elif choice == "8":
            exitapp = True
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
