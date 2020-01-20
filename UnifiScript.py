# import so script can request a URL
import requests

# import for Twilio so script may send an SMS
from twilio.rest import Client

# imports for selenium so script can automate the Chrome browser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# import so script can sleep
import time

# import so script can call the command line
import os

# import so script can grab output from the command line
import subprocess

# import so script can get the current date and time and the previous date
from datetime import datetime, timedelta

# import so script can create Excel workbook
import xlsxwriter

# import so script can create a ZIP folder
from zipfile import ZipFile

# import so script can remove a directory
import shutil

# class that holds device objects (switches and access points)
class Devices:
    #when an object is initialized, this function is called
    def __init__(self, driver, devices_xpaths):
        printing = False
        # for each element within the array of xpaths, assign the object equal to that xpath (or an alternative if the conditions are met)

        # the resulting text from each xpath (e.g. the usable data from each xpath)
        devices_xpaths_text = []

        #grab the text of each xpath (e.g. the data), if the xpath will not exist then assign different text,
        for i in range(len(devices_xpaths)):
            try:
                if (i == 12 or i == 13 or i == 14 or i == 15 or i == 18 or i == 19 or i == 20 or i == 21) and "Switch" in devices_xpaths_text[0]:
                    devices_xpaths_text.append("-")
                    check = 1

                elif i == 16 and (str(devices_xpaths_text[14]) == str(0) or str(devices_xpaths_text[14]) == "-"):
                    devices_xpaths_text.append("No clients")
                    check = 2

                elif i == 17 and (str(devices_xpaths_text[15]) == str(0) or str(devices_xpaths_text[15]) == "-"):
                    devices_xpaths_text.append("No clients")
                    check = 3

                else:
                    check = 4
                    devices_xpaths_text.append(driver.find_element_by_xpath(devices_xpaths[i]).text)

            # if the element does not exist for some reason (it should exist), just say that there was an error retrieving the data point
            except NoSuchElementException:
                if i == 16 or i == 17:
                    devices_xpaths_text.append("No clients (Unifi Error)")

                else:
                    print("Device NoSuchElementException occurred at: " + str(i) + " if area: " + str(check) + " XPath: " + devices_xpaths[i])
                    devices_xpaths_text.append("Error retrieving data point")
                    printing = True

            # if the element no longer exists for some reason (it should exist), just say there was an error retrieving the data point
            except StaleElementReferenceException:
                print("Device StaleElementReferenceException occurred at: " + str(i) + " if area: " + str(check) + " XPath: " + devices_xpaths[i])
                devices_xpaths_text.append("Error retrieving data point")
                printing = True

        # assign attributes of the object based on the text returned from each xpath
        self.name = devices_xpaths_text[0]
        self.mac_address = devices_xpaths_text[1]
        self.ip_address = devices_xpaths_text[2]
        self.status = devices_xpaths_text[3]
        self.model = devices_xpaths_text[4]
        self.version = devices_xpaths_text[5]
        self.uptime = devices_xpaths_text[6]
        self.mem_usage = devices_xpaths_text[7]
        self.cpu_usage = devices_xpaths_text[8]
        self.clients = devices_xpaths_text[9]
        self.down = devices_xpaths_text[10]
        self.up = devices_xpaths_text[11]
        self.wlan2g = devices_xpaths_text[12]
        self.wlan5g = devices_xpaths_text[13]
        self.clients2g = devices_xpaths_text[14]
        self.clients5g = devices_xpaths_text[15]
        self.experience2g = devices_xpaths_text[16]
        self.experience5g = devices_xpaths_text[17]
        self.bssid = devices_xpaths_text[18]
        self.tx = devices_xpaths_text[19]
        self.rx = devices_xpaths_text[20]
        self.channel = devices_xpaths_text[21]

        if printing == True:
            print(self)

    #when an object is printed, this function returns the device attributes in a JSON format
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    # function that returns the value of each attribute of the object in a list
    def listOfAttributes(self):
        return [self.name, self.mac_address, self.ip_address, self.status, self.model, self.version, self.uptime, self.mem_usage, self.cpu_usage, self.clients, self.down, self.up, self.wlan2g, self.wlan5g, self.clients2g, self.clients5g, self.experience2g, self.experience5g, self.bssid, self.tx, self.rx, self.channel]

# end of class "Devices"

# class that holds client objects (printers, laptops, phones, etc.)
class Clients:
    #when an object is initialized, this function is called
    def __init__(self, driver, clients_xpaths):
        printing = False
        # for each element within the array of xpaths, assign the object equal to that xpath (or an alternative if the conditions are met)

        # the resulting text from each xpath (e.g. the usable data from each xpath)
        clients_xpaths_text = []

        # get the text of each attribute of the device and add to the list
        for i in range(len(clients_xpaths)):

            try:
                if (i == 5 or i == 10) and clients_xpaths_text[4] == "LAN":
                    check = 1
                    clients_xpaths_text.append("-")

                else:
                    check = 2
                    clients_xpaths_text.append(driver.find_element_by_xpath(clients_xpaths[i]).text)

            # if the element does not exist for some reason (it should exist), just say that there was an error retrieving the data point
            except (NoSuchElementException, StaleElementReferenceException):
                print("Client NoSuchElementException occurred at: " + str(i) + " if area: " + str(check) + " XPath: " + clients_xpaths[i])
                clients_xpaths_text.append("Error retrieving data point")
                printing = True

            # if the element no longer exists for some reason (it should exist), just say there was an error retrieving the data point
            except StaleElementReferenceException:
                print("Client StaleElementReferenceException occurred at: " + str(i) + " if area: " + str(check) + " XPath: " + clients_xpaths[i])
                clients_xpaths_text.append("Error retrieving data point")
                printing = True

        # assign name of device as an attribute
        self.name = clients_xpaths_text[0]

        # assign hostname of device as an attribute
        self.hostname = clients_xpaths_text[1]

        # assign mac address of device as an attribute
        self.mac_address = clients_xpaths_text[2]

        # assign ip address of device as an attribute
        self.ip_address = clients_xpaths_text[3]

        # assign connection of device as an attribute
        self.connection = clients_xpaths_text[4]

        # assign status of device as an attribute
        self.wifi_experience = clients_xpaths_text[5]

        # assign model of device as an attribute
        self.status = clients_xpaths_text[6]

        # assign uptime of device as an attribute
        self.ap_port = clients_xpaths_text[7]

        # assign channel of client as an attribute
        self.channel = clients_xpaths_text[8]

        # assign wifi connection of client as an attribute
        self.wifi_connection = clients_xpaths_text[9]

        self.signal = clients_xpaths_text[10]

        # assign rx rate of client as an attribute
        self.rx_rate = clients_xpaths_text[11]

        # assign tx rate of client as an attribute
        self.tx_rate = clients_xpaths_text[12]

        # memory usage of device as an attribute
        self.up = clients_xpaths_text[13]

        # assign cpu usage of device as an attribute
        self.down = clients_xpaths_text[14]

        # assign uptime of device as an attribute
        self.uptime = clients_xpaths_text[15]

        # assign vendor of client as an attribute
        self.vendor = clients_xpaths_text[16]

        # assign type of client as an attribute
        self.type = clients_xpaths_text[17]

        # assign category of client as an attribute
        self.category = clients_xpaths_text[18]

        # assign os name of client as an attribute
        self.os_name = clients_xpaths_text[19]

        if printing == True:
            print(self)

    #when an object is printed, this function returns the device attributes in a JSON format
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    # function that returns the value of each attribute of the object in a list
    def listOfAttributes(self):
        return [self.name, self.hostname, self.mac_address, self.ip_address, self.connection, self.wifi_experience, self.status, self.ap_port, self.channel, self.wifi_connection, self.signal, self.rx_rate, self.tx_rate, self.down, self.up, self.uptime, self.vendor, self.type, self.category, self.os_name]

