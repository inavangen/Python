# coding=utf-8
#!/usr/bin/python
import matplotlib
import matplotlib.gridspec as gridspec 
import matplotlib.pyplot as plt

def plot_data(data_list_init, data_list, img):
		""" Takes two lists of similar dimentions and plots them. If img
		is true, a image is saved as plot.jpg """
		g = gridspec.GridSpec(1, 3, width_ratios=[10, 10, 2, 2, 1]) 
		
		first = plt.subplot(g[0]) 
		first.set_title("Plot 1") 
		first.imshow(data_list_init, cmap="gray", aspect="auto") 
		
		second = plt.subplot(g[1]) 
		second.set_title("Plot 2") 
		color = second.imshow(data_list, cmap="gray", aspect="auto")

		color_plot = plt.subplot(g[2]) 
		
		plt.colorbar(color, cax=color_plot)
		if img:
			plt.savefig("plot.jpg")
			print "Plot saved as plot.jpg"
		plt.show()