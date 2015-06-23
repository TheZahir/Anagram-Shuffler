from tkinter import *
from tkinter.ttk import *


class ButtonApp(Frame):
    """Container for the buttons."""

    def __init__(self, master=None):
        """Initialize the frame and its children."""

        super().__init__(master)
        self.createWidgets()

        # configure the frame's resize behaviour
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        self.grid(sticky=(N,S,E,W))

        # configure resize behaviour for the frame's children
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # bind to window resize events
        self.bind('<Configure>', self.resize)


    def createWidgets(self):
        """Make the widgets."""

        # this button mutates
        self.mutantButton = Button(self, text='Press Me',
                                   style='10.TButton')
        self.mutantButton.grid(column=0, row=0, sticky=(N,S,E,W))
        self.mutantButton['command'] = self.mutate

        # an ordinary quit button for comparison
        self.quitButton = Button(self, text='Quit', style='TButton')
        self.quitButton.grid(column=0, row=1, sticky=(N,S,E,W))
        self.quitButton['command'] = self.quit


    def mutate(self):
        """Rotate through the styles by hitting the button."""

        style = int(self.mutantButton['style'].split('.')[0])
        newStyle = style + 5
        if newStyle > 50: newStyle = 10
        print('Choosing font '+str(newStyle))
        self.mutantButton['style'] = fontStyle[newStyle]

        # resize the frame

        # get the current geometries
        currentGeometry = self._root().geometry()
        w, h, x, y = self.parseGeometry(currentGeometry)
        reqWidth = self.mutantButton.winfo_reqwidth()
        reqHeight = self.mutantButton.winfo_reqheight()

        # note assume height of quit button is constant at 20.
        w = max([w, reqWidth])
        h = 20 + reqHeight
        self._root().geometry('%dx%d+%d+%d' % (w, h, x, y))


    def parseGeometry(self, geometry):
        """Geometry parser.
        Returns the geometry as a (w, h, x, y) tuple."""

        # get w
        xsplit = geometry.split('x')
        w = int(xsplit[0])
        rest = xsplit[1]

        # get h, x, y
        plussplit = rest.split('+')
        h = int(plussplit[0])
        x = int(plussplit[1])
        y = int(plussplit[2])

        return w, h, x, y


    def resize(self, event):
        """Method bound to the <Configure> event for resizing."""

        # get geometry info from the root window.
        wm, hm = self._root().winfo_width(), self._root().winfo_height()

        # choose a font height to match
        # note subtract 30 for the button we are NOT scaling.
        # note we assume optimal font height is 1/2 widget height.
        fontHeight = (hm - 20) // 2
        print('Resizing to font '+str(fontHeight))

        # calculate the best font to use (use int rounding)
        bestStyle = fontStyle[10] # use min size as the fallback
        if fontHeight < 10: pass # the min size
        elif fontHeight >= 50: # the max size
            bestStyle = fontStyle[50]
        else: # everything in between
            bestFitFont = (fontHeight // 5) * 5
            bestStyle = fontStyle[bestFitFont]

        # set the style on the button
        self.mutantButton['style'] = bestStyle


root = Tk()
root.title('Alice in Pythonland')

# make a dictionary of sized font styles in the range of interest.
fontStyle = {}
for font in range(10, 51, 5):
    styleName = str(font)+'.TButton'
    fontName = ' '.join(['helvetica', str(font), 'bold'])
    fontStyle[font] = styleName
    Style().configure(styleName, font=fontName)

# run the app
app = ButtonApp(master=root)
app.mainloop()
root.destroy()

"""
http://stackoverflow.com/questions/12018540/python3-how-to-dynamically-resize-button-text-in-tkinter-ttk
"""