# end of class "Clients"

# function that gets the status of the network (if it is up or down)
def getNetworkStatus():

    # the first test url, google.com because that is rarely down
    test_url = "https://www.google.com"

    # number of seconds we are willing to wait for the request to go through
    timeout = 5

    # try a get request to google.com
    try:
        _ = requests.get(test_url, timeout=timeout)
        return True

    # if there is an issue
    except (requests.ConnectionError, requests.ReadTimeout):
        # try a get request to youtube.com
        try:
            test_url = "https://www.youtube.com"
            _ = requests.get(test_url, timeout=timeout)
            return True

        #if there is an issue now, it's unlikely both sites are down, so it's extremely likely the network is down
        except (requests.ConnectionError, requests.ReadTimeout):
            return False

# end of function "getNetworkStatus()"

# function to get date and time
def getCurrentDateTime():
    # the original datetime given by the datetime.dateime.now() function (very messy)
    datetime_original = datetime.now()

    date_final = str(datetime_original.strftime("%m-%d-%Y "))

    # the hour given by the time
    time_hour = int(datetime_original.hour)

    time_minute = int(datetime_original.minute)

    if time_minute < 10:
        time_minute = '0' + str(time_minute)

    if time_hour > 12:
        time_hour -= 12

        if time_hour < 10:
            time_final = "0" + str(time_hour) + ":" + str(time_minute) + "PM"

        else:
            time_final = str(time_hour) + ":" + str(time_minute) + "PM"

    elif time_hour == 12:
        time_final = str(time_hour) + ":" + str(time_minute) + "PM"

    elif time_hour == 0:
        time_final = "12:" + str(time_minute) + "AM"

    else:
        time_final = str(time_hour) + ":" + str(time_minute) + "AM"

    # assembles date and time together to look readable
    datetime_final = date_final + time_final + " EST"

    return datetime_final

# end of getCurrentDateTime() function

# function that gets the previous date
def getPreviousDate():

    # the previous date
    previous_date = str((datetime.now() - timedelta(1)).strftime('%m.%d.%Y'))

    return previous_date

# end of getPreviousDate() function

