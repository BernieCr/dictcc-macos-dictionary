
## Changelog

<br/>

2017-05-20 - v3.0 - Bernhard Caspar
- 1.404.624 entries in DE-EN
- Update build script to make it compatible with most recent dict.cc word list format
- Remove some non-printable characters from parsed word list that break dictionary generation
- Fix an issue where nested brackets in word definitions break dictionary generation
- Substantially improve indexing of words with prepositions ('unterhalten' now finds 'sich unterhalten', 'jdn./etw. unterhalten' etc.)
- Fine tune dictionary entry styling
- Improve build process in general
- Update info texts within dictionary and remove some broken references
- Add more metadata in order for dictionary entries to appear in Spotlight results
- Add MacOS installer .pkg generation to build script
- Fix some minor bugs in build script
- Successfully build dictionaries for the following language pairs:
  - German <-> English
  - German <-> Spanish
  - German <-> French
  - German <-> Icelandic
  - German <-> Italian
  - German <-> Swedish
  - German <-> Russian
  - German <-> Portuguese
  
2016-04-10 - (no public release) - Bernhard Caspar
- Restore compatibility with more recent dict.cc word lists
- Add word type (e.g verb, noun) to dictionary entries

2011-05-26 - v2.9 - Philipp Brauner/Lipflip
- 1.029.390 entries in DE-EN
- Uses tab separated input files
- added a link to the internal "about" page instead of a online access
        to lipflip.org (less anoying)    
- update link from front-back-matter and preferences dialog
- Supports input files in UTF8
- Supports multiple input languages
- handling of command line arguments
- packages for DE-EN and DE-IT
- some space saved (in DE-EN every byte in article-xml costs one MB) 
- link to lockup word online respects current package language (e.g.
        DE-IT package won't lookup in DE-EN)
        
2008-05-27 - Philipp Brauner/Lipflip
- Added Update check
- Added Link to dict.cc
- Added link to current entry
- aggregated mutliple entries to one page -> boosts widget experience
        the dictionary.app aggregates multiple simular entries automagically,
        the widget does not thus it's harder to lookup similar words 
- 528.637 entries in DE-EN
    
<br/>


