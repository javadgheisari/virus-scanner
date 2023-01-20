import time
import cloudmersive_virus_api_client
from cloudmersive_virus_api_client.rest import ApiException
from pprint import pprint
from selenium import webdriver
from tkinter import Tk, Button, Frame, Entry
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.ttk import Combobox, Label
import os
import glob
import threading
import sys
# from pathlib import Path

# Configure API key authorization: Apikey
configuration = cloudmersive_virus_api_client.Configuration()
configuration.api_key['Apikey'] = '1b64b6d4-c120-43c5-ae23-b3aa482d73da'

# create an instance of the API class
api_instance = cloudmersive_virus_api_client.ScanApi(cloudmersive_virus_api_client.ApiClient(configuration))

def base():
    max_size = int(input("enter max_size(mb): "))
    i = 0
    while True:
        # print(len(os.listdir('/media/javad')))
        if len(os.listdir('/media/javad')) == 5:
            i = i+1
            if i == 1:
                usb_scan(max_size)
            else:
                pass

        choice = int(input("1.System-Scan \n2.Drive-Scan \n3.File-Scan \n4.Link-Scan \n5.Usb-Scan \n6.Exit \n=>"))

        # SystemScan       
        if choice == 1:
            system_scan(max_size)

        # DriveScan
        elif choice == 2:
            drive_scan(max_size)

        # FileScan
        elif choice == 3:
            file_scan(max_size)

        # LinkScan
        elif choice == 4:
            link_scan()

        # UsbScan
        elif choice == 5 and i != 1:
            usb_scan(max_size)
        
        elif choice == 6:
            print("you are exit!")
            sys.exit()
        
        print("---------------------------------------------------------------------------------------")

def check_virus(address, max_size=1):
    values = glob.glob(f'{address}/*')
    if values == []:
        try:
            if os.path.getsize(address) <= max_size * 1000000:
                print('address file:', address)
                try:
                    # Scan a file for viruses
                    api_response = api_instance.scan_file(address)
                    print('result:', end=' ')
                    pprint(api_response)
                    print('-----------')
                except ApiException as e:
                    print("Exception when calling ScanApi->scan_file: %s\n" % e)
                except IsADirectoryError:
                    print("result: directory pass")
                except PermissionError:
                    pass
        except FileNotFoundError:
            pass
    else:
        for val in values:
            check_virus(val, max_size)


def system_scan(max_size):
    print('*** System Scan ***')
    # max_size = int(input("enter max_size(mb): "))
    check_virus('/home/javad/Documents', max_size)

def drive_scan(max_size):
    print('*** Drive Scan ***')
    # max_size = int(input("enter max_size(mb): "))
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    input_dir = askdirectory(initialdir="/media/javad") # file | Input file to perform the operation on.
    # print(type(input_file))
    check_virus(input_dir, max_size)
    
def file_scan(max_size):
    print('*** File Scan ***')
    # max_size = int(input("enter max_size(mb): "))
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    input_file = askopenfilename() # file | Input file to perform the operation on.
    size_file = os.stat(input_file).st_size / 1000000
    if size_file < max_size:
        try:
            # Scan a file for viruses
            api_response = api_instance.scan_file(input_file)
            print('result:', end=' ')
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling ScanApi->scan_file: %s\n" % e)
    else:
        print("size error, your size file is:", size_file, 'mb')
        base()

def link_scan():
    print('*** Link Scan ***')
    driver = webdriver.Firefox()
    url = ''
    while True:
        url_old = url
        url = driver.current_url
        if url != 'about:blank' and url_old != url:
            print('site-url:',url)
            input_site = cloudmersive_virus_api_client.WebsiteScanRequest(url) # WebsiteScanRequest | 
            try:
                # Scan a website for malicious content and threats
                api_response = api_instance.scan_website(input_site)
                print('result:', end=' ')
                pprint(api_response)
                print('-----------')
            except ApiException as e:
                print("Exception when calling ScanApi->scan_website: %s\n" % e)
        time.sleep(3)

def usb_scan(max_size):
    print('*** USB Scan ***')
    usb_found = False
    drives = os.listdir('/media/javad')
    for drive in drives:
        if (drive == 'DA0C9A240C99FBA71' or drive == 'DA0C9A240C99FBA7' or drive == 'New Volume1' or drive == 'New Volume'):
            continue
        else:
            usb_found = True
            # max_size = int(input("enter max_size(mb): "))
            if max_size < 5:
                check_virus(f'/media/javad/{drive}', max_size)
            else:
                print("size error, your size file is:", max_size, 'mb')
                base()
    if not usb_found:
        print('usb not found')


# def retrieve():
#     ch = choice.get()[0]
#     if ch == "1":
#         system_scan()
#     if ch == "2":
#         file_scan()
#     if ch == "3":
#         link_scan()
#     if ch == "4":
#         usb_scan()
    
# root = Tk()
# root.geometry('350x250')
# frame = Frame(root)
# frame.pack()
# # Label(root, text='select')
# choices = ['1.System-Scan', '2.File-Scan', '3.Link-Scan', '4.Usb-Scan']
# # variable = StringVar(root)
# # variable.set('1.FileScan')
# choice = Combobox(root, values=choices, width=20, height=50)
# choice.set("Pick an Option")
# choice.pack(padx = 5, pady = 5)

# btn = Button(root, text='submit', command=retrieve)
# btn.pack(padx = 5, pady = 5)

# root.mainloop()

t = threading.Thread(target=base)
# t.setDaemon(True)
t.start()
# time.sleep(500)