# function that retrieves network information if the network is up
def getNetworkInfo(twilio_body, network_issue, issue_count):

    # boolean that holds the initial status of the network prior to being subjected to this function, as the detected network status can change throughout this function compared to when the script previously ran, if it does change, then a message will need to be sent
    previous_network_issue = network_issue

    # boolean that holds whether there has been an error with the script or not, False by default
    script_issue = False

    # string that will hold info about network that will then be added to Twilio message
    twilio_network_info = ""

    #the username used to access the Unifi Controller
    unifi_username = "PUT_USERNAME_HERE"

    #the password used to access the Unifi Controller
    unifi_password = "PUT_PASSWORD_HERE"

    #dictionary that holds data about all devices (switches and access points)
    devices_data = {}

    #dictionary that holds data about all clients (nodes connected to network)
    clients_data = {}

    # path of google chrome on local computer
    CHROME_PATH = 'PATH_OF_GOOGLE_CHROME_HERE'

    # path of chromedriver on local computer
    CHROMEDRIVER_PATH = 'PATH_OF_CHROMEDRIVER_HERE'

    # computer screen resolution
    WINDOW_SIZE = "1920,1080"

    # setting these up will allow the browser to run in the background so it is not apparent to the user of the computer that the script is running
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.binary_location = CHROME_PATH

    #driver is used to navigate through the web browser, the web browser will open in Chrome silently
    driver = webdriver.Chrome(executable_path = CHROMEDRIVER_PATH, options = chrome_options)

    #open https://localhost:8443/ (the Unifi Controller) in Chrome
    driver.get("https://localhost:8443/")

    # wait for advanced button to load
    advanced_button_load = checkLoadElement("/html/body/div/div[2]/button[3]", driver, 20)

    if advanced_button_load == True:

        # the button to go to the link that will allow the browser to proceed
        advanced_button = driver.find_element_by_xpath("/html/body/div/div[2]/button[3]")

        # click the button
        advanced_button.click()

        # wait for proceed link to load
        proceed_link_load = checkLoadElement("/html/body/div/div[3]/p[2]/a", driver, 20)

        if proceed_link_load == True:

            # the link to go to the login page
            proceed_link = driver.find_element_by_xpath("/html/body/div/div[3]/p[2]/a")

            #click the link
            proceed_link.click()

            #wait for username text field to load
            username_text_field_load = checkLoadElement("/html/body/div/ui-view/ui-view/div/div/div/div/div[3]/ui-view/div/form/div[1]/input", driver, 20)

            #if username text field loads in specified time
            if username_text_field_load == True:
                #the text field where the username must be placed
                username_text_field = driver.find_element_by_xpath("/html/body/div/ui-view/ui-view/div/div/div/div/div[3]/ui-view/div/form/div[1]/input")

                #input username into text field
                username_text_field.send_keys(unifi_username)

                #the text field where the password must be placed
                password_text_field = driver.find_element_by_xpath("/html/body/div/ui-view/ui-view/div/div/div/div/div[3]/ui-view/div/form/div[2]/input")

                #input password into text field
                password_text_field.send_keys(unifi_password)

                #the sign in button to access the Unifi Controller
                sign_in_button = driver.find_element_by_xpath("//*[@id='loginButton']")

                #click on the sign in button to login
                sign_in_button.click()

                #wait for pop-up to load
                pop_up_load = checkLoadElement("//*[@id='whatsNewItemContainer-0']/div/div[1]/div[2]", driver, 20)

                #if pop up loads in specified time
                if pop_up_load == True:

                    #closes out of pop-up that first shows when logging in
                    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

                    #wait for the devices button to load
                    devices_button_load = checkLoadElement("/html/body/div/ui-view/ui-view/div/div/div/unifi-global-side-nav/div/div/div[1]/unifi-global-side-nav-item[4]", driver, 20)

                    #if devices button loads in specified time
                    if devices_button_load == True:

                        #button to see all Unifi devices (switches and access points)
                        devices_button = driver.find_element_by_xpath("/html/body/div/ui-view/ui-view/div/div/div/unifi-global-side-nav/div/div/div[1]/unifi-global-side-nav-item[4]")

                        #click on the button to see information
                        devices_button.click()

                        # wait for the devices button to load
                        devices_button_menu_load = checkLoadElement("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[8]/unifi-aura-list-column-selector/div/div/button", driver, 20)

                        # if devices button loads in specified time
                        if devices_button_menu_load == True:

                            #button to check off all desired fields we want about the devices
                            devices_menu_button = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[8]/unifi-aura-list-column-selector/div/div/button")

                            #click on the button to see customize columns checkbox
                            devices_menu_button.click()

                            #wait for the customize columns checkbox to load
                            devices_customize_columns_checkbox_load = checkLoadElement("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[8]/unifi-aura-list-column-selector/div/div/div/div[1]/div/div[2]/div/label", driver, 20)

                            #if customize columns checkbox loads
                            if devices_customize_columns_checkbox_load == True:

                                #the customize columns checkbox
                                devices_customize_columns_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[8]/unifi-aura-list-column-selector/div/div/div/div[1]/div/div[2]/div/label")

                                #clicks the customize columns checkbox
                                devices_customize_columns_checkbox.click()

                                #wait for mac address checkbox to load
                                devices_mac_address_checkbox_load = checkLoadElement("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[8]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[2]/div/label", driver, 20)

                                #if mac address checkbox loads
                                if devices_mac_address_checkbox_load == True:

                                    #the mac address checkbox
                                    devices_mac_address_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[8]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[2]/div/label")

                                    #clicks mac address checkbox
                                    devices_mac_address_checkbox.click()

                                    #the memory usage checkbox
                                    memory_usage_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[9]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[9]/div/label")

                                    #clicks memory usage checkbox
                                    memory_usage_checkbox.click()

                                    #the cpu usage checkbox
                                    cpu_usage_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[10]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[10]/div/label")

                                    #clicks cpu usage checkbox
                                    cpu_usage_checkbox.click()

                                    #the clients checkbox
                                    clients_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[11]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[12]/div/label")

                                    #clicks clients checkbox
                                    clients_checkbox.click()

                                    #the down checkbox
                                    down_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[12]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[13]/div/label")

                                    #clicks down checkbox
                                    down_checkbox.click()

                                    # the up checkbox
                                    up_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[13]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[14]/div/label")

                                    # clicks up checkbox
                                    up_checkbox.click()

                                    # the wlan2g checkbox
                                    wlan2g_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[14]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[15]/div/label")

                                    # clicks wlan2g checkbox
                                    wlan2g_checkbox.click()

                                    # the wlan5g checkbox
                                    wlan5g_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[15]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[16]/div/label")

                                    # clicks wlan5g checkbox
                                    wlan5g_checkbox.click()

                                    # the clients2g checkbox
                                    clients2g_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[16]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[19]/div/label")

                                    # clicks clients2g checkbox
                                    clients2g_checkbox.click()

                                    # the clients5g checkbox
                                    clients5g_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[17]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[20]/div/label")

                                    # clicks clients5g checkbox
                                    clients5g_checkbox.click()

                                    # the experience2g checkbox
                                    experience2g_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[18]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[21]/div/label")

                                    # clicks experience2g checkbox
                                    experience2g_checkbox.click()

                                    # the experience5g checkbox
                                    experience5g_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[19]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[22]/div/label")

                                    # clicks experience5g checkbox
                                    experience5g_checkbox.click()

                                    # the bssid checkbox
                                    bssid_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[20]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[23]/div/label")

                                    # clicks bssid checkbox
                                    bssid_checkbox.click()

                                    # the tx checkbox
                                    tx_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[21]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[24]/div/label")

                                    # clicks tx checkbox
                                    tx_checkbox.click()

                                    # the rx checkbox
                                    rx_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[22]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[25]/div/label")

                                    # clicks rx checkbox
                                    rx_checkbox.click()

                                    # the channel checkbox
                                    channel_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/thead/tr/th[23]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[28]/div/label")

                                    # clicks channel checkbox
                                    channel_checkbox.click()

                                    # variable containing the total number of devices and how many devices are on the current page
                                    num_of_devices_info = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tfoot/tr/td/unifi-aura-pagination/pagination/pagination-state/span").text

                                    # getting rid of the first space so we can properly grab the total number of devices
                                    num_of_devices_info = num_of_devices_info[num_of_devices_info.index(" ") + 1:]

                                    # variable containing the total number of devices
                                    total_num_of_devices = num_of_devices_info[num_of_devices_info.index(" ") + 1: num_of_devices_info.rindex(" ")]

                                    # header for adding info about the network to the Twilio message, not adding this directly to Twilio message until the end because need to put some text before it, but won't know what to put until the end of the function
                                    twilio_network_info += "Access Point Info:\n"

                                    # count of how many access points there are
                                    total_num_of_access_points = 0

                                    # count of how many access points are connected
                                    connected_access_points = 0

                                    # for each device that is currently on the network, grab pertinent data associated with it
                                    for i in range(1, int(total_num_of_devices) + 1):
                                        #the name of each device, changes throughout loop since there will be a new device through each iteration of the loop
                                        device_name = "device" + str(i)

                                        # array that holds the xpaths of all device data
                                        devices_xpaths = []

                                        name_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[2]"
                                        devices_xpaths.append(name_xpath)

                                        mac_address_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[3]"
                                        devices_xpaths.append(mac_address_xpath)

                                        ip_address_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[4]/span/span"
                                        devices_xpaths.append(ip_address_xpath)

                                        status_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[5]/div/div[1]"
                                        devices_xpaths.append(status_xpath)

                                        model_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[6]/span"
                                        devices_xpaths.append(model_xpath)

                                        version_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[7]"
                                        devices_xpaths.append(version_xpath)

                                        uptime_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[8]"
                                        devices_xpaths.append(uptime_xpath)

                                        memory_usage_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[9]/span"
                                        devices_xpaths.append(memory_usage_xpath)

                                        cpu_usage_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[10]"
                                        devices_xpaths.append(cpu_usage_xpath)

                                        clients_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[11]"
                                        devices_xpaths.append(clients_xpath)

                                        down_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[12]"
                                        devices_xpaths.append(down_xpath)

                                        up_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[13]"
                                        devices_xpaths.append(up_xpath)

                                        wlan2g_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[14]"
                                        devices_xpaths.append(wlan2g_xpath)

                                        wlan5g_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[15]"
                                        devices_xpaths.append(wlan5g_xpath)

                                        clients2g_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[16]/unifi-device-clients-num/div"
                                        devices_xpaths.append(clients2g_xpath)

                                        clients5g_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[17]/unifi-device-clients-num/div"
                                        devices_xpaths.append(clients5g_xpath)

                                        experience2g_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[18]/unifi-ap-satisfaction-status-bar/div/unifi-wifi-satisfaction-status-bar/div/div[2]/div"
                                        devices_xpaths.append(experience2g_xpath)

                                        experience5g_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[19]/unifi-ap-satisfaction-status-bar/div/unifi-wifi-satisfaction-status-bar/div/div[2]/div"
                                        devices_xpaths.append(experience5g_xpath)

                                        bssid_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[20]/div"
                                        devices_xpaths.append(bssid_xpath)

                                        tx_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[21]"
                                        devices_xpaths.append(tx_xpath)

                                        rx_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[22]"
                                        devices_xpaths.append(rx_xpath)

                                        channel_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[3]/div/div/table/tbody/tr[" + str(i) + "]/td[23]"
                                        devices_xpaths.append(channel_xpath)

                                        #add the device to the dictionary (in the dictionary index after all other devices that came before it in the loop)
                                        devices_data[device_name] = Devices(driver, devices_xpaths)

                                        # if the device is not a switch (and therefore an access point) then add it's status to the Twilio message
                                        if not "Switch" in devices_data[device_name].name:
                                            # add to the number of total access points
                                            total_num_of_access_points += 1

                                            # adding info about each access point to the Twilio message
                                            twilio_network_info += devices_data[device_name].name[0: devices_data[device_name].name.index(' ')] + ': ' + devices_data[device_name].status + "\n"

                                            # if there is an access point that is not connected and the network was working previously, indicate that the network is now no longer working and add to the issue count
                                            if not devices_data[device_name].status == 'CONNECTED' and network_issue == False:
                                                network_issue = True
                                                issue_count += 1

                                            # if the access point is connected, add to the total number of connected access points
                                            elif devices_data[device_name].status == 'CONNECTED':
                                                connected_access_points += 1

                                        # if this is the last device, then add another empty line to make Twilio message look nicer
                                        if i == int(total_num_of_devices):
                                            twilio_network_info += '\n'

                                        # for testing, shows device info in console
                                        # print(devices_data[device_name])

                                    # end of loop

                                    # if all access points are connected, then there is no network issue
                                    if connected_access_points == int(total_num_of_access_points):
                                        network_issue = False
                                        issue_count = 0

                                    #the clients button to see all clients/nodes (printers, mobile devices, desktops, etc.) on the network
                                    clients_button = driver.find_element_by_xpath("/html/body/div[1]/ui-view/ui-view/div/div/div/unifi-global-side-nav/div/div/div[1]/unifi-global-side-nav-item[5]")

                                    #clicks clients button
                                    clients_button.click()

                                    #checks if the client menu button has loaded
                                    clients_menu_button_load = checkLoadElement("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[11]/unifi-aura-list-column-selector/div/div/button", driver, 20)

                                    #if clients menu button loaded
                                    if clients_menu_button_load == True:
                                        #the client menu button that will show the checkboxes for each attribute that a client may have
                                        clients_menu_button = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[11]/unifi-aura-list-column-selector/div/div/button")

                                        #click on the clients menu button
                                        clients_menu_button.click()

                                        #checks if the customize columns checkbox has loaded
                                        clients_customize_columns_checkbox_load = checkLoadElement("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[11]/unifi-aura-list-column-selector/div/div/div/div[1]/div/div[3]/div/label", driver, 20)

                                        #if customize columns checkbox loaded
                                        if clients_customize_columns_checkbox_load == True:
                                            # the clients customize columns checkbox to alter the attributes that are shown for each client
                                            clients_customize_columns_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[11]/unifi-aura-list-column-selector/div/div/div/div[1]/div/div[3]/div/label")

                                            # click on the clients customize columns checkbox
                                            clients_customize_columns_checkbox.click()

                                            # checks if the hostname checkbox has loaded
                                            hostname_checkbox_load = checkLoadElement("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[11]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[4]/div/label", driver, 20)

                                            # if hostname checkbox loaded
                                            if hostname_checkbox_load == True:
                                                #the hostname checkbox
                                                hostname_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[11]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[4]/div/label")

                                                #clicks the hostname checkbox
                                                hostname_checkbox.click()

                                                #the mac address checkbox
                                                clients_mac_address_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[12]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[5]/div/label")

                                                #clicks the mac address checkbox
                                                clients_mac_address_checkbox.click()

                                                #the status checkbox
                                                status_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[13]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[10]/div/label")

                                                #clicks the status checkbox
                                                status_checkbox.click()

                                                # the activity checkbox
                                                activity_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[14]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[20]/div/label")

                                                # clicks the activity checkbox
                                                activity_checkbox.click()

                                                # the channel checkbox
                                                clients_channel_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[13]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[14]/div/label")

                                                # clicks the channel checkbox
                                                clients_channel_checkbox.click()

                                                # the wifi connection checkbox
                                                wifi_connection_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[14]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[15]/div/label")

                                                # clicks the wifi connection checkbox
                                                wifi_connection_checkbox.click()

                                                # the signal checkbox
                                                signal_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[15]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[17]/div/label")

                                                # clicks the signal checkbox
                                                signal_checkbox.click()

                                                # the rx rate checkbox
                                                rx_rate_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[16]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[18]/div/label")

                                                # clicks the rx rate checkbox
                                                rx_rate_checkbox.click()

                                                # the tx rate checkbox
                                                tx_rate_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[17]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[19]/div/label")

                                                # clicks the tx rate checkbox
                                                tx_rate_checkbox.click()

                                                # the vendor checkbox
                                                vendor_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[18]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[26]/div/label")

                                                # clicks the vendor checkbox
                                                vendor_checkbox.click()

                                                # the type checkbox
                                                type_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[19]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[27]/div/label")

                                                # clicks the type checkbox
                                                type_checkbox.click()

                                                # the category checkbox
                                                category_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[20]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[28]/div/label")

                                                # clicks the category checkbox
                                                category_checkbox.click()

                                                # the os name checkbox
                                                os_name_checkbox = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/thead/tr/th[21]/unifi-aura-list-column-selector/div/div/div/div[2]/div/div/div[29]/div/label")

                                                # clicks the os name checkbox
                                                os_name_checkbox.click()

                                                # variable containing the total number of clients and how many clients are on the current page
                                                num_of_clients_info = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tfoot/tr/td/unifi-aura-pagination/pagination/pagination-state/span").text

                                                # getting rid of the first space so we can properly grab the total number of clients
                                                num_of_clients_info = num_of_clients_info[num_of_clients_info.index(" ") + 1:]

                                                # variable containing the total number of clients
                                                total_num_of_clients = num_of_clients_info[num_of_clients_info.index(" ") + 1: num_of_clients_info.rindex(" ")]

                                                #if there are more then 50 clients, show 100 rows instead of 50
                                                if int(total_num_of_clients) > 50:

                                                    # rows per page dropdown menu
                                                    rows_per_page_dropdown = driver.find_element_by_xpath("//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tfoot/tr/td/unifi-aura-pagination/pagination/pagination-state/pagination-page-size/select")

                                                    # clicks the rows per page dropdown menu
                                                    rows_per_page_dropdown.click()

                                                    # pressing down arrow to hover over 100
                                                    webdriver.ActionChains(driver).send_keys(Keys.DOWN).perform()

                                                    # pressing enter to confirm that 100 rows should display
                                                    webdriver.ActionChains(driver).send_keys(Keys.RETURN).perform()

                                                # header for adding info about network clients to the Twilio message
                                                twilio_network_info += "Client Info:\n"

                                                # for each client that is currently on the network, grab pertinent data associated with it
                                                for i in range(1, int(total_num_of_clients) + 1):

                                                    # the name of each client, changes throughout loop since there will be a new client through each iteration of the loop
                                                    client_name = "client" + str(i)

                                                    # array that holds the xpaths of all device data
                                                    clients_xpaths = []

                                                    client_name_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[2]"

                                                    # boolean that checks if the client still exists, as time has elapsed since all clients were gathered so one may have gotten off the network
                                                    client_exists = checkLoadElement(client_name_xpath, driver, 3)

                                                    # if the client no longer exists, skip over the creation of this client and move to the next
                                                    if client_exists == False:
                                                        i -= 1
                                                        total_num_of_clients = int(total_num_of_clients) - 1
                                                        continue

                                                    clients_xpaths.append(client_name_xpath)

                                                    hostname_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[3]"
                                                    clients_xpaths.append(hostname_xpath)

                                                    client_mac_address_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[4]"
                                                    clients_xpaths.append(client_mac_address_xpath)

                                                    client_ip_address_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[5]"
                                                    clients_xpaths.append(client_ip_address_xpath)

                                                    connection_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[8]"
                                                    clients_xpaths.append(connection_xpath)

                                                    wifi_experience_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[6]/unifi-wifi-satisfaction-status-bar/div/div[2]/div"
                                                    clients_xpaths.append(wifi_experience_xpath)

                                                    status_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[7]/span"
                                                    clients_xpaths.append(status_xpath)

                                                    ap_port_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[9]/button"
                                                    clients_xpaths.append(ap_port_xpath)

                                                    client_channel_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[10]"
                                                    clients_xpaths.append(client_channel_xpath)

                                                    wifi_connection_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[11]"
                                                    clients_xpaths.append(wifi_connection_xpath)

                                                    signal_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[12]/span/span"
                                                    clients_xpaths.append(signal_xpath)

                                                    rx_rate_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[13]"
                                                    clients_xpaths.append(rx_rate_xpath)

                                                    tx_rate_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[14]"
                                                    clients_xpaths.append(tx_rate_xpath)

                                                    up_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[15]"
                                                    clients_xpaths.append(up_xpath)

                                                    down_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[16]"
                                                    clients_xpaths.append(down_xpath)

                                                    client_uptime_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[17]"
                                                    clients_xpaths.append(client_uptime_xpath)

                                                    vendor_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[18]"
                                                    clients_xpaths.append(vendor_xpath)

                                                    type_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[19]"
                                                    clients_xpaths.append(type_xpath)

                                                    category_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[20]"
                                                    clients_xpaths.append(category_xpath)

                                                    os_name_xpath = "//*[@id='contentContainer']/div/ui-view/div/div[2]/div/div/table/tbody/tr[" + str(i) + "]/td[21]"
                                                    clients_xpaths.append(os_name_xpath)

                                                    # add the client to the dictionary (in the dictionary index after all other clients that came before it in the loop)
                                                    clients_data[client_name] = Clients(driver, clients_xpaths)

                                                    # for testing, shows client info in console
                                                    # print(clients_data[client_name])

                                                # adding info about the number of clients to the Twilio message
                                                twilio_network_info += "There are " + str(total_num_of_clients) + " clients currently on the network."

                                                # if there is a network issue, add the AnyDesk info to the Twilio message so we can remote in to resolve the issue
                                                if network_issue == True:
                                                    twilio_network_info += "\n\n" + getAnyDeskInfo()

                                            #if the element doesn't load, add error code to Twilio message and increment the issue count
                                            else:
                                                twilio_network_info += "\nScript Error: 009 - Client Menu - Column - More"
                                                issue_count += 1
                                                network_issue = True
                                                script_issue = True

                                        else:
                                            twilio_network_info += "\nScript Error: 008 - Client Menu - Column"
                                            issue_count += 1
                                            network_issue = True
                                            script_issue = True

                                    else:
                                        twilio_network_info += "\nScript Error: 007 - Client Menu"
                                        issue_count += 1
                                        network_issue = True
                                        script_issue = True

                                else:
                                    twilio_network_info += "\nScript Error: 006 - Device Menu - Column - More"
                                    issue_count += 1
                                    network_issue = True
                                    script_issue = True

                            else:
                                twilio_network_info += "\nScript Error: 005 - Device Menu - Column"
                                issue_count += 1
                                network_issue = True
                                script_issue = True

                        else:
                            twilio_network_info += "\nScript Error: 004 - Device Menu"
                            issue_count += 1
                            network_issue = True
                            script_issue = True

                    else:
                        twilio_network_info += "\nScript Error: 003 - Device Button"
                        issue_count += 1
                        network_issue = True
                        script_issue = True

                else:
                    twilio_network_info += "\nScript Error: 002 - Pop-Up"
                    issue_count += 1
                    network_issue = True
                    script_issue = True


            else:
                twilio_network_info += "\nScript Error: 001 - Login Field"
                issue_count += 1
                network_issue = True
                script_issue = True

    #send the final twilio message, if it should be sent (if the network was ok before but now isn't, or if the network was not ok before but now is)
    if not network_issue == previous_network_issue:
        if network_issue == True:
            if script_issue == False:
                twilio_body += "The issue(s) with the network just occurred.\n\n"

            else:
                twilio_body += "The issue with the script just occurred.\n\n"

        else:
            twilio_body += "The network has no issues.\n\n"

        twilio_body += twilio_network_info
        sendTwilioMessage(twilio_body, "numbers.txt")

    elif network_issue == True and issue_count % 12 == 0:
        twilio_body += "The issue(s) with the network have lasted approximately " + str(issue_count / 12) + " hour(s).\n\n"
        twilio_body += twilio_network_info
        sendTwilioMessage(twilio_body, "numbers.txt")

    # close out of browser
    driver.close()
    driver.quit()

    return network_issue, issue_count, devices_data, clients_data

