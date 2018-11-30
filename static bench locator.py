from tkinter import *
from tkinter.filedialog import askopenfilename
from datetime import *
import os
import webbrowser

mainpath = ("/")
filename = ("")
finfile = ("")
fullpath = ("")
simpname = ("")
sheetlist = []
stations = dict()
itemlist = []
sheetfound = []

def xmltofilelist(basepath,file):
    print("base path " + basepath)
    print("file " + file)
    xmlfile = str(basepath + "/" + file + "_files/filelist.xml")
    print(xmlfile)
    x = []
    with open (xmlfile, "r+") as f:
        for line in f:
            if 'sheet' in line and '.htm' in line:
                x.append(line[15:27])
        for items in x:
            print("Found:" + items)
            if  len(x) == 0:
                print("No map files found")
    return(x)
        

def repair():
    global mainpath
    global filename
    global simpname
    global sheetlist
    global finfile
    global sheetfound
    tabpathfull = (mainpath + "/" + simpname + "_files/tabstrip.htm")
    tabpathnew = (mainpath + "/" + simpname + "_files/tabstripdump.htm")
    fullfile = (mainpath + "/" + filename)
    print(fullfile)
    finfile = fullfile.replace(simpname, simpname + "dump")
    print(finfile)
    #tabstrip repair
    print("Repairing Tabstrip: ")
    with open (tabpathfull, "r+") as f, open(tabpathnew,"w+") as p:
        for line in f:
            if simpname in line:
                print("before: " + line)
                line = line.replace(simpname + ".htm", simpname + "dump.htm")
                p.write(line)
            elif any(x in line for x in sheetfound):
                line = line.replace(".htm", "dump.htm")
                line = line.replace("#FFFFFF","#00f1be")
                p.write(line)
            elif any(x in line for x in sheetlist):
                line = line.replace(".htm", "dump.htm")
                p.write(line)
            else:
                p.write(line)
        p.close()
        
    with open (fullfile, "r+") as w, open(finfile,"w+") as r:
        for line in w:
            if filename in line:
                print("before: " + line)
                filenamenew = filename.replace(".htm","dump.htm")
                line = line.replace(filename, filenamenew)
                r.write(line)
                print("after: " + line)
            elif "tabstrip.htm" in line:
                line = line.replace("tabstrip.htm","tabstripdump.htm")
                r.write(line)
            elif any(x in line for x in sheetlist):
                for x in sheetlist:
                    if x in line:
                      line = line.replace(".htm", "dump.htm")
                      r.write(line)
            else:
                  r.write(line)

        r.close()
            


def highlight():
    global mainpath
    global filename
    global fullpath
    global simpname
    global stations
    global itemlist
    global sheetfound
    global sheetlist
    sheetfound = []
    print(itemlist)
    for items in sheetlist:
        sheetpathfull = (mainpath + "/" + simpname + "_files/" + items)
        oldsheet = items
        items = items.replace(".htm","dump.htm")
        sheetpathnew = (mainpath + "/" + simpname + "_files/" + items)
        print("Searching " +sheetpathfull+ " for stations, writing stations to " + sheetpathnew + ".")
        with open(sheetpathfull, "r+") as f, open(sheetpathnew, "w+") as p:
            for line in f:
                if any(x in line for x in itemlist):
                    for s in itemlist:
                        if s in line:
                            item = s
                    if oldsheet not in sheetfound:
                        sheetfound.append(oldsheet)
                    print("original line: " + line)
                    newitem = ("""<span style="background:#008822">""" + item + """</span>""")
                    line = line.replace(item + "<" , newitem + "<")
                    p.write(line)
                    print("replaced: " + line)
                else:
                    p.write(line)
            p.close()
            print("Items found on the following sheets: " + str(sheetfound))



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
        if self.listy.size() == 0:
            print("No items in list to locate. Please add items")
        else:
            global itemlist
            itemlist =  self.listy.get(0,END)
            print("generate map")
            highlight()
            repair()
            print(finfile)
            webbrowser.open_new(finfile)


    def select(self):
        global filename
        global finfile
        global mainpath
        global fullpath
        global simpname
        global sheetlist
        print("Select File.")
        name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                filetypes =(("Web Page", "*.htm"),("All Files","*.*")),
                title = "Choose map file."
                )
        filename = os.path.basename(name)
        mainpath = os.path.dirname(name)
        s = filename.split('.')
        simpname = s[0]
        sheetlist = xmltofilelist(mainpath,simpname)
        
        


        

root = Tk()
my_gui = Statics(root)
root.mainloop()





