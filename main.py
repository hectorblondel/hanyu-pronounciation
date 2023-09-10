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
        "query": f"deck:{deck_name} audio:"
    }
}

response = anki_request(params)
notes_list = response['result']
print(f"{len(notes_list)} notes needs to be updated")



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
    raw_pinyin = infos[0]["fields"]["Pinyin"]["value"]
    print("computes the syllabus of {} (id = {})... ".format(raw_pinyin,note))
    syllabus = split_syllabus(remove_delimiters(raw_pinyin))
    audio_content = "" #The content of the audio field (it will send to the files from the storage path)
    for sound_code in syllabus :
        #We download the new sound if it doesn't exists yet
        file_name = sound_code+".mp3"
        if not file_name +".mp3" in os.listdir(storage_path):
            print("downloading {} ...".format(file_name))
            headers = {'User-Agent': 'pinyin-to-sound'}
            request = requests.get(url + file_name,headers=headers) #We download the file
            if request.status_code == 200 :
                with open(storage_path+file_name, 'wb') as f:
                    f.write(request.content)
            else :
                print("error {}".format(request.status_code))
                print(request.content)
        audio_content += "[sound:"+file_name+"]"
    
    #We update the note
    params = {
        "action": "updateNoteFields",
        "version": 6,
        "params": {
            "note": {
                "id": note,
                "fields": {
                    "Audio": audio_content
                }
            }
        }
    }
    response = anki_request(params)
    if response["error"] != None :
        print(response["error"])
    