# end of function "getNetworkInfo(twilio_body, network_issue, issue_count)"

# function that gets AnyDesk information
def getAnyDeskInfo():
    # the id for  AnyDesk account
    anydesk_id = 'ANYDESK_ACCOUNT_ID'

    # the password for our AnyDesk account
    anydesk_password = 'ANYDESK_ACCOUNT_PASSWORD'

    return 'Remote Access Info:\nAnyDesk ID: ' + anydesk_id + '\nAnyDesk Password: ' + anydesk_password
# end of function "getAnyDeskInfo()"

# function that sends Twilio message with the specified body
def sendTwilioMessage(twilio_body, numbers_file):
    # Twilio account SID
    twilio_account_sid = 'TWILIO_ACCOUNT_SID'

    # Twilio account auth token
    twilio_account_auth_token = 'TWILIO_ACCOUNT_AUTH_TOKEN'

    # Twilio phone number
    twilio_from_number = 'TWILIO_PHONE_NUMBER'

    # array of phone number(s) the Twilio message will be sent to, blank by default
    twilio_to_numbers = []

    # text file that holds the list of numbers that needs to be sent the Twilio message; Shane, Joe, Florina, Krutarth, Bhavin
    numbers = open(numbers_file, "r")

    # object that can read the lines of the text file that holds the numbers
    numbers_read = numbers.readlines()

    for line in numbers_read:
        twilio_to_numbers.append(str(line))

    # Twilio client that will be used to actually send a message
    twilio_client = Client(twilio_account_sid, twilio_account_auth_token)

    # send the Twilio message to everyone in the array
    for i in range(len(twilio_to_numbers)):
        # sends Twilio message to specified user
        message = twilio_client.messages \
            .create(
            body=twilio_body,
            from_=twilio_from_number,
            to=twilio_to_numbers[i]
        )
