from tkinter import*
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt

# ******************************************************************************************
# ******************************************************************************************
# ******************************************************************************************


def createSliders(master, parameters, plots):
    sliders = {}
    frames = {}

    sliders['ny'] = slider(master, label='ny', type_=IntVar,
                           value=parameters['ny'], plotObj=plots, orient='horizontal')
    sliders['ny'].row(0)

    sliders['nyUntilFreeze'] = slider(
        master, label='nyUntilFreeze', type_=IntVar, value=parameters['nyUntilFreeze'],
        plotObj=plots, orient='horizontal')
    sliders['nyUntilFreeze'].row(1)

    sliders['nyFarField'] = slider(master, label='nyFarField', type_=IntVar,
                                   value=parameters['nyFarField'], plotObj=plots, orient='horizontal')
    sliders['nyFarField'].row(2)

    sliders['dy0'] = slider(master, label='dy0', type_=DoubleVar,
                            value=parameters['dy0'], plotObj=plots, orient='horizontal')
    sliders['dy0'].row(3)

    sliders['dyFreeze'] = slider(master, label='dyFreeze', type_=DoubleVar,
                                 value=parameters['dyFreeze'], plotObj=plots, orient='horizontal')
    sliders['dyFreeze'].row(4)

    sliders['dyFarField'] = slider(master, label='dyFarField', type_=DoubleVar,
                                   value=parameters['dyFarField'], plotObj=plots, orient='horizontal')
    sliders['dyFarField'].row(5)

    sliders['truncateFarField'] = slider(master, label='truncateFarField', type_=DoubleVar,
                                         value=parameters['truncateFarField'], plotObj=plots, orient='horizontal')
    sliders['truncateFarField'].row(6)

    return sliders, frames

# ******************************************************************************************
# ******************************************************************************************
# ******************************************************************************************

# Export y and


def exportFile(y, parameters):

    # from scipy.io import FortranFile
    # f = FortranFile("y.i", "w")
    # f.write_record(np.array([1, 1, parameters['ny']], dtype=np.int32))
    # f.write_record(np.array(np.transpose(y), dtype=np.float64))
    # f.close()
    np.savetxt("y.csv", y, delimiter=",")
    with open('./zetastrParams.dat', 'w') as f:
        for key, entry in parameters.items():
            f.write('%s %s \n' % (key, entry))


# ******************************************************************************************
# ******************************************************************************************
# ******************************************************************************************

def smoothhat(yi, yc, ye, m1, m2, Nt, alpha):
    x1 = np.linspace(0.0, 1.0, m1)
    y1 = (6.0*x1**5 - 15.0*x1**4 + 10*x1**3)

    dy = yc-yi
    y1 = y1*dy + yi

    x2 = np.linspace(0.0, alpha, m2)
    y2 = (6.0*x2**5 - 15.0*x2**4 + 10*x2**3)   # TODO

    dy = ye-yc
    y2 = y2/alpha*(dy-yc) + yc

    cte = np.zeros(Nt-m1-m2)
    cte = cte + yc

    y = np.concatenate((y1, cte, y2))

    return y
# ******************************************************************************************
# ******************************************************************************************
# ******************************************************************************************


def loadParameters():

    parameters = {}
    try:
        with open('./zetastrParams.dat', 'r') as f:
            lines = f.readlines()
        for line in lines:
            key, entry = line.split()
            parameters[key] = int(entry) if entry.isdigit() else float(entry)

    except:
        print('File with initial parameters not found.')

    return parameters

# ******************************************************************************************
# ******************************************************************************************
# ******************************************************************************************


class slider:
    def __init__(self, frame, label, type_, value, plotObj, orient='horizontal'):
        self.useScientificNotation = True if type_ == DoubleVar else False
        self.value = type_()
        self.value.set(value)

        # Create frames for storing slider, label and entry
        self.leftFrame = Frame(frame)
        self.rightFrame = Frame(frame)

        # Create entry
        self.entry = Entry(self.rightFrame)
        self.entry.insert(15, self.value.get())
        self.button = Button(
            self.rightFrame, command=self.updateSlider, text='Center bars')

        # Keep a copy of plotObj
        self.plotObj = plotObj

        # Create label that stays on top of slider
        self.labelString = StringVar()
        self.labelString.set(label)
        self.label = Label(self.leftFrame, anchor='n',
                           textvariable=self.labelString)

        # Create slider
        self.slider = Scale(self.leftFrame, orient=orient,
                            variable=self.value, command=self.updateEntry, showvalue=False)
        self.updateEntry(value)
        self.updateSlider()

    def updateEntry(self, value):
        self.entry.delete(0, 15)
        if self.useScientificNotation:
            self.entry.insert(15, '%.2e' % (float(value)))
            self.plotObj[0].updateXY(**{self.labelString.get(): float(value)})

        else:
            self.entry.insert(15, '%d' % int(float(value)))
            self.plotObj[0].updateXY(
                **{self.labelString.get(): int(float(value))})

    def updateSlider(self):
        number = float(self.entry.get())
        if number <= 1e-15:
            number = 1e-12

        magnitude = 10**int(np.floor(np.log10(number)))
        self.slider.configure(resolution=(2*magnitude)/200.)
        self.slider.configure(to=number+magnitude)
        self.slider.configure(from_=number-magnitude)

        self.slider.set(self.entry.get())
        self.updateEntry(self.entry.get())

    # Organize elements in a grid
    def row(self, row):
        self.leftFrame.grid(row=row, column=0)
        self.rightFrame.grid(row=row, column=1)

        self.label.grid(row=0, column=0)
        self.slider.grid(row=1, column=0)
        self.entry.grid(row=1, column=0)
        self.button.grid(row=1, column=1)

