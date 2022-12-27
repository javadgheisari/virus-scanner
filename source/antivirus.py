from __future__ import print_function
import time
import cloudmersive_virus_api_client
from cloudmersive_virus_api_client.rest import ApiException
from pprint import pprint
from selenium import webdriver
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

# Configure API key authorization: Apikey
configuration = cloudmersive_virus_api_client.Configuration()
configuration.api_key['Apikey'] = 'API-KEY'

choice = int(input("1.filescan \n2.linkscan \n=>"))

# create an instance of the API class
api_instance = cloudmersive_virus_api_client.ScanApi(cloudmersive_virus_api_client.ApiClient(configuration))


if choice == 1:
    max_size = int(input("enter max_size(mb): "))
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    input_file = askopenfilename() # file | Input file to perform the operation on.
    size_file = os.stat(input_file).st_size / 1000000
    if size_file < max_size:
        try:
            # Scan a file for viruses
            api_response = api_instance.scan_file(input_file)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling ScanApi->scan_file: %s\n" % e)
    else:
        print("size error, your size file is:", size_file, 'mb')

elif choice == 2:
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
                pprint(api_response)
            except ApiException as e:
                print("Exception when calling ScanApi->scan_website: %s\n" % e)
        time.sleep(3)

