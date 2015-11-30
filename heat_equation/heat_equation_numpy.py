# coding=utf-8
#!/usr/bin/python
from numpy import *
from test_heat import *

def heat_equation_numpy(t0, t1, dt, n, m, nu, u, f, verbose):
	""" Performs heat equation using numpy and 
	returns a new list(n x m)"""
	u = asarray(u)
	u_new = zeros((m,n)) 
	f = asarray(f)
	while (t0 < t1):
		u_new[1:-1, 1:-1] = u[1:-1, 1:-1]+ dt*(nu*u[:-2, 1:-1] \
			+ nu*u[1:-1, :-2] -4*nu*u[1:-1, 1:-1]+ nu*u[1:-1, 2:] \
			+ nu*u[2:, 1:-1] + f[1:-1, 1:-1])

		if verbose: print "\rTimestep: {}".format(t0),
		t0 += dt 
		u = u_new
	if verbose: print""
	return u_new