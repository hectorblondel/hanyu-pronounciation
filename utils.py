from unidecode import unidecode
import json
import requests

#The dictionnary where tones[letter] gives the tone (1,2,3,4)
tones = {
    "ā": "1",
    "á": "2",
    "ǎ": "3",
    "à": "4",
    "ē": "1",
    "é": "2",
    "ě": "3",
    "è": "4",
    "ō": "1",
    "ó": "2",
    "ǒ": "3",
    "ò": "4",
    "ī": "1",
    "í": "2",
    "ǐ": "3",
    "ì": "4",
    "ū": "1",
    "ú": "2",
    "ǔ": "3",
    "ù": "4",
    "ǖ": "1",
    "ǘ": "2",
    "ǚ": "3",
    "ǜ": "4"
}


def number_pinyin(word):
    """changes each voyel f the word into : the voyel without an accent + a number corresponding ot the tone"""
    tone = ""
    res = ""
    for letter in word:
        if letter in tones.keys():
            res += unidecode(letter)
            tone = tones[letter] #the tone that will be added at the end of the letters
        else:
            res += letter
    
    return res+tone

def remove_delimiters(chn):
    """removes the tex between brackets < and />"""
    res = ""
    i = 0
    while i < len(chn):
        if chn[i] == "<":
            while chn[i] != ">":
                i += 1
        else:
            res += chn[i]
        i += 1
    return res

def split_syllabus(input_word,without_accents=True):
    #Split a pinyin word into a list of syllables
    #Accurate only if "èr" isn't present in the word.
    consonnes = ["b","p","m","f","d","t","n","l","z","c","s","zh","ch","sh","r","j","q","x","g","k","h","y"]
    voyelles = ["a","ai","ao","an","ang","e","ei","en","eng","er","o","ou","ong","i","ia","iao","ian","iang","ie","in","ing","iong","iu","u","ua","uo","uai","ui","uan","uang","un","ueng","ue"]
    #ue is only for üe

    #We remove all the spaces from input_word
    word = input_word.replace(" ","")

    all_syllables = []
    for c in consonnes :
        for v in voyelles :
            all_syllables.append(c+v)
    
    #We sort the syllabus in decreasing length order to avoid match "de" before "deng"
    all_syllables.sort(key=len, reverse=True)

    syllabes = []
    i = 0
    while i < len(word):
        for syllabe in all_syllables:

            if word[i:i+2] == "èr":
                syllabes.append("èr")
                i += 2
                break
            

            if unidecode(word[i:i+len(syllabe)]) == syllabe and not word[i+len(syllabe)-1:i+len(syllabe)+1] == "èr":
                syllabes.append(word[i:i+len(syllabe)])
                i += len(syllabe)
                break

        
        else:
            # Si aucune correspondance n'est trouvée dans le dictionnaire, nous prenons un caractère seul
            # (Ce cas ne devrait pas se produire)
            print("No match found for", word[i])
            syllabes.append(word[i])
            i += 1
            break

    if without_accents :
        for i in range(len(syllabes)):
            syllabes[i] = number_pinyin(syllabes[i])
        return syllabes
    else :
        return syllabes
    

def anki_request(params):
    params_formated = json.dumps(params).encode('utf-8')
    #print(params)
    response = requests.post('http://localhost:8765',params_formated)
    if response.status_code == 200 :
        return json.loads(response.content)
    else :
        print("error {}".format(response.status_code))
        return None





if __name__ == '__main__':
    print(split_syllabus("zhōngguó"))
    print(split_syllabus("nüèr"))