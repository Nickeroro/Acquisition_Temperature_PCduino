
from pyduino import *
import datetime 

noLoop=True


filepath=""
filename=""
myDataPath=""

compt=0
refTime=None
intervalle=1 


minute0="" 
today0=""  
hour0="" 

def setup():

        global filepath, filename, myDataPath, today0, hour0, minute0, refTime
        myDataPath=("data/text/") 

        createFilename() 

        print filepath

        if exists(filepath):
                print "Le fichier existe"
        else :
                print "Le fichier n'existe pas : creation du fichier"
                myFile=open(filepath,'w') 
                myFile.close()

        loop()

def loop():

        global filepath, filename, myDataPath, today0, hour0, minute0, refTime, compt

        if minute0!=minute():  

                createFilename()

                
                if exists(filepath):
                        print "Le fichier existe"
                else :
                        print "Le fichier n'existe pas : creation du fichier"
                        myFile=open(filepath,'w') 
                        myFile.close()

                addDataToFile(filepath)  

        else: 
                addDataToFile(filepath) 

        compt=compt+1 

        timer(intervalle*1000, loop) 

# -- fin loop --

def addDataToFile(filepathIn):

        global filepath, filename, myDataPath, today0, hour0, minute0, refTime, compt

        myFile=open(filepathIn,'a')
        #myFile=open(filepath,'w') # ouverture pour ecriture avec effacement contenu



        dataValue=str(random(0,1023)) 

        
        # format de donnees utilise : JJ/MM/YYYY hh:mm:ss , val \n
        #dataLine=today('/') + " " + hh +":"+mm + ":" + str(t)+","+dataValue+"\n"
        #dataLine=str(dataTime)+","+dataValue+"\n" # format datetime JJ-MM-AAAA hh:mm:ss
        dataLine=today("-")+ " " + hour() +":"+ minute() +":"+ second() +"," + dataValue+"\n"# format datetime JJ-MM-AAAA hh:mm:ss
        print dataLine 
        myFile.write(dataLine) 

        myFile.close() 

def createFilename() :

        global filepath, filename, myDataPath, today0, hour0, minute0, refTime, compt

        today0=today("_") 
        hour0=hour() 
        minute0=minute() 

        path=homepath()+myDataPath  
        filename="data_"+today0+"_"+hour0+"_"+minute0+".txt" 
        filepath=path+filename 

        print filepath

if __name__=="__main__": 
        setup() 
        while not noLoop: loop() 
 
