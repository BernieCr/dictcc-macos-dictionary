#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Warning:
#  This is my first dive into Python. There is much room for improvement. :)
#  Some parts are implemented in a rather ugly manner.
#  Philipp Brauner  - lipflip.org
#  Wolfgang Reszel - www.tekl.de 

import sys, re, string, codecs, datetime, os, locale, urllib, argparse, cgi, locale

#
# Global variable for storing the command line arguments
arguments = ''

#
# statistics -- displayed during make
statistics = {'indexkeys': 0, 'entries': 0, 'variants': 0, 'elements': 0}

#
# initialize an empty dictionary
dictionary = {}

#
# URL for update checking
creationDate =  str(datetime.date.today())
checkVersionURL= "http://lipflip.org/dictcc?date="+creationDate


def thousandsseparator (number):
    return re.sub(r'(\d{3})(?=\d)', r'\1.', str(number)[::-1])[::-1]
#
#
#   Main fuction.
#   Handles parameter parsing and appropriate execution of the various steps in the tool chain
#
def main(argv):
    print("dict.cc to Dictionary.app XML Converter - $Id$")
    print("    Version 2.9")
    print("    Philipp M. Brauner -  lipflip.org")
    print("    licensed under the GLP")
    print("    http://lipflip.org/articles/dictcc-dictionary-plugin")
    
    parser = argparse.ArgumentParser(description="dict.cc to Dictionary.app XML Converter")
    
    parser.add_argument('-d', '--debug', action='store_true', dest='debug', default=False, help='Enables debug output')
    parser.add_argument('-x', '--subset', action='store_true', dest='generatesubset', default=False, help='Creates much smaller packages with a random subset of words')
    parser.add_argument('-e', '--encoding', action='store', dest='encoding', default='utf_8', help='Character encoding of input file (default UTF8)')
    
    parser.add_argument('-v', '--version', action='store', dest='osxversion', default='10.5', help='required OS X version (packages for 10.6 are smaller) (default 10.5)')

    parser.add_argument('filename', type=str, action='store', default="DE-EN.txt", help='Language package to create (e.g. "DE-EN.txt")')
    parser.add_argument('shortname', type=str, action='store', default="DE-EN", help='Short name of language package to create (e.g. "DE-EN")')
    parser.add_argument('longname', type=str, action='store', default="Deutsch-Englisch by dict.cc", help='Long name of language package to create (e.g. "Deutsch-Englisch dict.cc")')
    parser.add_argument('-tempfile', type=str, action='store', default="dictionary.xml", help='Temporary file')
    
    global arguments
    arguments = parser.parse_args()
    
    
    # DE-IT -> dtit.dict.cc -> Will work for online lookups
    if(string.upper(arguments.shortname)=="DE-EN"):
        arguments.urlprefix = ""
    else:
        arguments.urlprefix = string.replace(string.lower(arguments.shortname), '-', '') + '.'

    # Fix encoding of long title (e.g. make Deutsch FranzÖsisch work)
    #u = unicode('abcü', 'iso-8859-1')
    arguments.longnameencoded = "%s".encode('iso-8859-1') % unicode(arguments.longname, 'iso-8859-1')


    if(arguments.debug):
        print "Debug:     ", arguments.debug
        print "Subset:    ", arguments.generatesubset
        print "Filename:  ", arguments.filename
        print "Tempfile:  ", arguments.tempfile
        print "URLPrefix: ", arguments.urlprefix
        print "Shortname: ", arguments.shortname
        print "Longname:  ", arguments.longname
        print "Encoding:  ", arguments.encoding
        print "OSXVersion:", arguments.osxversion

    # enable printing of unicode strings without using .encode() millions of times
    print("Switching sys.stdout to utf-16...")
    sys.stdout = codecs.getwriter("utf-16")(sys.stdout);
    print(" switched!")

    global checkVersionURL
    checkVersionURL = "http://lipflip.org/dictcc?date="+creationDate+"&lang="+arguments.shortname

    
    readVocabulary(arguments.filename)
    generateXML(arguments.tempfile)
    
    createPlist()
    createDictionary()
    createPackage()
    
    
def createPackage():
    print("Creating installation package")
    
