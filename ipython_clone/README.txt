Requirements
	- Flask must be installed in order to use the web-interface.
	- console.html must be located at path: /templates/

When feedline is run in ipython it returns funny output such as:
	In [5]: feedline("x=1")
	Out[5]: '\nout[2]: \nin [2]: '

	In [6]: feedline("print x")
	Out[6]: '\nout[3]: 1\n\nin [3]:

This is due to that the assingment text says that the "return value should be a string containing the output of the command run and the next prompt for the command after". This makes it prettier in the mypython and the web-interface version. Yet this could be fixed by removing parts of the retstring such as:

	ret_string = str(out)

instead of:

	ret_string = "\nout[" + str(counter+1) +"]: " + str(out) + "\nin [" + str(counter+1) +"]: "
