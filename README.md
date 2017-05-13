# dict.cc Dictionary Generator for MacOS

![Screenshot](screenshot.png)

<br/>
This is a Python script to create a MacOS (OS X) dictionary from dict.cc word lists. The generated dictionary is a regular dictionary for the MacOS stock Dictionary app, which means you can also look up words using Sportlight or anywhere via 3-Finger-Tap.

<br/>
<br/>
The dictionary itself can be downloaded from (Link)

<br/>
<br/>
Currently the following languages are available (built in May 2017):

- German - English
- German - Spanish
- German - French
- German - Icelandic
- German - Italian
- German - Swedish
- German - Russian
- German - Portugese

<br/>
<br/>

## Installation

Download a dictionary or build one by yourself (build instructions see below).<br/>
Double click the dictionary (.pkg) and follow the installer 
Open the Dictionary app</br>
Go to Preferences<br/>
Activate the dictionary by checking the checkbox (the new dictionary will be at the bottom of the list)


<br/>
<br/>

## Build Instructions

Get dict.cc word list<br/>
http://www1.dict.cc/translation_file_request.php<br/>
copy to project root<br/>
rename to "de-en.txt" for example<br/>

Apple Dictionary Developer Kit<br/>
https://developer.apple.com/download/more/<br/>
"Additional Tools for Xcode 8.2"<br/>
open .dmg<br/>
Utilities/Dictionary Development Kit<br/>
copy to /Developer/Extras/Dictionary Development Kit<br/>

Run Python build script (written in Python 2)<br/>
for example: python createpackages.py -d de-en.txt DE-EN "Deutsch-Englisch (dict.cc)"

<br/>

## Project Credits

Bernhard Caspar<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;https://github.com/bernhardc/dictcc-macos-dictionary

Philipp Brauner/Lipflip<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;https://lipflip.org/articles/dictcc-dictionary-plugin<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;https://lipflip.org/node/2096
   
Wolfgang Reszel<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;http://www.tekl.de/deutsch/Lexikon-Plugins.html
   

	
## License
This project is released under GPL license


