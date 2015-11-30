# coding=utf-8
#!/usr/bin/python
from test_heat import *
from numpy import *
import pyximport; pyximport.install()
import cython_calc

def heat_equation_cython(t0, t1, dt, n, m, nu, u, f, verbose):
	""" Performs heat equation using cython and 
	returns a new list(n x m)"""
	if verbose:	print "Starting heat equation calculaions."
	u_new = cython_calc.heat_equation_cython(array(u, dtype=float), 
		array(f,dtype=float), t0, t1, dt, n, m, nu, verbose)
	u_new = asarray(u_new)
	return u_new
	 