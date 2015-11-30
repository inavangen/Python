#!/usr/bin/env python
# encoding: utf-8
""" Takes a single string as a input and runs te string as a python
command with basic functionality such as importing modules, creating 
variables and functions. Returns the string containing the output of
the command.
"""
import sys
from StringIO import StringIO
import traceback

namespace = vars().copy()
counter = 0
input_list = []
out_list = []

def get_input():
	"""Returns a list of previous input"""
	return input_list
def get_output():
	"""Retruns a list of previous output"""
	return out_list

def feedline(strin):
	""" Uses eval or exec on a input-string 'strin', and returns the 
	results. Function also handles enumeration of in and out. In- 
	and out is also saved (used i.e. by web-interfaces and mypython).

	Args:
		(strin): string containing user input.
	Returns:
		ret_string: string containing enumeration for new prompt
		and output.    	
	Raises:
		TypeError: if no arguments.

	Example usage:
	>>> feedline("x=123")
	>>> feedline("print x")
	out[2]: 123
	in [2]: 
   	"""
	global counter
	global input_list
	global out_list 
	
	oldio, sys.stdout = sys.stdout, StringIO()
	input_list.append(strin) # append input to list

	try:
		try:
			out = eval(strin, namespace)
			sys.stdout = oldio
		except:
			exec(strin, namespace)
			out = sys.stdout.getvalue()
			sys.stdout = oldio

		# Returns new prompt in addition to return string.	
		if strin == "":
			ret_string = "\nin [" + str(counter) +"]: "
		else:
			ret_string = "\nout[" + str(counter+1) +"]: " + str(out) + "\nin [" + str(counter+1) +"]: "
			counter += 1
		out_list.append(out) # append output to list
		return ret_string

	# Returns traceback if it's not possible to use eval or exec.
	# For example if variable is not defined.
	except:		 
		sys.stdout = oldio
		ret_string = "\nin [" + str(counter) +"]: "
		trace = traceback.format_exc()
		print trace
		out_list.append(trace)
		return ret_string
