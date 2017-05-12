# dict.cc Dictionary Generator for MacOS 


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

Run Python 2 build script<br/>
for example: python createpackages.py -d de-en.txt DE-EN "Deutsch-Englisch (dict.cc)"

<br/>

## Project Credits

by Philipp Brauner/Lipflip 2008<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;lipflip@lipflip.org<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;https://lipflip.org/articles/dictcc-dictionary-plugin<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;https://lipflip.org/node/2096
   
Partially by Wolfgang Reszel<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;http://web.mac.com/tekl/deutsch/Wörterbücher.html
   
Additional work by Bernhard Caspar<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;https://github.com/bernhardc/dictcc-macos-dictionary
	
## License
This project is released under GPL license


