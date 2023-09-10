"""Clears all the sounds in the anki deck specified in the info.json file"""

import json
import requests
from utils import *
import tqdm
import os

#We get the name of the deck
with open("info.json","r") as info_file:
    info = json.load(info_file)
    deck_name = info["deck"]
    storage_path = info["storage_path"]
    if storage_path == "" :
        raise NameError('no storage path in info.json')
    url = info["url"]
    if url == "" :
        raise NameError('no url in info.json')

#We get all the cards from the deck thanks to the ankiconnect api
params = {
    "action": "findNotes",
    "version": 6,
    "params": {
        "query": f"deck:{deck_name}"
    }
}

response = anki_request(params)
notes_list = response['result']
print(notes_list)



#print(notes_list[0])
for note in notes_list :
    
    params = {
    "action" : "notesInfo",
    "version" : 6,
    "params" : {
        "notes" : [note]
        }
    }
    
    response = anki_request(params)
    infos = response["result"]
    sound = infos[0]["fields"]["Audio"]["value"]
    if sound != "" :
        #We delete the sound from the note
        params = {
        "action": "updateNoteFields",
        "version": 6,
        "params": {
            "note": {
                "id": note,
                "fields": {
                    "Audio": ""
                }
            }
        }
    }
    print("clearing sound from note {} ... ".format(note))
    response = anki_request(params)
    if response["error"] != None :
        print(response["error"])
    
