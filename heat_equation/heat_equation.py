# coding=utf-8
#!/usr/bin/python
from test_heat import *

def heat_equation(t0, t1, dt, n, m, nu, u, f, verbose):
	""" Performs heat equation using pure python and 
	returns a new list(n x m)"""
	if verbose:	print "Starting heat equation calculaions."

	u_new = [[0 for i in range(n)] for j in range(m)]
	
	while (t0 < t1):
		for i in range(1, m-1):
			for j in range(1, n-1):
				u_new[i][j] = u[i][j]+ dt*(nu*u[i-1][j] + nu*u[i][j-1] -4*nu*u[i][j]+ nu*u[i][j+1] + nu*u[i+1][j] + f[i][j])
			
		if verbose: print "\rTimestep: {}".format(t0),
		t0 += dt 
		u = u_new
	if verbose: print""
	return u_new

	

