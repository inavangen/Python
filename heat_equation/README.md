#HEAT EQUATION 
Made by: Ina Vangen

#Introduction
This script shows a heat equation for a given heat source. The program demonstrates the different computation times between pure-python, numpy and cython, and shows that a different implementation might result in huge computational differences. 

More detailed documentation in report.tex and report.pdf

#Installation
Below follows some important guidelines how to use the script:

- To run script, run: heat_equation_ui.py

- Cython mode is selected as default. To change, add arguments in the command line: -type python or -type numpy (slower).
- Add -test to command line to OFF testing (testing is on by default.)
- If input file is chosen, dimension are overridden based on the dimensions of the input file.
- End time should be higher thant stat time.
- add --help to command line for more information about how specify the 
script using arguments from command line.
