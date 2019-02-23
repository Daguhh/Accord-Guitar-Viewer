#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Display guitar chords from listedesaccords database
"""
import tkinter as tk
import tkinter.ttk as ttk

from guitare_parameter import cordes_espacement, \
                              cordes_offset, \
                              frets_nombre, \
                              frets_espacement, \
                              guitare_width, \
                              guitare_height # param géométiques
from listedesaccords import CHORDS # dictionnaire des accords
try:
    from woodenbackground import get_background # créé image de fond (optionel)
except : pass

################# Interface Principale ##############################
class MainGui:

    def __init__(self, root, pos=[0,0]):

        mainframe = tk.Frame(root, relief="sunken", borderwidth=3)

        # Création d'une grille représentant une guitare
        frame1=tk.Frame(mainframe)
        self.guitare = Guitare(frame1)
        frame1.pack(side=tk.TOP)

        # Création de listes déroulantes pour selection de l'accord
        frame2=tk.Frame(mainframe)
        self.accordage = self.combobox(frame = frame2,
                                       liste = list(CHORDS),
                                       callback = self.change_accords_liste)

        self.accord = self.combobox(frame = frame2,
                                    liste = None,
                                    callback = self.change_variantes_liste)

        self.variante = self.combobox(frame = frame2,
                                      liste = None,
                                      callback = self.dessine_tablature)
        frame2.pack(side=tk.LEFT)

        mainframe.grid(row=pos[0], column=pos[1])

    # Création des listes déroulantes (excecuté à l'init uniquement)
    def combobox(self, frame, liste, callback):
        return DropList(frame=frame, values=liste, callback=callback)

    # Modification du contenus des listes
    def change_accords_liste(self, event):
        # éléments selectionnés des combobox précédentes
        accordage = self.accordage.box.get()
        # application des nouvelles valeurs
        accords = list( CHORDS[accordage] )
        self.accord.box['values'] = accords

    def change_variantes_liste(self, event):
        # éléments selectionnés des combobox précédentes
        accordage = self.accordage.box.get()
        accord = self.accord.box.get()
        # application des nouvelles valeurs
        variantes = list( CHORDS[accordage][accord] )
        self.variante.box['values'] = variantes

    # affichage de la tablature
    def dessine_tablature(self, event):
        # éléments selectionnés des combobox précédentes
        accordage = self.accordage.box.get()
        accord = self.accord.box.get()
        variante = self.variante.box.current()
        # obtention de l'accord et affichage sur le manche
        accord_choisi = CHORDS[accordage][accord][variante]
        self.guitare.show_accord(accord_choisi)

################# Widgets & Canvas #####################################
class DropList:
# Créé une liste déroulante afin de selectionner les accords à afficher
# affiche la liste "values" et excecute "callback" à la selection
    def __init__(self, frame, values=None, callback=None):

        self.value = tk.StringVar()
        self.box = ttk.Combobox(frame,
                                textvariable=self.value,
                                width = 11)
        self.box.bind('<<ComboboxSelected>>', callback)
        self.box['values'] = values
        self.box.pack(side=tk.TOP)


class Guitare:
# Créé une grille représentant un manche de guitare et affiche l'accord
# selectionné
    def __init__(self, frame):
    # Création de l'espace de dessin et initialisation de la géometrie
        self.frame = frame
        # Espace de dessin
        self.canvas1 = tk.Canvas(self.frame,
                                 width = guitare_width,
                                 height = guitare_height)

        # Paramètres du manche de guitare
        self.cordes_nombre = len(list(CHORDS)[0])
        self.cordes_taille = (frets_nombre) * frets_espacement
        self.frets_taille = (self.cordes_nombre - 1) * cordes_espacement \
                            + 2 * cordes_offset

        # Listera les objets pour manipulation/suppression
        self.accord_choisi = None
        self.accord_precedent = [0]*self.cordes_nombre
        self.numero_frette = []

        # Création du manche de guitare
        self.guitare = self.create_guitare()
        self.canvas1.pack(side=tk.TOP)

    def create_guitare_background(self):
    # génère de façon procédurale une image de manche en bois
        try:
            self.canvas1.background = get_background((self.frets_taille*2,
                                                      self.cordes_taille*2))
            self.background =\
                self.canvas1.create_image(0, 0, image=self.canvas1.background)
        except:
            print("Impossible de créer l'image, voir fonction get_backgound")

    def create_guitare(self):
    # création de la grille (frettes + cordes)
        # Création du fond
        self.canvas1.delete("all")
        self.create_guitare_background()

        # Création des frettes
        for n_fret in range(frets_nombre) :
            self.canvas1.create_line(0,
                                     frets_espacement * n_fret,
                                     self.frets_taille,
                                     frets_espacement * n_fret,
                                     fill="black",
                                     width=1.5)
        # Première frette (plus large)
        self.canvas1.create_line(0,
                                 frets_espacement * 1,
                                 self.frets_taille,
                                 frets_espacement * 1,
                                 fill = "black",
                                 width = 5)

        # Création des cordes
        for n_corde in range(self.cordes_nombre):
            self.canvas1.create_line(n_corde * cordes_espacement + cordes_offset,
                                     0,
                                     n_corde * cordes_espacement + cordes_offset,
                                     self.cordes_taille,
                                     width=(7-n_corde)/3,
                                     fill="darkgray")

    def show_accord(self, accord_choisi):
    # dessine l'accord choisi par les combobox

        # on redessine le manche si le nombre de cordes à changé
        if len(accord_choisi) != len(self.accord_precedent) :
            self.cordes_nombre = len(accord_choisi)
            self.frets_taille = (self.cordes_nombre - 1) * cordes_espacement\
                                + 2 * cordes_offset
            self.create_guitare()

        # On l'affiche à partir de la première frette utilisée
        accord_norm, position_frette = self.get_accord_norm(accord_choisi)
        for n_corde in range(len(self.accord_precedent)):
            note_precedente = self.accord_precedent[n_corde]
            self.canvas1.delete(note_precedente)
        self.accord_precedent = [0] * len(accord_choisi)

        # On dessine, une à une, les notes de l'accord
        for n_corde, n_fret in enumerate(accord_norm) :

            # Définition des couleurs pour les notes jouées :
            if n_fret == 0 : color = None # à vide
            elif n_fret == 'x' : color = 'black'; n_fret = 0 # étouffées
            else : color = 'snow' # normalement

            # Calcul de la position de la note
            x = n_corde * cordes_espacement + cordes_offset
            y = int(n_fret) * frets_espacement + frets_espacement/2
            # Création de la note
            note_nouvelle = self.canvas1.create_oval(x-7,
                                                     y-7,
                                                     x+7,
                                                     y+7,
                                                     fill=color,
                                                     width=2)

            # On enregistre les objets (les notes) pour suppression ulterieure
            self.accord_precedent[n_corde] = note_nouvelle

            # On affiche le numero de frette
            self.canvas1.delete(self.numero_frette)
            self.numero_frette = self.canvas1.create_text(self.frets_taille+15,
                                                     cordes_espacement+20,
                                                     text=str(position_frette),
                                                     font=("Comics", 16))

    def get_accord_norm(self, accord_choisi):
    # corrige la valeur des notes pour afficher uniquement la zone du manche utilisée

        # on trouve la note la plus basse sur le manche qui n'est ni "0" ni "x"
        note_min = 50
        for i, note in enumerate (accord_choisi):
            if isinstance(note, int): # ni x
                if note >= 1 : # ni 0
                    if note < note_min :
                        note_min = note

        # Pour chaque note (ni 0 ni x) on la remonte de note_min sur le manche
        accord_norm=[0]*len(accord_choisi)
        for i, note in enumerate (accord_choisi):
            if isinstance(note, str): # si x
                accord_norm[i] = note
            elif note >= 1 : # si normale
                accord_norm[i] = note - note_min + 1
            else : # si 0
                accord_norm[i] = note

        return accord_norm, note_min-1

############### Boucle #################################
root=tk.Tk()
for i in range(3):
    for j in range (6):
        guitare  = MainGui(root, [i,j])
root.mainloop()
