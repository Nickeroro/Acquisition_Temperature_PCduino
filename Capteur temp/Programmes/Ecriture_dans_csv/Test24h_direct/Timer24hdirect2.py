from pyduino import * 
import datetime 
noLoop=True

today0=today("-")
#--- setup ---
def setup():

        myDataPath=("data/")

        path=("/media/HAKUNA MART/")+myDataPath
        filename=today0+".csv"
        filepath=path+filename 

        print filepath

        if exists(filepath):
                print "Le fichier existe : le contenu va etre efface"
        else :
                print "Le fichier n'existe pas : le fichier va etre cree"

        
        myFile=open(filepath,'w') # ouverture pour ecriture avec effacement contenu

        hh=str(hour())
        mm=str(minute())

        refTime=datetime.datetime(int(year()), int(month()), int(day())) # date a utiliser - heure 00:00:00 si pas precise
        print refTime

        for t in range(288) : 
                dataValue=str(random(22,25)) # genere une valeur aleatoire entiere

                dataTime=refTime+datetime.timedelta(0, t*300) # jours, secondes - ici toutes les minutes
              
                # format de donnees utilise : JJ/MM/YYYY hh:mm:ss , val \n
                #dataLine=today('/') + " " + hh +":"+mm + ":" + str(t)+","+dataValue+"\n"
                dataLine=str(dataTime)+","+dataValue+"\n" # format datetime JJ-MM-AAAA hh:mm:ss
                myFile.write(dataLine) 

        myFile.close() 
        
        myFile=open(filepath,'r') 
        print ("Contenu du fichier : ")
        myFile.seek(0) 
        print myFile.read() 

        myFile.close() 
def loop():
        return  

if __name__=="__main__": 
        setup() 
        while not noLoop: loop()
