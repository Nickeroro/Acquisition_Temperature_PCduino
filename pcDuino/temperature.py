#!/usr/bin/python
# -*- coding: utf-8 -*-


from pyduino import *
import datetime

noLoop=True

filepath=""
filename=""
myDataPath=""

compt=0
refTime=None
intervalle=300

minute0=""
today0=""
hour0=""

temperatureC=""
value=""

def setup():
	
	global filepath, filename, myDataPath, today0, hour0, minute0, refTime
	
	myDataPath=("temperatures/")
	
	createFilename()
	
	if exists(filepath):
			print "le fichier existe"
	else :
			print "le fichier n'existe pas : creation du fichier"
			myFile=open(filepath, 'w')
			myFile.close()
			
	loop()
	
def loop():
	
	global filepath, filename, myDataPath, today0, hour0, minute0, refTime, compt, temperatureC, value
	
	#val =
	value = analogRead(A2);
	tension = value * 3.3 / 4096.0;
	temperatureC = (tension - 0.55) * 100 ;
	
	if today0!=today("_"):  # si the day memorisee est differente minute courante

                createFilename()


        else: 
                addDataToFile(filepath)  #ajoute donnee au fichier

	compt=compt+1
	timer(intervalle*1000, loop)
	
	

def addDataToFile(filepathIn):
	
	global filepath, filename, myDataPath, today0, hour0, minute0, refTime, compt, temperatureC, value
	
	myFile=open(filepathIn, 'a')
	dataValue=str(round(temperatureC, 2))
	
	# format des donneees : JJ/MM/YYYY hh:mm, val \n
	dataLine=today("-") + " " + hour() + ":" + minute() + "," + dataValue+"\n"
	
	print dataLine
	print value
	myFile.write(dataLine)
	myFile.close()

def createFilename() :
	
	global filepath, filename, myDataPath, today0, hour0, minute0, refTime, compt
	
	today0=today("_")
	hour0=hour()
	minute0=minute()
	
	path=("/var/www/SD_card/lost+found/data/")+myDataPath
	filename="data_"+today0+".csv"
	filepath=path+filename
	
	
if __name__=="__main__":
	setup()
	while not noLoop: loop()
	
	
