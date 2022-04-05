# Advanced Keylogger with Webcam and Microphone Spy
Advanced Keylogger in Python with screenshot, microphone, webcam pictures taking capabilities and also Collects Network/Wifi Info, System Info, Clipbaord Data, Browser History and then send these files through email.

## Installation & Running of this Keylogger
1. [Download Python](https://www.python.org/downloads/) and [Install](https://www.w3schools.in/python-tutorial/install/) it.
2. Make sure all the associated modules are installed. I've added all the modules in the [requirements.txt](https://github.com/rohitranaqh/Advanced-Keylogger-with-Webcam-and-Microphone-Spy/blob/main/requirements.txt) file.
3. If any of the module is not in the requirements.txt file then open Command Prompt & type
```
pip install ModuleName
```
5. At **line 96** in the main file enter your full email instead of quitehacker@instagram.com.
6. At **line 97** in the main file enter the password for that email account.
7. Make sure in the gmail account settings that the [allow less secure apps](https://support.google.com/accounts/answer/6010255?hl=en#zippy=%2Cif-less-secure-app-access-is-on-for-your-account) is on.
8. Open up a Command Prompt and Change to the directory the program is placed and execute the [AdvancedKeylogger.py](https://github.com/rohitranaqh/Advanced-Keylogger-with-Webcam-and-Microphone-Spy/blob/main/Advnaced%20Keylogger.py) file.
9. Open the graphical file manager and go to the C://Users/Public/Logs directory to watch the program in action.
10. After files are encrypted and sent to email, download them and place them in the directory specified in [Decryptor.py](https://github.com/rohitranaqh/Advanced-Keylogger-with-Webcam-and-Microphone-Spy/blob/main/Decryptor.py) and run the decrypt file in command prompt.

## Working:
* Creates a directory to temporarily store information to exfitrate
* Gets all the essential network information -> stores to log file (takes about a minute)
* Gets the wireless network ssid's and passwords in XML data file
* Retrieves system hardware and running process/service info
* If the clipboard is activated and contains anything -> stores to log file
* Browsing history is retrieved as a JSON data file then dumped into a log file
* Then using multiprocessing 4 features work together simultaniously: (Timeouts and ranges can be adjusted)
* Logs pressed keys
* Takes screenshots every 15 seconds
* Records microphone in 10 seconds segments
* Takes webcam picture every 5 seconds
* After all the .txt and .xml files are grouped together and encrypted to protect sensitive data
* Then by individual directory, the files are grouped and sent through email by file type with regex magic
* Finally the Log directory is deleted and the program loops back to the beginning to repeat the same process.
