from tkinter import *
from tkinter.filedialog import askopenfilename
from datetime import *


stations = dict()

def xmltofilelist():
    print("blah")

def repair():
    print("repair")

def runit():
    print(runit)

class Static:
    def __init__(self, interval, date, location, description, status, days):
        self.interval = interval
        self.date = date
        self.location = location
        self.descrption = description
        self.status = status
        self.days = days



class Statics:
    def __init__(self, master):
        self.master = master
        root.geometry("700x300")
        master.title("Static Bench Locator")

        master.bind("<Return>", lambda x: self.add())
        
        self.label = Label(master, text="Choose Map File (.htm)")
        self.label.place(x=145,y=0)
        
        self.label2 = Label(master, text="File:")
        self.label2.place(x=210,y=30)

        
        frame = Frame(master)
        scrollbar = Scrollbar(master, orient=VERTICAL)
        
        self.select_button = Button(master, text="Select File", command=self.select)
        self.select_button.place(x=145, y=20, in_=root)
        
        self.e = Entry(master, width=20)
        self.e.place(x=145, y=50, in_=root)

        self.listy = Listbox(master, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listy.yview)
        self.listy.pack(side=LEFT, fill=Y)
        scrollbar.pack(side=LEFT, fill=Y)
        #scrollbar.place(x=140,y=150)
        #self.listy.place(x=10, y=80)

        self.add_button = Button(master, text="Add Asset", command=self.add)
        self.add_button.place(x=280, y=45, in_=root)

        self.remove_button = Button(master, text="Remove Asset", command=self.remove)
        self.remove_button.place(x=145, y=75, in_=root)

        self.clear_button = Button(master, text="Clear List", command=self.clear)
        self.clear_button.place(x=145, y=105, in_=root)

        self.clear_button = Button(master, text="Auto Add", command=self.autoadd)
        self.clear_button.place(x=145, y=135, in_=root)

        self.clear_button = Button(master, text="Auto Add Awaiting Label", command=self.autoaddlabel)
        self.clear_button.place(x=145, y=165, in_=root)

        self.clear_button = Button(master, text="Auto Add Completed", command=self.autoaddcomplete)
        self.clear_button.place(x=145, y=195, in_=root)

        self.generate_button = Button(master, text="Generate Map", command=self.generate)
        self.generate_button.place(x=145, y=225, in_=root)
        

    def add(self):
        s = self.e.get()
        self.listy.insert(END, s)
        print("Add Item: " + s)
        self.e.delete(0,END)

    def remove(self):
        s = self.listy.get(ACTIVE)
        self.listy.delete(ANCHOR)
        print("Removed: " + s)

    def clear(self):
        self.listy.delete(0,END)
        print("Clear List.")
        stations.clear()

    def autoadd(self):
        self.listy.delete(0,END)
        stations.clear()
        print("Auto adding assets requiring service.")
        with open ('stationdata.csv', 'r+') as f:
            for line in f:
                if 'RECEIVED' in line:
                    z = line.split(',')
                    self.listy.insert(END, z[3])
                    today = datetime.today()
                    due = datetime.strptime(z[1], "%m/%d/%Y")
                    delta = due - today
                    daysuntildue  = delta.days
                    print("Add Item: " + z[3] + " due " + z[1] + " in " + z[2] + ". Due in " + str(daysuntildue) + " days.")
                    p = z[3]
                    stations[p] = (Static(z[0],z[1],z[2],z[4],z[5],daysuntildue))
                    print(stations[p].date)
                else:
                    pass

    def autoaddlabel(self):
        self.listy.delete(0,END)
        stations.clear()
        print("Auto adding assets requiring labeling.")
        with open ('stationdata.csv', 'r+') as f:
            for line in f:
                if 'AWATING COMPLETION' in line:
                    z = line.split(',')
                    self.listy.insert(END, z[3])
                    today = datetime.today()
                    due = datetime.strptime(z[1], "%m/%d/%Y")
                    delta = due - today
                    daysuntildue  = delta.days
                    print("Add Item: " + z[3] + " due " + z[1] + " in " + z[2] + ". Due in " + str(daysuntildue) + " days.")
                    p = z[3]
                    stations[p] = (Static(z[0],z[1],z[2],z[4],z[5],daysuntildue))
                    print(stations[p].date)
                else:
                    pass

    def autoaddcomplete(self):
        self.listy.delete(0,END)
        stations.clear()
        print("Auto adding assets requiring labeling.")
        with open ('stationdata.csv', 'r+') as f:
            for line in f:
                if 'COMPLETE' in line:
                    z = line.split(',')
                    self.listy.insert(END, z[3])
                    today = datetime.today()
                    due = datetime.strptime(z[1], "%m/%d/%Y")
                    delta = due - today
                    daysuntildue  = delta.days
                    print("Add Item: " + z[3] + " due " + z[1] + " in " + z[2] + ". Due in " + str(daysuntildue) + " days.")
                    p = z[3]
                    stations[p] = (Static(z[0],z[1],z[2],z[4],z[5],daysuntildue))
                    print(stations[p].date)
                else:
                    pass


        
    def generate(self):
        print("generate map")

    def map(self):
        print("mapfilechosen")

    def select(self):
        print("Select File.")
        name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                title = "Choose a file."
                )
        print (name)


        

root = Tk()
my_gui = Statics(root)
root.mainloop()