# end of function "sendTwilioMessage(twilio_body, numbers_file)"

# function that creates the folder with the name of the date and this folder will contain all logs for the script that ran on that day
def createDateFolder():
    date_and_time = getCurrentDateTime()

    date = date_and_time[0: date_and_time.index(' ')]

    date = date.replace('-', '.')

    folder_path = 'PATH_TO_FOLDER' + date + '/'

    try:
        os.mkdir(folder_path)
        print('New Date Folder Created: ' + folder_path)
        return True

    except FileExistsError:
        return False

# end of function "createDateFolder()"

# function that creates a ZIP folder of the log files from the previous day
def createZipFolder():

    # will contain list of all file names that must be zipped, blank by default
    file_paths = []

    # gets previous date
    previous_date = getPreviousDate()

    # the folder path that must have all files within it zipped
    folder_path = 'PATH_TO_FOLDER' + previous_date + '/'
    print("Unzipped Folder: " + folder_path)

    # the path of the eventual zip file
    zip_path = 'PATH_TO_FOLDER' + previous_date + '.zip'
    print("Zipped Folder: " + zip_path)

    # going through all directories and subdirectories of the folder (there should not be any folders in this folder but just in case)
    for root, directories, files, in os.walk(folder_path):
        # for each file in the directory, get the full file path and append it to the list of files
        for filename in files:
            # getting full file path
            filepath = os.path.join(root, filename)

            # appending file to list of files
            file_paths.append(filepath)

    # actually zipping files into specified folder that should be zipped
    with ZipFile(zip_path, 'w') as zip:
        for file in file_paths:
            zip.write(file)

    try:
        # deleting old folder that is not zipped, there is no need for it anymore since there is now a zipped version
        shutil.rmtree(folder_path)
        print("Deleted old unzipped folder")

    except FileNotFoundError:
        # if the old folder doesn't exist for whatever reason, don't do anything
        print("Did not delete old unzipped folder")
        pass

