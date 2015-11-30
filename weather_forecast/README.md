# WEATHER FORECAST
Made by: Ina Vangen

#Introduction
This program retrieves weather data from www.yr.no and returns the werather forecast for the selected place/time for the current or next day.

#Installation

- To run program type: python forecast.py (only works for places in Norway)

- extreme.py is an additinal script that simply finds the hottest and coldest places in Norway. Due to huge computation times the limit has been set to 100.


#Important
Due to buffer activity the program will create lots of text files in the same directory for every location searched for. This is to not overload the servers at yr.no. The program will only fetch new weather data if more than 6 hours has passed. Possible impovements would be to move these files to a subdirectory or used pickle to store all data in one file.

The program have some wildcard implementation but does not work properly.