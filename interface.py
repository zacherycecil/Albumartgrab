import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import urllib.request
import shutil
import requests
import re
import os
import sys
from scrollable import VerticalScrolledFrame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *

def add_text(str):
    var.set(str + "\n" + var.get())
    print(str)
    root.update_idletasks()


def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    mypath = filedialog.askdirectory()
    folder_path.set(mypath)
    button2['state'] = "disabled"
    
    error = ""
    with os.scandir(mypath) as entries:
        for entry in entries:
            with os.scandir(os.path.join(mypath, entry)) as albums:
                for album in albums:
                    entry_path = os.path.join(mypath, entry)
                    album_path = os.path.join(entry_path, album)
                    if os.path.isdir(os.path.join(mypath, entry.name + "\\" + album.name)):

                        if os.path.isfile(os.path.join(mypath, entry.name + "\\" + album.name + "\\cover.jpg")) is False:

                            try:
                                
                                query = (entry.name + "+" + album.name).replace(" ", "+")

                                add_text("Accessing https://musicbrainz.org/search?query=" + query + "&type=release_group&method=indexed")

                                x= requests.get("https://musicbrainz.org/search?query=" + query + "&type=release_group&method=indexed")
                                match = re.search('<a href="\/release-group\/\w{8}-\w{4}-\w{4}-\w{4}-\w{12}', x.text)[0]
                                mbid = match[len(match)-36:]

                                url = "https://coverartarchive.org/release-group/" + mbid + "/front-500"
                                file_name = mypath + "\\" + entry.name + "\\" + album.name + "\\cover.jpg"

                                add_text("Accessing https://coverartarchive.org/release-group/" + mbid + "/front")

                                with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
                                    shutil.copyfileobj(response, out_file)
                                    
                                add_text("Added art for " + entry.name + " - " + album.name)
                                
                            except:
                                error += entry.name + " - " + album.name + "\n"

                        else:
                            add_text("Skipping " + entry.name + " - " + album.name + ", cover exists.")
                    else:
                        add_text("Issue with directory structure.")
        button2['state'] = 'active'
        add_text(error)


root = Tk()
root.geometry("600x300")
root.title("Album Art Grab")

folder_path = StringVar()
label1 = tk.Label(text="""Folder structure should be /Music/Artist/Album/song.mp3
        In this example, please select 'Music' folder
        Album art is found online based on the names of your Artist/Album folder names, so name them well!
        Enter the path to your music library: """)
button2 = Button(text="Browse", command=browse_button)

label1.pack()
button2.pack()


frame = VerticalScrolledFrame(root)
frame.pack(fill=BOTH, pady=(20))


var = StringVar()

l = Label(frame.interior, textvariable = var)
l.pack(side=TOP, fill=BOTH, expand=1)

root.mainloop()
