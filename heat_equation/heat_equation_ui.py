# coding=utf-8
#!/usr/bin/python
import time
import argparse
import timeit
from heat_equation import *	
from heat_equation_numpy import *
from heat_equation_cython import *
from test_heat import *
import pickle

def arg_parser(parser):
	"""Takes a parser as parameter and read sets up the heat equation
	parameters based on argumments from command line. Type --help for 
	information about valid arguments."""
	# TODO maybe remove nargs and action
	parser.add_argument('-n', nargs='?', type = int, default=50, help="Choose horizontal dimention of rectangle") 
	parser.add_argument('-m', nargs='?', type = int, default=100, help="Choose vertical dimention of rectangle") 
	parser.add_argument('-t0', nargs='?', type = int, default=0, help="Choose Start-time")
	parser.add_argument('-t1', nargs='?', type = int, default=1000, help="Choose End-time")
	parser.add_argument('-dt', nargs='?', type = float, default=0.1, help="Choose timestep")
	parser.add_argument('-nu', nargs='?', type = int, default=1, help="Choose thermal diffusity coefficient")
	parser.add_argument('-hs', nargs='?', type = int, default=1, help="Choose constant heat source")
	parser.add_argument('-input', nargs='?', default=False, help="write input") 
	parser.add_argument('-output', nargs='?', default=False, help="write output") 
	parser.add_argument('-type', choices=['python', 'numpy', 'c'], default='c',  help="Choose heat equation mode")	
	parser.add_argument('-img', action="store_true", default=False,  help="Turn on save plot as image-file.") 
	parser.add_argument('-t', action="store_true", default=False, help="Turn on timeit mode") 
	parser.add_argument('-v', action="store_true", default=False, help="Turn on verbose") 
	parser.add_argument('-test', action="store_true", default=False, help="Turn on test-mode") 
	args = parser.parse_args() 

	if(args.v):
		print "Turn on verbose-mode."
	if(args.t):
		if args.v: print "Turn on time-mode"
	if(args.img):
		if args.v: print "Turn on image-mode"

	if args.v: print """
Dimentions:\t {}x{}
Start-time:\t {}
End-time:\t {}
Timestep:\t {}
Thermal diff:\t {}
Heatsource:\t {}
	""".format(args.n, args.m, 
		args.t0, args.t1, args.dt, args.nu, args.hs,)

	return args.n, args.m, args.t0, args.t1, args.dt, args.nu, args.hs, \
	args.v, args.t, args.img, args.input, args.output, args.type, args.test

def read_input_file(argin, hs, n, m):
	""" Sets up initial temperature from an input file. a .dat file is
	required. If file is invalid, the scirps uses the selected/default
	heatsource and dimentions as initial temperature.""" 
	try: 
		with open(argin, "rb") as p:
			data_list_init =  pickle.load(p)
			print "Initial temperature set from file"
			# Update dimentions to the shape of the file.
			m = data_list_init.shape[0]
			n = data_list_init.shape[1]
			print "Updated dimensions to {}x{}".format(n,m)

	except: 
		print "Failed to load initial temperature data. Make sure the input file is a .dat file."
		data_list_init = [[hs for i in range(n)] for j in range(m)]

	return data_list_init, n, m

def write_output(argout, data_list):
	""" Takes a filename and a list of data as parameter
	Write data to output file. File should be a .dat file. """
	
	# TODO test pickle
	try:
		with open(argout, "wb") as p:
			pickle.dump(data_list, p)
			print "Saved output file as ", argout
	except: 
		print "Failed to dump output file. Make sure it is a .dat file."


def main():
	"""Calls argsparse, selects right mode, performs heat equation 
	and plotting. Also handles in- and output files."""
	parser = argparse.ArgumentParser(description='Heat equation')
	n, m, t0, t1, dt, nu, hs, verbose, timeit_mode, img, argin, argout, \
	argtype, argtest = arg_parser(parser)
	computation_time = 0

	# If input file was choosen, read and set heatsource.
	if argin:
		data_list_init, n, m = read_input_file(argin, hs, n, m)
	else: 
		data_list_init = [[hs for i in range(n)] for j in range(m)]

	# Sets heatsource and selecs right heat equation implementation.
	f = [[hs for i in range(n)] for j in range(m)]
	print "Running calculations. This might take a while..."
	if(argtype == "numpy"):
		if verbose: print "Numpy mode selected"
		data_list = heat_equation_numpy(t0, t1, dt, n, m, nu, 
			data_list_init, f, verbose)
		if timeit_mode: timer = timeit.Timer(lambda: 
			heat_equation_numpy(t0, t1, dt, n, m, nu, 
				data_list_init, f, verbose))
	elif(argtype == "c"):
		if verbose: print "C(Cython) mode selected ."
		data_list = heat_equation_cython(t0, t1, dt, n, m, nu, 
			data_list_init, f, verbose)
		if timeit_mode: timer = timeit.Timer(lambda: 
			heat_equation_cython(t0, t1, dt, n, m, nu, 
				data_list_init, f, verbose))
	elif(argtype == "python"):
		if verbose: print "python mode selected(default)"
		data_list = heat_equation(t0, t1, dt, n, m, nu, 
			data_list_init, f, verbose)
		if timeit_mode: timer = timeit.Timer(lambda: 
			heat_equation(t0, t1, dt, n, m, nu, 
				data_list_init, f, verbose))
	else:
		print "Error occured! This should not happen."

	# plotting and testing
	plot_data(data_list_init, data_list, img)
	
	# Check if testing is turned on
	if not argtest:
		runtest = testing(t0, t1, dt, m, n, data_list_init, f, 
			verbose, False)

	# Check if timeit is turned on
	if timeit_mode:
		print "Running timer ..."
		times = timer.repeat(repeat=5, number= 1)	
		print "Computation times: ", times
		print "Average: ", reduce(lambda x, y: x+y, times)/len(times)

	# If output file was choosen
	if(argout):
		write_output(argout, data_list)

if __name__ == "__main__":
	main()