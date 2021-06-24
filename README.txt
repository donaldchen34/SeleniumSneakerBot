My attempt at making a Sneaker bot using selenium. 
The bot falls short at handling Captchas.
The main file is the GUI.py

CURRENTLY DOES NOT WORK


Setup

-Install selenium mozilla firefox driver and move it into main directory
https://github.com/mozilla/geckodriver/releases

-Install yolonet and move it into main directory
https://imageai.readthedocs.io/en/latest/detection/


Structure:
Database/ File Storage:
 ReadData.py
 FilePaths.py
 CreateDataFiles.py

FrontEnd:
 GUI - Load up the screens
 Screens/* - Folder for all the screens
   -> TaskScreen contains TaskHandler()

Backend:
 TaskHandler() - is Thread dispatcher for all tasks(TaskThread)
   -> TaskThread() The separate thread that runs Task()
       -> Task - calls the separate sites
 CaptchaSolver() - Auto Captcha Handler, uses imageai to find the correct images to select *** IN THE WORKS(not really) *** 
 
 
 