# end of function "createZipFolder()"

# function that checks if an HTML element is loaded within the Chrome browser
def checkLoadElement(element_xpath, driver, wait_time):
    count = 0
    while count < wait_time:
        #grabs element
        try:
            element = driver.find_element_by_xpath(element_xpath)
            return True

        # if element does not exist yet, sleep for 1 second and try again
        except NoSuchElementException:
            count += 1
            time.sleep(1)

        # if element has not loaded in 20 seconds, return False
        if count == wait_time:
            return False
# end of function "checkLoadElement(element_xpath, driver, wait_time)"

# the function that attempts to connect to the WiFi (both the regular, guest, and hotspot) to determine if the network is down
def switchToWiFi():

    # the SSID of the regular network
    regular_network_ssid = "REGULAR_WIFI_SSID_HERE"

    # the SSID of the regular network formatted for the command prompt
    regular_network_ssid_cmd = '"REGULAR_WIFI_SSID_HERE"'

    # the profile of the regular network (formatted for the command prompt) that was previously configured on this laptop
    regular_network_profile_cmd = '"REGULAR_WIFI_SSID_HERE"'

    # the SSID of the guest network
    guest_network_ssid = "GUEST_NETWORK_SSID_HERE"

    # the profile of the guest network that was previously configured on this laptop
    guest_network_profile = "GUEST_NETWORK_SSID_HERE"

    # the SSID of the Verizon Hotspot
    hotspot_network_ssid = "VERIZON_HOTSPOT_SSID_HERE"

    # the profile of the Verizon Hotspot that was previously configured on this laptop
    hotspot_network_profile = "VERIZON_HOTSPOT_SSID_HERE"

    # the network that we will eventually be connected to, 'NOT CONNECTED' by default
    network_connected_to = 'NOT CONNECTED'

    # indication that the network was successfully switched, False by default
    switch_successful = False

    # command that must be given to command line to see all available networks
    cmd_networks_available = "netsh wlan show networks"

    # variable that holds information about the networks that are available
    networks_available = str(subprocess.Popen(cmd_networks_available, stdout=subprocess.PIPE).communicate()[0])

    # if the regular WiFi is available to connect to, connect to it
    if regular_network_ssid in networks_available:

        # command that must be given to command line to connect to the regular network
        wifi_connect_cmd = "netsh wlan connect ssid=" + regular_network_ssid_cmd + " name=" + regular_network_profile_cmd

        # line that actually connects the laptop to the regular network
        os.system(wifi_connect_cmd)

        # indicate we are now connected to the regular network
        network_connected_to = regular_network_ssid + " WiFi"

        time.sleep(3)

        # checking the network status
        switch_successful = getNetworkStatus()

    # if the guest WiFi is available to connect to, but not the regular WiFi and the regular WiFi isn't working properly, connect to it
    if (network_connected_to == 'NOT CONNECTED' or switch_successful == False) and guest_network_ssid in networks_available:

        # command that must be given to command line to connect to the guest network
        wifi_connect_cmd = "netsh wlan connect ssid=" + guest_network_ssid + " name=" + guest_network_profile

        # line that actually connects the laptop to the guest network
        os.system(wifi_connect_cmd)

        # indicate we are now connected to the guest network
        network_connected_to = guest_network_ssid + " WiFi"

        time.sleep(3)

        # checking the network status
        switch_successful = getNetworkStatus()

    # if the Verizon Hotspot is available to connect to, but not the regular WiFi or guest WiFi (or neither is working right), connect to it
    if (network_connected_to == 'NOT CONNECTED' or switch_successful == False) and hotspot_network_ssid in networks_available:

        # command that must be given to command line to connect to the Verizon hotspot
        wifi_connect_cmd = "netsh wlan connect ssid=" + hotspot_network_ssid + " name=" + hotspot_network_profile

        # line that actually connects the laptop to the verizon hotspot
        os.system(wifi_connect_cmd)

        # indicate we are now connected to the hotspot
        network_connected_to = hotspot_network_ssid + " hotspot"

        time.sleep(3)

        # checking the network status
        switch_successful = getNetworkStatus()

    return switch_successful, network_connected_to

