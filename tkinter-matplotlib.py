#!/usr/bin/python3

from tkinter import * 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import numpy as np
import matplotlib.pyplot as plt

cmax=40 # max current (mA)
cmin=-40 # min current (mA)
nc=64 # number of currents
xpos=np.arange(nc)
my_cmap = plt.cm.get_cmap('bwr')
bank=['A','B','C','D']
bars = [bank[int(x/16)]+str(x%16) for x in xpos]
print(bars)


# plot function is created for 
# plotting the graph in 
# tkinter window
def plot():
  
    # Make a random dataset:
    current=(np.random.random(nc)-.5)*80
    print(current)

    data_color = [(x-cmin)/(cmax-cmin) for x in current]
    colors = my_cmap(data_color)

    
    # plotting the graph
    ax.clear()
    ax.bar(xpos,current,color=colors)
    # Create names on the x-axis
    ax.set_xticks(xpos)
    ax.set_xticklabels(bars,rotation=90,ha='center',va='top')
    ax.set_ylim([cmin,cmax])
    ax.set_ylabel('current (mA)')
    canvas.draw()

# the main Tkinter window
window = Tk()
  
# setting the title 
window.title('Current control')
  
# dimensions of the main window
window.geometry("1000x250")

# button that displays the plot
plot_button = Button(master=window,
                     command=plot,
                     height=2,
                     width=10,
                     text="Plot")

# place the button in main window
plot_button.pack()

# the figure that will contain the plot
fig=Figure(dpi=100)
fig.set_tight_layout(True)

# adding the subplot
ax = fig.add_subplot(111)

# creating the Tkinter canvas containing the Matplotlib figure
canvas=FigureCanvasTkAgg(fig,master=window)  

# plot it once
plot()
  
# placing the canvas on the Tkinter window
canvas.get_tk_widget().pack(fill='x')
  
# run the gui
window.mainloop()
