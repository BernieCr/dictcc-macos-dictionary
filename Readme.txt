by Philipp Brauner/Lipflip 2008, licensed under the GLP
   lipflip@lipflip.org
   http://lipflip.org/articles/dictcc-dictionary-plugin
Partially by Wolfgang Reszel
   http://web.mac.com/tekl/deutsch/Wörterbücher.html

Installation:
1. Unzip dictcc-dictionary-distrib.zip. You already did this. Hooray!
2. Download and install the OS X Developer Tools from Apple.com.
   You'll need to join the Apple Developer Connection to do this (there's a
   free membership). You only need X-Code < 4.0 do build the dictionary so
   there's no need to buy (!) the most recent version of the developer tools.
3. Download dict.cc's database(s) in UTF-8 encoding and place it in the
   dictcc-dictionary-distrib directory.
   You only need one database for each language pair (e.g. DE-EN, EN-DE is not
   required).
4. Open a Terminal and "cd" to the dictcc-dictionary-distrib directory.
5. Launch the build script:
   user$ ./createpackages.py $filename $short $long
   Where $filename is the filename of the downloaded database, $shortname
   is the short name of your dictionary (e.g. "DE-EN"), and $longname is the
   long form of your dictionary's name (e.g. "Deutsch Englisch").
   
   user$ ./createpackages.py -dx DE-EN.txt DE-EN "Deutsch Englisch"
   
   There are some flags that toggle debug output (-d) or generate only a
   minimal subset of the dictionary (-x).
6. After some minutes or hours the dictionary can be found in
   ./objects/$longname.
   It can be installed by moving it into /Library/Dictionaries or
   /Users/$username/Library/Dictionaries/
7. Start/restart Dictionary.App.
8. Keep in mind that the license of dict.cc prohibits the distribution of the
   dict.cc database. Thus you are not allowed to distribute your dictionary.
9. The script is quite messy. Feel free to clean it up a bit. :) 


   Have fun!  Lipflip AT gmail.com
