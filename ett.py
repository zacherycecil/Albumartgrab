import urllib.request
import shutil
import requests
import re
import os
import sys

mypath = "C:\\Users\\zcjl9\\OneDrive\\Documents\\iPod"

error = "issues with:\n"

with os.scandir(mypath) as entries:
    for entry in entries:
        with os.scandir(os.path.join(mypath, entry)) as albums:
            for album in albums:
                entry_path = os.path.join(mypath, entry)
                album_path = os.path.join(entry_path, album)
                print("")
                if os.path.isdir(entry_path):

                    if os.path.isfile(os.path.join(mypath, entry.name + "\\" + album.name + "\\cover.jpg")) is False:
                    

                        
                        print(os.path.join(mypath, album))
                        print(entry.name + " site:musicbrainz.org")

                        try:
                            
                            query = (entry.name + "+" + album.name).replace(" ", "+")

                            print("https://musicbrainz.org/search?query=" + query + "&type=release_group&method=indexed")

                            x= requests.get("https://musicbrainz.org/search?query=" + query + "&type=release_group&method=indexed")
                            print(x.text)
                            match = re.search('<a href="\/release-group\/\w{8}-\w{4}-\w{4}-\w{4}-\w{12}', x.text)[0]
                            print(match[len(match)-36:])
                            mbid = match[len(match)-36:]

                            print("A:\\Music\\\"" + entry.name + "\"\\\"" + album.name + "\"\\cover.jpg")

                            url = "https://coverartarchive.org/release-group/" + mbid + "/front-500"
                            file_name = mypath + "\\" + entry.name + "\\" + album.name + "\\cover.jpg"

                            print("https://coverartarchive.org/release-group/" + mbid + "/front")

                            with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
                                shutil.copyfileobj(response, out_file)

                        except:
                            error += entry.name + "\n"

                    else:
                        print("Skipping " + entry.name + " " + album.name)
  

print(error)
