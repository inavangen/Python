cimport cython
from libc.stdio cimport printf
@cython.boundscheck(False)
cpdef double[:,:] heat_equation_cython(double[:,:]u, double[:,:]f, double t0, double t1, double dt, int n, int m, double nu, verbose=False): 
	cdef int i, j
	cdef double[:,:] u_new = u
	while (t0 < t1):
		for i in range(0, m-1):
			for j in range(0, n-1):
				u_new[i, j] = u[i, j]+ dt*(nu*u[i-1, j] + nu*u[i, j-1] -4*nu*u[i, j]+ nu*u[i, j+1] + nu*u[i+1, j] + f[i, j])
			
		t0 +=  dt 
		u = u_new
		if verbose: printf("\rTimestep: %f2", t0)

	if verbose: printf("\n")
	return u_new
