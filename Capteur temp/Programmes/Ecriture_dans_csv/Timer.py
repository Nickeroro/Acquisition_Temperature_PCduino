
from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
noLoop=True

#--- setup ---
def setup():

        myDataPath=("data/text/")

        path=homePath()+myDataPath  # chemin du répertoire à utiliser
        filename="testdata.txt" # nom du fichier
        filepath=path+filename # chemin du fichier

        print filepath

        if exists(filepath):
                print "Le fichier existe : le contenu va etre efface"
        else :
                print "Le fichier n'existe pas : le fichier va etre cree"

       
        myFile=open(filepath,'w') #

        hh=str(hour())
        mm=str(minute())
#val =
	value = analogRead(A2);
	tension = value * 3.3 / 4096.0;
	temperatureC = (tension - 0.55) * 100 ;
	
        for sec in range(60) : # defile 60 secondes theoriques
                dataValue=str(temperatureC) # genere une valeur aleatoire entiere

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

def loop():
        return  # si vide

if __name__=="__main__": 
        setup() # appelle la fonction main
        while not noLoop: loop() # appelle fonction loop sans fin