# end of function switchToWifi()

# function used to create an Excel sheet with data
def createExcelFile(data, headers, file_name_beginning):
    date_and_time = getCurrentDateTime()

    date = date_and_time[0: date_and_time.index(' ')]

    date = date.replace('-', '.')

    time = date_and_time[date_and_time.index(' ') + 1: date_and_time.index(' ') + 8]

    time = time.replace(':', '.')

    folder_path = 'PATH_TO_FOLDER' + date + '/'

    file_name = file_name_beginning + date + '_' + time + '.xlsx'

    full_path = folder_path + file_name

    # variable that holds the actual Excel workbook
    workbook = xlsxwriter.Workbook(full_path)

    # variable that holds the actual Excel worksheet
    worksheet = workbook.add_worksheet()

    # formatting text for header cells
    header_cell_format = workbook.add_format()

    # setting header text to bold
    header_cell_format.set_bold()

    # writing the headers of each column into the worksheet for each header there is
    for i in range(len(headers)):
        # writing the header into the worksheet (row, col, text, format)
        worksheet.write_string(0, i, headers[i], header_cell_format)

    # writing the actual data to the Excel sheet
    # for each device that needs to have data written about it
    for i in range(1, len(data) + 1):

        try:
            # variable that holds the list of attributes of the object (the actual raw data that will be inserted in Excel)
            object_attributes = data[file_name_beginning + str(i)].listOfAttributes()

        # if the data being given does not have a listOfAttributes function, then only a list was given so just make the local variable equal to the passed variable
        except TypeError:
            object_attributes = data

        # for each attribute of the device that needs to have data written about it
        for j in range(len(object_attributes)):
            # write the data to each column, but in the same row because it is the same device
            worksheet.write_string(i, j, object_attributes[j])

    try:
        # close and save and actually create the workbook in the system
        workbook.close()

    except FileNotFoundError:
        date_folder_created = createDateFolder()

        # if the date folder was just created, then it must be a new day, meaning the folder with the previous date must be zipped
        if date_folder_created == True:

            print("Creating Zip Folder...")
            # creates a ZIP folder of the log files from the previous day
            createZipFolder()

# end of function createExcelFile(data, headers, file_name_beginning)

# function that creates a text file logging the status of the results of this script
def createTextFile(file_name_beginning, text_body):
    date_and_time = getCurrentDateTime()

    date = date_and_time[0: date_and_time.index(' ')]

    date = date.replace('-', '.')

    time = date_and_time[date_and_time.index(' ') + 1: date_and_time.index(' ') + 8]

    time = time.replace(':', '.')

    full_path = 'PATH_TO_FOLDER' + date + '/' + file_name_beginning + date + '_' + time + '.txt'

    # creating text file to write to
    text_file = open(full_path, 'w+')

    # writing to text file
    text_file.write(text_body)

    #closing the text file
    text_file.close()

# end of function createTextFile(file_name_beginning, text_body)

# function that returns a String containing all the people currently on the network
def getPeoplePresent(dict_name, data):

    # list of the names of the people on the network, blank by default
    people_names = ''

    # for the number of indices in the data list, grab the name to see who the device belongs to
    for i in range(len(data)):
        # grabbing the name of the client connected to the network
        client_name = data[dict_name + str(i + 1)].name

        # if there is any indicator of a person possessing the device in the name, then grab that name
        if "'s" in client_name or "s'" in client_name:
            # grabbing the name of the person that owns the client connected to the internet
            person_name = client_name[0: client_name.index("'")]

            # if the person has not been recorded yet and the device is personal, then add them to the list of people in the building
            if person_name not in people_names and 'Personal' in client_name:
                # adding person's name to the list of people in the building
                people_names += '\n' + person_name

    return people_names

