#!/usr/bin/python
# -*- coding: utf-8 -*-

# exemple pyDuino - par X. HINAULT - www.mon-club-elec.fr
# Aout 2013- Tous droits r�serv�s - GPLv3
# voir : https://github.com/sensor56/pyDuino

# Creer un fichier de donnees horodatees de test

from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True

#--- setup ---
def setup():

        myDataPath=("data/text/")

        path=homePath()+myDataPath  # chemin du r�pertoire � utiliser
        filename="testdata.txt" # nom du fichier
        filepath=path+filename # chemin du fichier

        print filepath

        if exists(filepath):
                print "Le fichier existe : le contenu va etre efface"
        else :
                print "Le fichier n'existe pas : le fichier va etre cree"

        #myFile=open(filepath,'a') # ouverture pour ajout de texte
        myFile=open(filepath,'w') # ouverture pour ecriture avec effacement contenu

        #-- ajout de chaines au fichier
        hh=str(hour())
        mm=str(minute())

        for sec in range(60) : # defile 60 secondes theoriques
                dataValue=str(random(0,1023)) # genere une valeur aleatoire entiere

                # format de donnees utilise : JJ/MM/YYYY hh:mm:ss , val \n
                dataLine=today('/') + " " + hh +":"+mm + ":" + str(sec)+","+dataValue+"\n"
                #print dataLine - debug
                myFile.write(dataLine) # ecrit la ligne dans le fichier

        myFile.close() # fermeture du fichier en ecriture

        #-- lecture du fichier --
        myFile=open(filepath,'r') # ouverture en lecture
        print ("Contenu du fichier : ")
        myFile.seek(0) # se met au debut du fichier
        print myFile.read() # lit le fichier

        myFile.close() # fermeture du fichier

        # NB : on peut aussi ouvrir le fichier dans l'editeur pour verifier son contenu

# -- fin setup --

# -- loop --
def loop():
        return  # si vide

# -- fin loop --

#--- obligatoire pour lancement du code --
if __name__=="__main__": # pour rendre le code executable
        setup() # appelle la fonction main
        while not noLoop: loop() # appelle fonction loop sans fin