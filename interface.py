import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import urllib.request
from urllib.request import Request, urlopen
import shutil
import requests
import re
import os
import sys
from scrollable import VerticalScrolledFrame
import numpy as np
from tkinter import *
from dotenv import load_dotenv

load_dotenv()

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
    
    error = "-"
    with os.scandir(mypath) as entries:
        for entry in entries:
            with os.scandir(os.path.join(mypath, entry)) as albums:
                for album in albums:
                    entry_path = os.path.join(mypath, entry)
                    album_path = os.path.join(entry_path, album)
                    if entry_path != mypath + '\\test' and os.path.isdir(os.path.join(mypath, entry.name + "\\" + album.name)):

                        # if os.path.isfile(os.path.join(mypath, entry.name + "\\" + album.name + "\\cover.jpg")) is False:

                           try:

                                query = "https://api.discogs.com/database/search?release_title=" + album.name + "&artist=" + entry.name + "&type=master&key={}&secret={}".format(str(os.environ["KEY"]), str(os.environ["SECRET"]))
                                
                                query = query.replace(' ', '%20')
                                print(query)
                                x = requests.get(query)
                                print(x)

                                url = x.json()['results'][0]['cover_image']
                                print(url)

                                # query = (entry.name + "+" + album.name).replace(" ", "+")
                                # add_text("Accessing https://musicbrainz.org/search?query=" + query + "&type=release_group&method=indexed")
                                # x = requests.get("https://musicbrainz.org/search?query=" + query + "&type=release_group&method=indexed")
                                # match = re.search('<a href="\/release-group\/\w{8}-\w{4}-\w{4}-\w{4}-\w{12}', x.text)[0]
                                # mbid = match[len(match)-36:]
                                # url = "https://coverartarchive.org/release-group/" + mbid + "/front-500"
                                # add_text("Accessing https://coverartarchive.org/release-group/" + mbid + "/front")

                                file_name = mypath + "\\" + entry.name + "\\" + album.name + "\\cover.jpg"


                                
                                req = Request(
                                    url=x.json()['results'][0]['cover_image'],
                                    headers={'User-Agent': 'Mozilla/5.0'}
                                )
                                
                                filename2 = mypath + '\\test\\' + album.name + ".jpg"

                                with urllib.request.urlopen(req) as response, open(file_name, 'wb') as out_file, open(filename2, 'wb+') as test123:
                                    shutil.copyfileobj(response, out_file)
                                    shutil.copyfile(file_name, filename2)
                                    
                                add_text("Added art for " + entry.name + " - " + album.name)
                                
                           except:
                                error += "\t" + entry.name + " - " + album.name + "\n"

                    elif os.path.samefile(entry_path, mypath + '\\test') == False:
                        add_text("Issue with directory structure for " + entry.name + "\\" + album.name)
        button2['state'] = 'active'
        add_text("Could not download:\n" + error)


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