# end of function getPeoplePresent(dict_name, data)

# the driving function of this script, this calls all other functions
def startScript():

    # boolean that holds the value of whether the network is currently down or not, False by default, can change depending on what the script finds about the network
    network_issue = False

    # integer that holds how many times in a row the script has ran and the network has still had an issue, 0 by default
    issue_count = 0

    while True:

        # the text that will appear in the Twilio message, blank by default (except for header), text will be added as the script runs
        twilio_body = 'Unifi Script Results:\nDate: ' + getCurrentDateTime() + '\n\n'

        # calls function to see if network is up
        network_status = getNetworkStatus()

        # creates folder with date name (if it doesn't already exist) where the excel and text files will be held, True == folder was created, False == folder already existed
        date_folder_created = createDateFolder()

        # if the date folder was just created, then it must be a new day, meaning the folder with the previous date must be zipped
        if date_folder_created == True:

            print("Creating Zip Folder...")
            # creates a ZIP folder of the log files from the previous day
            createZipFolder()

        # if the network is up
        if network_status == True:
            # adding to the body of the Twilio message if the network is up
            twilio_body += "Network is UP.\n\n"

            # calls function to retrieve network information since the network is up, will send a Twilio message if there is a change in the network's status compared to the network's status of the previous run through of the script
            network_issue, issue_count, devices_data, clients_data = getNetworkInfo(twilio_body, network_issue, issue_count)

            # variable that holds a list of the headers for the Excel sheet
            devices_headers = ['Name', 'MAC Address', 'IP Address', 'Status', 'Model', 'Version', 'Uptime', 'Memory Usage', 'CPU Usage', 'Clients', 'Download', 'Upload', 'Wlan2g', 'Wlan5g', 'Clients2g', 'Clients5g', 'Experience2g', 'Experience5g', 'BSSID', 'TX', 'RX', 'Channel']

            # variable that holds a string that will be at the start of the filename (to differentiate between clients and devices
            devices_file_name_beginning = 'device'

            # creates Excel sheet for devices
            createExcelFile(devices_data, devices_headers, devices_file_name_beginning)

            # variable that holds a list of the headers for the Excel sheet
            clients_headers = ['Name', 'Hostname', 'MAC Address', 'IP Address', 'Connection', 'Wifi Experience', 'Status', 'AP/Port', 'Channel', 'WiFi Connection', 'Signal', 'RX Rate', 'TX Rate', 'Download', 'Upload', 'Uptime', 'Vendor', 'Type', 'Category', 'OS Name']

            # variable that holds a string that will be at the start of the filename (to differentiate between clients and devices
            clients_file_name_beginning = 'client'

            createExcelFile(clients_data, clients_headers, clients_file_name_beginning)

            # indicating what the beginning of the text file should say
            text_file_name_beginning = 'peoplePresent'

            # indicating what the name of the objects are within the dictionary (so that we can properly get the people present in the building)
            dict_name = 'client'

            # creating text body showing the people in the office
            text_body = 'People currently present on network:' + getPeoplePresent(dict_name, clients_data)

            # creating text file saying who is currently in the building
            createTextFile(text_file_name_beginning, text_body)

        # if the network is down
        else:
            # add to the count of how many times in a row an issue has occurred
            issue_count += 1

            # if the network was not down previously, then send out a message and indicate that it is now having issues
            if network_issue == False:
                # the text that will appear in the Twilio message if the script detects the network is down
                twilio_body += "Network is DOWN. The Network Admin laptop cannot connect to the Internet, indicating a problem at the network's source.\n\nThe issue(s) with the network just occurred.\n\n" + getAnyDeskInfo() + "\n\nThis message was sent using the Verizon Hotspot connected to the Network Admin laptop."

                # switch to WiFi or a hotspot since the LAN appears to be down
                switch_successful, network_connected_to = switchToWiFi()

                if switch_successful == True:

                    twilio_body += '\n\nThis message was sent through ' + network_connected_to + ', not LAN.'

                    # send message about the network being down
                    sendTwilioMessage(twilio_body, "numbers.txt")

                    # disconnect from the WiFi/hotspot, which automatically reconnects the laptop back to LAN
                    os.system("netsh wlan disconnect")

                else:
                    print("There was an error sending the Twilio message")

                # indicate that the network is down
                network_issue = True

            # if the issue has occurred for hourly, indicate how many hours the network has persisted with an issue
            elif issue_count % 12 == 0:
                #indicate the number of hours an issue has persisted
                twilio_body += "Network is DOWN. The Network Admin laptop cannot connect to the Internet, indicating a problem at the network's source.\n\nThe issue(s) with the network have lasted " + str(issue_count / 12) + " hour(s).\n\n" + getAnyDeskInfo() + "\n\nThis message was sent using the Verizon Hotspot connected to the Network Admin laptop."

                # switch to WiFi or a hotspot since the LAN appears to be down
                switch_successful, network_connected_to = switchToWiFi()

                if switch_successful == True:

                    twilio_body += '\n\nThis message was sent through ' + network_connected_to + ', not LAN.'

                    # send message about the network being down
                    sendTwilioMessage(twilio_body, "numbers.txt")

                    # disconnect from the WiFi/hotspot, which automatically reconnects the laptop back to LAN
                    os.system("netsh wlan disconnect")

                else:
                    print("There was an error sending the Twilio message")

            # info for the Excel workbook that will show the network was down while this script was running
            network_down_headers = ['NETWORK DOWN']
            network_down_data = ["Network is down so no data could be gathered at this time."]
            network_down_file_name_beginning = 'NETWORKDOWN'

            # creating Excel sheet
            createExcelFile(network_down_data, network_down_headers, network_down_file_name_beginning)

            # indicating what the beginning of the text file should say when the network is down
            text_file_name_beginning = 'NETWORKDOWN'

            # creating text body for when the network is down
            text_body = 'Unable to determine the people on the network as the network is currently down.'

            # creating text file saying that the script is unable to determine who is in the building
            createTextFile(text_file_name_beginning, text_body)

        #prints to the console when the script finished, indicates if there was a network issue or not
        print("Script finished processing at: " + getCurrentDateTime() + " Network Issue? " + str(network_issue))

        # wait to run script again for 1 minute
        time.sleep(60)

# end of function "startScript()"

# THE VERY BEGINNING OF THE SCRIPT STARTS HERE

# initial call that starts the entire script, will loop endlessly
startScript()