# todo
#	@/Developer/Applications/Utilities/PackageMaker.app/Contents/MacOS/PackageMaker -d $(PMDOC_NAME) -o $(DICT_NAME)_$(DATE).pkg
#	@echo "- Zipping Install Package."
#	@zip $(DICT_NAME)_$(DATE).zip -9 -o $(DICT_NAME)_$(DATE).pkg 
#	@echo "Done."
#	@echo "Execute '$(DICT_NAME) $(DATE).pkg' to install the dictionary."
	

def updateInPreferences():
    global statistics, arguments, checkVersionURL
    checkUpdateImage = 'http://tools.lipflip.org/dict.cc/updateimage.php?date='+creationDate+'&amp;lang='+arguments.shortname
    checkUpdateURL = 'http://tools.lipflip.org/dict.cc/update.php?date='+creationDate+'&amp;lang='+arguments.shortname+'&amp;mode=preferences'

    s = '<strong>' + arguments.longnameencoded + '</strong><br />'
    s += '<p>This dictionary is based on the vocabulary database from http://dict.cc/.<br />'
    s += 'It was generated on ' + datetime.date.today().strftime('%A, %B %d %Y') + ' and contains ' + str(thousandsseparator(statistics['entries'])) + ' entries.</p>'
    
    s += '<p>The copyright for the vocabulary database is held by Paul Hemetsberger and the dict.cc community. Philipp Brauner (lipflip.org) converted the database into a format suitable for OS X and wrote a series of tools to do so. Parts of his work were inspired by Wolfgang Reszel (tekl.de) and his Beolingus plugin.</p>'

    # Primitive Update-Funktionalität
    #  - link, der auf mini-update-seite springt 

   # s += '<p><a href="' + checkUpdateURL + '">Click here to check for updates.</a></p>'
    
    #  - Update image  (works, but currently not active due to privacy concerns
    # s += '<p><img src="'+checkUpdateImage+'" width="320" height="60" alt="Visual update indicator [loading...]" /></p>'
    s += '<p>For more information visit</p>'
    s += '<p>http://tools.lipflip.org/dict.cc/</p>'

    if(arguments.debug):
        print s
    
    return s

