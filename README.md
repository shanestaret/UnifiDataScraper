# Unifi Data Scraper
This is a project written in Python that collects data about the Unifi Access Points (APs) connected to an internal network and data about the clients that are currently using the Unifi Access points. This program also determines if the network is online or if one of the APs appears to be malfunctioning.

### Explanation & Use
Essentially, this program monitors the status of an internal network that uses Unifi Access Points (APs). This program determines if the entire network is online and if the individual APs on the network are functioning as expected. The script gathers data about every AP (number of clients, CPU usage %, memory usage %, IP address, etc.) and also about every client connected to each AP (IP address, hostname, uptime, OS name, upload rate, download rate, etc.) in two Excel files. A text file is created that holds the name of every person on the network, based on the name of the device within the Unifi Controller. So, three files are created each time the script runs (the script loops endlessly) and the files are put into a folder that corresponds to the current date. Once a new day begins, the folder with the date of the previous day is compressed and a new folder with the current date is created. If the network is down, or if one of the APs appears to be malfunctioning, a text is sent through Twilio to the phone number(s) specified in the "numbers.txt" file. This text contains information about which AP could be malfunctioning or information about the entire network appearing to be offline. This program was designed so that a Verizon Hotspot would constantly be within connecting range, so that if the network appears to be entirely offline, the device running this script would automatically connect to the Verizon Hotspot to send the Twilio message about the network being offline. The script loops endlessly and every time it runs, a message is printed to the console indicating the time that the script finished running and an indicator if the script identified any network issues. This program is entirely written in Python and makes use of Selenium Webdriver.

### Potential Improvements
I would improve this code by expanding its functionality. I believe this could be used effectively as a clock-in/clock-out system. Each employee could be assigned a small FOB or other device that automatically connects to the network. As long as the employee has this device on them while they are in the building, the network can check for this specific device to determine if the employee is at work. Once the device is first detected on the network, the employee is clocked in automatically. Once the device is detected as no longer being on the network, the employee is automatically clocked out.

In terms of improving the actual code, I would recreate the code using an object-oriented mindset. Unfortunately, Python is not a language that fits well within the object-oriented paradigm, however, it was the most viable solution for this specific script because of how powerful Selenium Web Driver is. You can implement classes within Python and I did so in this program. However, I did not make great use of the object-oriented functionalities that Python contains. I simply stored data members within the two objects that I defined (AP devices and clients) and I did not establish functions specific to each class. Looking back through the code, greater efficiency and code readability could have been achieved if I properly defined the two major objects in the program to have the correct data members AND functions.

Also, there are too few methods. Some of the methods in this program are too long and they could have been separated into multiple methods. Methods should primarily do ONE task, not multiple. By having a method be responsible for multiple tasks, you increase its complexity and inhibit its ability to be reused. If I were to redesign this application, I would be sure to try to break up some of the larger methods into multiple small ones to improve the overall code structure.

I am proud of what this program accomplishes and I also would like to highlight how well I commented the code.
