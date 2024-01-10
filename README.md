# ~ Website Screenshotter ~
Take screenshots of websites automatically and import them to DaVinci Resolve!

This captures the complete website in its full resolution, as it would appear in your web browser.

![WebsiteScreenshotter](https://github.com/neezr/Website-Screenshotter-for-DaVinci-Resolve/assets/145998491/e76c2018-7aa8-4063-97af-6b8a76a7b5fd)


## Usage:
- Run this script from DaVinci Resolve's dropdown menu (Workspace > Scripts)
- Select your project folder and paste a website URL into the text field
- A screenshot of the website will automatically be taken as a .png-file with the highest available resolution, placed in your project folder and imported to your Media Pool!

## Install:
- Copy the .py-file into the folder "%appdata%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility"
- *Windows Only:* Install Python 3.7+
- Install the python module 'selenium'
	- open 'cmd' on Windows and execute 'pip install selenium' in the command line
	- or: install via requirements.txt with 'pip install -r requirements.txt'