def createPlist():
    global arguments
    print("Creating plist")
    
    output = codecs.open("dictcc.plist","w","utf-8")
    output.write(u'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleDevelopmentRegion</key>
	<string>German</string>
	<key>CFBundleIdentifier</key>
	<string>com.apple.dictionary.dictcc</string>
	<key>CFBundleName</key>
	<string>%s</string>
	<key>CFBundleVersion</key>
	<string>%s</string>
	<key>CFBundleShortVersionString</key>
	<string>%s</string>
	<key>DCSDictionaryCopyright</key>
	<string>%s</string>
	<key>DCSDictionaryManufacturerName</key>
	<string>Paul Hemetsberger, dict.cc / Philipp Brauner, lipflip.org / Wolfgang Reszel, www.tekl.de</string>
	<key>DCSDictionaryFrontMatterReferenceID</key>
	<string>front_back_matter</string>
</dict>
</plist>
''' % (arguments.shortname, str(datetime.date.today()), str(datetime.date.today()), '<![CDATA['+updateInPreferences()+']]>' ) )


def createDictionary():
    global arguments
    print "Calling external script to create dictionary"
    # -v 10.5 -> bigger packages
    # -v 10.6 -> smaller packages
    # arguments.osxversion
    command = string.join(["/Developer/Extras/Dictionary\ Development\ Kit/bin/build_dict.sh", "-v 10.6", '"'+arguments.longname+'"', arguments.tempfile, "dictcc.css", "dictcc.plist"], " ")
#    print "% "+ command
    os.system(command)
    
#
#   styles meta information of dictionary entries (e.g. "{colloq.}")
def style(text):
    text = re.sub('(\{[^}]+\})', r' <i>\1</i>',text)
    text = re.sub('(\([^)]+\))', r' <span id="a">\1</span>',text)
    text = re.sub('(\[[^]]+\])', r' <span id="b">\1</span>',text)
    return text


#
# calculates an index-key and adds the entry to the dictionary
# multiple translations and annotated terms are stored in one entry
# INDEX: term
#	term: [trans1, trans2, tras3]
#   term (umgs.) : [trans4]

def addEntry(word, definition, entryType):
	global dictionary;
	
	# normalization
	# prepare index string // remove all kinds of additional descriptions
	index = word
	if index.startswith("to "): index =  index[3:] # strip (to)
	index = re.sub('(\([^)]+\))', r'',index)
	index = re.sub('(\{[^}]+\})', r'',index)
	index = re.sub('(\[[^]]+\])', r'',index)
	index = re.sub('  ', r' ', index) # remove
	index = index.strip()   # .lower()
	index = index.lower()
	if index.endswith("-"): index = index[:-1]
   
	definitionx = definition
	if entryType!='': definitionx = definition + '(' + entryType + ')'

	# nothing left to be used as an index (e.g. entries like sayings) 
	if len(index)<1:
		raise NameError
	
	#dictionary[index][entries]	 -> 
	#dictionary[index][entryType][entries]

	# get entry from dictionary	
	if dictionary.has_key(index):
		entry = dictionary[index]
	else:
		entry = {}      # not found? create new entry
		
	#if entry.has_key(entryType):
#		subentry = entry[entryType]
#	else:
#		subentry = {}

	# add translation to entry 
	if entry.has_key(word):
		entry[word].append(definitionx)
	else:
		entry[word]=[definitionx]
		
	#entry[entryType] = subentry

	# store entry in dictionary
	dictionary[index] = entry;


#
# reads a data file and add terms to dictionary
def readVocabulary(filename):
    lines=0
    comments=0
    errors=0
    try:
        input = codecs.open(filename, "r", arguments.encoding)
    except IOError:
        print '*** File "' + filename + '" not found or other error.'
        return False
    else:
        print 'Processing "'+filename+'"'
        for line in input:
            lines=lines+1

            if(arguments.generatesubset):
                if(lines>3000):
                    break
            # trow away comments or empty lines
            if (line[0]=="#") or (len(line)<=2):
                comments=comments+1
                continue

            # throw away my email address
            if (re.search('lipflip', line) or re.search('herun7erg', line)):
                if arguments.debug:
                    print "  Found fingerprint: " + line
                continue

            # remove incompatible characters
            line = line.replace("<","&lt;")
            line = line.replace(">","&gt;")
            line = line.replace("&","&amp;")

            # split entry into english and german part 
            data = line.split("\t", 2);
            if len(data)<2:
                errors = errors+1
                if arguments.debug:
                    print "Error: "+line
                continue

            left = data[0].strip();
            right = data[1].strip();
            entryType = "";
            if len(data)>=3:
                entryType = data[2].strip();
               


            # fix quotes
#           left  = re.sub('"([^"]+)"',r'„\1“'.decode("utf-8"), left)  # dt. anführungsstriche
#           right = re.sub('"([^"]+)"',r'“\1”'.decode("utf-8"), right)  # engl. anführungsstriche
            left = left.replace('"', "")
            right = right.replace('"', "")
#           if (left1!=left) or (right1!=right):
#               print "PANIC! " + line
#               raise NameError

            # ok... add to dictionary
            try:
                addEntry(left, right, entryType);
            except:
				dsfsf=5
                #if arguments.debug:
                   # print "addEntry('%s', '%s', '%s') failed!" % (left, right, entryType)
                #errors =  errors+1
            try:
                addEntry(right, left, entryType);
            except:
				dsfsf=5
                #if arguments.debug:
                   # print "addEntry('%s', '%s', '%s') failed!" % (right, left, entryType)
                #errors =  errors+1

        input.close
        print("")
        print("  Read %s lines with %s comments. Errors: %s" % ( lines, comments, errors) )
        print("  %s unique pages in dictionary (probably)." % len(dictionary))
        
        return True


#
#  generate a search query url for the current entry
#  TODO - convert title to a valid url
#  spaces -> "+"
#  überholen -> s=%FCberholen 
def generateSearchQuery(title):
    global arguments
#    encodedTitle = urllib.quote_plus(title.encode('cp1252'))
    return "http://"+arguments.urlprefix+"dict.cc?s="+title


#
# generate a set of keys in the index
# to download -> { to download, download }
def generateIndexEntries(entry):
    def fix(text):
        text = re.sub('  ', r' ', text) # remove dublicate spaces
        text = text.strip()
        return text
 
    # create empty set and add several keys 
    indexKeys = []
    variants = []

    # make a copy...
    text = entry
    
    # remove  additional descriptions
    text = re.sub('(\{[^}]+\})', r'',text)
    text = re.sub('(\[[^]]+\])', r'',text)
    
    # remove info "(ganz) gewöhnlich" => "gewöhnlich"
    reducedText = re.sub('(\([^)]+\))', r'',text)
    variants.append(reducedText)
    
    # if something was changed add alternative: "(info) blupp -> info blupp" (without braces)
    if (reducedText != text):
        extendedText = re.sub('\(([^)]+)\)', r'\g<1>', text)
        variants.append ( extendedText )


    # loop through variants and add normalized keys
    for variant in variants:
        indexKeys.append(fix(variant))
        if variant.startswith("to "): indexKeys.append(fix(variant[3:]))  # download -> download, to download

    return indexKeys


#
#  renders an entry to XML
#  ID: unique number
#  index: dictionary entry
def renderEntry(ID, index):
    global dictionary
    global statistics
    entry = dictionary[index]
    
    # unique entry id
    ID = str(ID)
    
    # duh. that's a bit to simple
    # TODO
    title = index;

    
    # generate a set of index keys for this entry
    indexKeys = []
    for term in entry.keys():
        indexKeys.extend(generateIndexEntries(term)) 
    
    # throw out dublicate entries
    indexKeys = set(indexKeys)
    
    #print 'Index keys generated for "'+title+'":'
    #for indexKey in indexKeys:
    #   print '  ' + indexKey   

    #
    # CREATE HTML ENTRY 
    #
    
    # start with title
    s = '<d:entry id="' + ID + '" d:title="' + title +'" >\n'
    statistics['entries']+=1

    # add generated inddexKeys
    for indexKey in indexKeys:
        statistics['indexkeys']+=1
        s+= '<d:index d:value="' + indexKey +'"/>'

    # loop through several spellings
    for term in entry.keys():
        statistics['variants']+=1

        sub ='<h1>'+style(term)+'</h1>'
        
        sub+="<ul>"
        for element in entry[term]:
            statistics['elements']+=1
            sub+="<li>"+style(element)+"</li>"
        sub+="</ul>"

        s+=sub
        
    # add a footer
    s+='<div id="f">'
    
    # URL for online query
#    s+='on <a href="'+generateSearchQuery(title)+'">dict.cc</a>'   

    s+='<a href="'+generateSearchQuery(title)+'">lookup online</a>'   

    s+=' | <a href="x-dictionary:r:front_back_matter">About</a>'
    # check version link
#    s+=' | <a href="'+checkVersionURL+'">Update?</a> '
    s+='</div>'
    
    s+='</d:entry>\n\n'

    return s

# Generate XML output
def generateXML(filename):
    print "Generating XML output"
    global statistics, arguments, dictionary, arguments, checkVersionURL

    # prepare output
    if (arguments.debug):
        print "  Filename: " + filename
    output = codecs.open(filename,"w","utf-8")

    # XML Header
    output.write(u'''<?xml version="1.0" encoding="UTF-8"?>
<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">\n''')
  
  
    # Primitive Update-Funktionalität
    #  - link, der auf mini-update-seite springt 

    checkUpdateURL = 'http://tools.lipflip.org/dict.cc/update.php?date='+creationDate+'&amp;lang='+arguments.shortname

    # process each dictionary term
    count = 0
    for term in dictionary.keys():
        count = count + 1
        output.write(renderEntry(count, term))       
    # front matter
    if arguments.debug:
        print "  Vordere/hintere seiten anlegen..."

#<d:index d:value="Vorwort (dict.cc-plugin)"/>
#<d:index d:value="Lizenz (dict.cc-plugin)"/>
#<d:index d:value="Copyright (dict.cc-plugin)"/>
#<d:index d:value="dict.cc"/>
#<d:index d:value="update (dict.cc-Plugin)"/>
    
#    u = unicode('abcü', 'iso-8859-1')
#    encodedlongname = "%s".encode('iso-8859-1') % u
    
    output.write(u'''
<d:entry id="front_back_matter" d:title="Vorwort">


    <h1>dict.cc Wörterbuch %s</h1>
    <p>Dieses Wörterbuch stammt aus dem von Paul Hemetsberger angebotenen Online-Wörterbuch <a href="http://www.dict.cc">www.dict.cc</a>, das seinerseits auf der Wortliste von <a href="http://dict.tu-chemnitz.de/">dict.tu-chemnitz.de</a>, sowie der Mitarbeit zahlreicher Benutzerinnen und Benutzer von dict.cc basiert.</p>
    <p>Die Werkzeuge zur Erstellung eines Plugins für Dictionary.App/Lexikon wurden von <a href="http://lipflip.org/articles/dictcc-dictionary-plugin">Philipp Brauner</a> entwickelt und durch die Integration eines ähnlichen Tools von <a href="http://www.tekl.de/">Wolfgang Reszel</a> erheblich verbessert.</p>
    <p>Dieses Wörterbuch wurde am %s erstellt und enthält %s Einträge (<a href="%s">Nach Aktualisierungen suchen</a>).</p>
        <p>Weitere aktuelle Informationen finden sie hier:<br /><a href="http://tools.lipflip.org/dict.cc/">http://tools.lipflip.org/dict.cc/</a>.</p>
<p></p>
    <p><h1>Lizenz:</h1>
Nutzungsbedingungen der Übersetzungsdaten von dict.cc<br />
Stand vom 11. Februar 2005<br />
Die Bezeichnung "die Daten" steht für die Inhalte der Datenbank, die auf den Seiten und in den Dateien auf www.dict.cc zur Verfügung gestellt wird, sowie für Auszüge daraus.<br />
<br />
PERSÖNLICHER GEBRAUCH<br />
Die Nutzung der Daten für den persönlichen Gebrauch ist gestattet, solange die Daten nicht weitergegeben oder veröffentlicht werden.<br />
<br />
VERWENDUNG IN COMPUTERPROGRAMMEN<br />
Die Verwendung der Daten in Computerprogrammen ist erlaubt, wenn folgende Bedingungen eingehalten werden:<br />
Programme, die Daten von dict.cc verwenden, müssen der GPL unterliegen.<br />
Das heißt unter anderem, dass der Quellcode des Programms der Allgemeinheit zur Weiterverwendung zur Verfügung gestellt werden muss.<br />
Die Übersetzungsdaten selbst dürfen nicht mit dem Programm mitgeliefert werden, sondern der Benutzer muss aufgefordert werden, die benötigte Datei für den eigenen Gebrauch direkt von dict.cc herunterzuladen. Dadurch wird gewährleistet, dass jeder Nutzer der Daten diese Lizenzbestimmungen gesehen und akzeptiert hat.<br />
Das Programm darf nicht dazu bestimmt oder geeignet sein, die Daten im Internet zu veröffentlichen, auch nicht auszugsweise.<br />
<br />
SONSTIGE VERWENDUNG<br />
Weitere Arten der Verwendung der Daten, insbesondere die Verwendung auf Webseiten, auch auszugsweise, bedürfen einer ausdrücklichen schriftlichen Genehmigung des Betreibers von <a href="http://dict.cc/">dict.cc</a>, Ing. Paul Hemetsberger.<br />
Die Verwendung der Daten im Zusammenhang mit Suchmaschinen-Optimierungstaktiken oder Spamming in jeglicher Form ist strengstens untersagt.<br />
<br />
WEITERE BESTIMMUNGEN<br />
Sämtliche Aspekte bezüglich der Übersetzungsdaten von dict.cc, die in diesen Bestimmungen nicht eindeutig behandelt sind, bedürfen einer schriftlichen Klärung vor einer eventuellen Verwendung. Bei Verstößen gegen diese Bedingungen behält sich der Betreiber von dict.cc rechtliche Schritte vor. Der Gerichtsstand ist Wien. Es gilt materielles österreichisches Recht.<br /></p>
</d:entry>
''' % (arguments.longnameencoded, datetime.date.today().strftime('%d.%m.%Y'), thousandsseparator(str(statistics['entries'])), checkUpdateURL)  )

    if(arguments.debug):
        print("  Closing dictionary xml...")
    
    # Finish up
    output.write(u'''</d:dictionary>\n''');
    output.close
    print ("  Wrote %s entries to '%s'" % (count, filename) )
    if(arguments.debug):
        print ("  Entries   : %s" % (statistics['entries']));
        print ("  Index keys: %s" % (statistics['indexkeys']));
        print ("  Variants  : %s" % (statistics['variants']));
        print ("  Elements  : %s" % (statistics['elements']));

if __name__ == "__main__":
    main(sys.argv[1:])
    