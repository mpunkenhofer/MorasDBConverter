# MorasDBConverter
Converts a .json daoc db to moras db format.
The .json database and metadata files can be found here: http://www.darkageofcamelot.com/content/downloadable-item-database (2017-11-09)
## Version 1.1
## Usage
```
usage: MorasDBConverter.py [-h] [-o OUTPUT] [-e] [-i ID [ID ...]]
                           [-if IGNORE_FILE]
                           database metadata

Converts a .json daoc db to moras db format.

positional arguments:
  database              daoc item database file (.json)
  metadata              daoc item database metadata file (.json)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file name (moras database)
  -e, --errors          display conversion errors
  -i ID [ID ...], --ignore ID [ID ...]
                        ignore item(s) with a matching ID
  -if IGNORE_FILE, --ignore_file IGNORE_FILE
                        same as -i but parameter is a file which contains the
                        IDs
```
## Previous Versions
### Version 1.0
Most items get converted. Craft Tradeskill items will not be converted (stat types 23-26 ... if you see corresponding converison errors [-e] ) 
Since this is the first version please report any bugs/errors you find in the converted moras database.
#### Usage
```
usage: MorasDBConverter.py [-h] [-e] [-i INPUT] [-o OUTPUT] [-m METADATA]

optional arguments:
  -h, --help            show this help message and exit
  -e, --errors          display conversion errors
  -i INPUT, --input INPUT
                        input file name
  -o OUTPUT, --output OUTPUT
                        output file name
  -m METADATA, --metadata METADATA
                        metadata file name
```
