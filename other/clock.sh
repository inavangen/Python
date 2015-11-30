#!/bin/bash
# Oppgave 1.5 Eternal loop interrupted with Ctrl-C 

i=1

control_c()
{
	echo "Bye bye"
	exit $?
}

trap control_c SIGINT

while [ $i -lt 2 ] 
do
	date
done




	