# ******************************************************************************************
# ******************************************************************************************
# ******************************************************************************************


class plots:
    def __init__(self, master, parameters):

        self.parameters = {}
        self.parameters = parameters

        self.nPlots = 4
        self.fig, self.ax = plt.subplots(self.nPlots, 1, sharex=False)

        # Populate axes
        plt.subplots_adjust(hspace=0.5)
        for i in range(self.nPlots):
            self.ax[i].plot(0, 0, 'o-')

        # A DrawingArea.
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, master)
        toolbar.draw()
        toolbar.pack(side=LEFT)
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        # self.canvas.show()

        self.resetButton = Button(
            master, command=self.resetAxes, text='Reset View')
        self.resetButton.pack(side='bottom')

    # Replot everything so axes are resetted
    def resetAxes(self):
        for i in range(self.nPlots):
            y = self.ax[i].lines[0].get_ydata()
            x = self.ax[i].lines[0].get_xdata()
            self.ax[i].clear()
            self.ax[i].plot(x, y, '-o', markersize=2)

        self.beautify()

        self.canvas.draw()

    # Update XY data
    def updateXY(self, **kwargs):

        if kwargs is not None:
            for key, value in kwargs.items():
                self.parameters[key] = value

        ny = self.parameters['ny']
        dy0 = self.parameters['dy0']
        dyFreeze = self.parameters['dyFreeze']
        dyFarField = self.parameters['dyFarField']
        nyUntilFreeze = self.parameters['nyUntilFreeze']
        nyFarField = self.parameters['nyFarField']
        truncateFarField = self.parameters['truncateFarField']

        dy = smoothhat(dy0, dyFreeze, dyFarField, nyUntilFreeze,
                       nyFarField, ny-1, truncateFarField)

        y = np.zeros(ny)
        for i, _ in enumerate(dy):
            y[i+1] = np.sum(dy[:i+1])

        stretchRatio = (dy[1:]) / (dy[0:-1])

        self.ax[0].lines[0].set_ydata(y)
        self.ax[0].lines[0].set_xdata(np.arange(np.size(y)))

        self.ax[1].lines[0].set_ydata(stretchRatio)
        self.ax[1].lines[0].set_xdata(np.arange(np.size(stretchRatio)))

        self.ax[2].lines[0].set_ydata(stretchRatio)
        self.ax[2].lines[0].set_xdata(y[1:-1])

        self.ax[3].lines[0].set_ydata(dy)
        self.ax[3].lines[0].set_xdata(np.arange(np.size(dy)))

        self.beautify()
        self.y = y

    # Add labels and grid
    def beautify(self):
        self.ax[0].set(ylabel='y')
        self.ax[0].set(xlabel='i')

        self.ax[1].set_ylabel('Stretch ratio')
        self.ax[1].set_xlabel('i')

        self.ax[2].set_ylabel('Stretch Ratio')
        self.ax[2].set_xlabel('y')

        self.ax[3].set_ylabel('dy')
        self.ax[3].set_xlabel('i')

        for i in range(self.nPlots):
            self.ax[i].grid(True)

        self.canvas.draw()

# ******************************************************************************************
# ******************************************************************************************
# ******************************************************************************************


if __name__ == '__main__':

    parameters = {}

    # Number of points in airfoil outward direction
    parameters['ny'] = 300
    parameters['dy0'] = 0.00004      # Minimum normal distance
    # Number of points before turning on y freezing
    parameters['nyUntilFreeze'] = 161
    parameters['dyFreeze'] = 0.003   # Size of y step when slope of y freezes
    parameters['dyFarField'] = 0.2   # Stretch in the far-field
    parameters['nyFarField'] = 50
    parameters['truncateFarField'] = 1.
    # parameters = loadParameters()

    def onClose(plotWindow, sliders):
        root.destroy()
    root = Tk()
    root.protocol("WM_DELETE_WINDOW")
    root.geometry("1000x1000+800+0")
    inputsFrame = Frame(root)
    inputsFrame.pack(side='left')
    plotFrame = Frame(root)
    plotFrame.pack(side='right', fill='both', expand=True)
    plotWindow = [plots(plotFrame, parameters)]
    sliders, frames = createSliders(inputsFrame, parameters, plotWindow)
    plotWindow[0].resetAxes()
    exportButton = Button(inputsFrame, text='Export', command=lambda: exportFile(
        plotWindow[0].y, plotWindow[0].parameters))
    exportButton.grid(columnspan=2,  sticky=N+S+E+W)
    quitButton = Button(inputsFrame, text='Quit',
                        command=lambda: onClose(plotWindow, sliders))
    quitButton.grid(columnspan=2,  sticky=N+S+E+W)
    plotFrame.mainloop()
