#~ Website Screenshotter ~
#created by nizar / version 1.0
#contact: http://twitter.com/nizarneezR

#Usage:
# Run this script from DaVinci Resolve's dropdown menu (Workspace > Scripts)
# Select your project folder and paste a website URL into the text field
# A screenshot of the full website will automatically be taken as a .png-file with the highest available resolution, placed in your project folder and imported to your Media Pool!

#Install:
# Copy this .py-file into the folder "%appdata%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility"
# Install the python module 'selenium'
#	open cmd and execute 'pip install selenium' in the command line
#	or: install via requirements.txt with 'pip install -r requirements.txt'

import time
import os
import re
from tkinter import *
from tkinter import filedialog

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
except ModuleNotFoundError:
    root_errormsg = Tk()
    root_errormsg.wm_title("Nizar's Website Screenshotter for DaVinci Resolve")
    l_err_msg = Label(root_errormsg, text="Module 'selenium' not found!\n\n'Website Screenshotter' requires the external module 'selenium' in order to create a browser environment.\nPlease install selenium by opening the command line interface and running 'pip install selenium'.")
    l_err_msg.pack(side="top", fill="x", pady=10)
    l_ok_button = Button(root_errormsg, text="Okay", command=root_errormsg.destroy)
    root_errormsg.mainloop()


STANDARD_FILE_LOCATION = os.path.expandvars(r"%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\Website Screenshotter".replace("\\", os.sep))

filelocation = STANDARD_FILE_LOCATION

def screenshot_website(url, output_path, browser_name="chrome"):
    driver = get_browser_driver(browser_name)
    url = get_complete_url(url)

    driver.get(url)

    get_driver_win_size = lambda x: driver.execute_script('return document.body.parentNode.scroll' + x)
    driver.set_window_size(get_driver_win_size('Width'), get_driver_win_size('Height'))

    if not output_path.endswith(".png"): # error handling
        output_path += ".png"
    driver.find_element(By.TAG_NAME, 'body').screenshot(output_path)
    driver.quit()
    resolve.GetMediaStorage().AddItemsToMediaPool(output_path)
    os.startfile(filelocation, operation="explore")


def get_browser_driver(browser_name:str) -> webdriver.chrome.webdriver.WebDriver:
    browser_name = browser_name.lower()
    if browser_name not in ["chrome", "firefox", "edge"]:
        raise ValueError(f"Unsupported Browser '{browser_name}'")
    elif browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        driver = webdriver.Chrome(options=options)
        return driver
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        return driver
    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument('headless')
        driver = webdriver.Edge(options=options)
        return driver
    else:
        raise ValueError

def create_output_path(url: str):
    base_name = "scr_" + re.sub(r"^(https?://)?(www\.)?(\w{2}\.)?", "", url).split(".")[0]
    base_name = os.path.join(filelocation, base_name)

    file_path = base_name
    numeral_suffix = 1
    while os.path.isfile(file_path + ".png"):
        file_path = base_name + "(" + str(numeral_suffix) + ")"
        numeral_suffix += 1
    return file_path + ".png"

def get_complete_url(url: str):
    if not "." in url:
        return "" # don't open the website if invalid
    elif not re.match(r"^https?://.*",url):
        return "https://" + url
    else:
        return url

# GUI

def gui_scrshot_event():
    global l_entryField, l_downloadbutton, l_stdbrowser_button
    url = l_entryField.get()
    browser_name = l_stdbrowser_button.cget("text")

    if len(url) > 0:
        output_path = create_output_path(url)
        
        l_downloadbutton.configure(state=DISABLED, text="Downloading...")
        l_entryField.configure(state=DISABLED)
        try:
            screenshot_website(url, output_path, browser_name)
        except Exception as e:
            print(f"Error: {e}")
        l_downloadbutton.configure(state=NORMAL, text="Download")
        l_entryField.configure(state=NORMAL)
        l_entryField.delete(0, END)


def gui_change_filelocation_event():
    global l_filelocation_label, filelocation
    previous_filelocation = filelocation # resetting after canceling out the prompt window
    filelocation = filedialog.askdirectory()
    if not filelocation:
        filelocation = previous_filelocation
    l_filelocation_label.configure(text=filelocation)

def gui_reset_filelocation_event():
    global l_filelocation_label, filelocation, STANDARD_FILE_LOCATION
    filelocation = STANDARD_FILE_LOCATION
    l_filelocation_label.configure(text=filelocation)

def gui_change_default_browser():
    global l_stdbrowser_button
    current_browser = l_stdbrowser_button.cget("text")
    next_browsers = {"Chrome":"Firefox", "Firefox":"Edge", "Edge":"Chrome"}
    l_stdbrowser_button.configure(text=next_browsers[current_browser])

root = Tk()
root.title("Nizar's Website Screenshotter for DaVinci Resolve")
BG_COLOR = '#28282e'
FG_COLOR = '#cac5c4'
root.configure(background=BG_COLOR)


l_text = Label(root, text="Enter Website:", bg=BG_COLOR, fg=FG_COLOR)
l_text.grid(row=0, column=0, sticky="W", padx=20, pady=10)
l_entryField = Entry(root, width=50)
l_entryField.grid(row=1,column=0, sticky="W", padx=20)
l_downloadbutton = Button(root, text="Download", padx=50, command=gui_scrshot_event)
l_downloadbutton.grid(row=2, column=0, sticky="W", padx=20, pady=10)


l_filelocation_label = Label(root, text=filelocation, anchor="w", bg=BG_COLOR, highlightbackground = "gray", highlightthickness=2, fg=FG_COLOR)
l_filelocation_label.grid(row=4,column=0, sticky="W", padx=20, pady=(60,10))
l_filelocation_button = Button(root, text="Change download folder", padx=50, command=gui_change_filelocation_event)
l_filelocation_button.grid(row=5,column=0, sticky="W", padx=20)
l_filereset_button = Button(root, text="Reset download folder", padx=50, command=gui_reset_filelocation_event)
l_filereset_button.grid(row=5, column=1, sticky="W", padx=20)

l_stdbrowser_text = Label(root, text="Change browser mode:", bg=BG_COLOR, fg=FG_COLOR)
l_stdbrowser_text.grid(row=6, column=0, sticky="W", padx=20, pady=(60,10))
l_stdbrowser_button = Button(root, text="Chrome", padx=50, command=gui_change_default_browser)
l_stdbrowser_button.grid(row=7,column=0, sticky="W", padx=20)

root.mainloop()


