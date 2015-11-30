# coding=utf-8
#!/usr/bin/python
from plotting import *
import math
from numpy import *
from heat_equation import *
from heat_equation_numpy import *
from heat_equation_cython import *


def get_heat(f, m, n, nu, verbose):
	"""Calculates and returns a new f based on f, m, n and nu.
	Used for testing() """
	if verbose: print "Calculating new heat source..."
	for i in range(0, m-1):
		for j in range(0, n-1):
			f[i][j] = nu*((2*pi/(n-1))**2+ (2*pi/(m-1))**2) \
			*sin(2*pi/(m-1)*i)*sin(2*pi/(n-1)*j)
	return f

def get_analytic(m, n, verbose):
	"""Calculates and returns an analytic_u based on m and n """
	analytic_u = zeros((m,n))
	if verbose: print "Calculating analytic u..."
	for i in range(0, m-1):
		for j in range(0, n-1):
			analytic_u[i][j] = sin(2*pi/(m-1)*i)*sin(2*pi/(n-1)*j)

	return analytic_u

def testing(t0, t1, dt, m, n, u, f, verbose, img):
	""" Performs test to check if formula is mathematically correct,
	and prints an error value based on u - analytic_u."""	
	nu = 1
	f_new = get_heat(f, m, n, nu, verbose)
	analytic_u = get_analytic(m, n, verbose)
	null = zeros((m,n))

	print "Running test. This might take a while..."
	u = heat_equation_numpy(t0, t1, dt, n, m, nu, null, f_new, verbose)
	
	err = (abs(u - analytic_u)).max()
	print "Error val: {:.6f}".format(err)

	if verbose: print "Plotting data..."
	plot_data(u, analytic_u, img)

	

