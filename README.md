README.md

# DBC parser
- Parses dbc file and generates Java interfaces for:
	1. per frame Jva enum for all signals + attributes (factor,offset,initVal,min,max) 
	2.  All frames Cycle time + direction (Tx/Rx)

## How to use
- Update dbc_parser_constants.py with the required dbc paths (DBC_PATHS constant).
-  Run Generate_DBC_Java_files.py
