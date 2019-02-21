#!/usr/bin/python3

# create à readable list for python3
#to be used by "show_guitar_accord.py"
import os

os.system("sed -e 's/\"p\":\"/\"p\":[/g' -e 's/\",\"f\"/],\"f\"/g' -e 's/x/\"x\"/g' -e 's/w/\"w\"/g' accord.json >> temp.py")
os.system("sed -i '1s/^/CHORDS=/' temp.py")

from temp import CHORDS

if 1:
    new_chords={}
    for a in list(CHORDS):
        new_chords[a]={}


    for a in list(CHORDS):
        for b in list(CHORDS[a]):
            new_chords[a][b]=[]

    for a in list(CHORDS):
        for b in list(CHORDS[a]):
            for c in range(len(list(CHORDS[a][b]))):
                print(CHORDS[a][b][c]['p'])
                print(new_chords[str(a)][str(b)])
                new_chords[a][b].append(CHORDS[a][b][c]['p'])
    with open("listedesaccord_fichier2.py", 'w') as f:
        f.write("CHORDS="+str(new_chords))

os.system("sed 's/],/&\\n/g' listedesaccord_fichier2.py > listedesaccords.py")
os.system("rm listedesaccord_fichier2.py")
