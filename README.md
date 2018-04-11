# glitch

A python script for creating glitch art 

Also can be used to corrupt data if you decide to do that

Usage: 
- There are currently two modes
- python glitchr.py [-o <output file name>] corrupt [-a <amount of bits to corrupt>] [-d <distance to move bits>] [-r] <input file name>
- python glitchr.py [-o <output file name>] overwrite <file to transplant bits from> [-a <amount of bits to transplant>] [-d <offset bits from file header (if file recognized)>] <input file name>
