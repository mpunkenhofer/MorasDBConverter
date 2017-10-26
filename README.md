# MorasDBConverter
Converts a .json daoc db to moras db format.
The .json database and metadata files can be found here: http://www.darkageofcamelot.com/content/downloadable-item-database (26.10.2017)
## Usage
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

## Acknowledgements 
Most items get converted. Craft Tradeskill items will not be converted (stat types 23-26 ... if you see corresponding converison errors [-e] ) 
Since this is the first version please report any bugs/errors you find in the converted moras database.
