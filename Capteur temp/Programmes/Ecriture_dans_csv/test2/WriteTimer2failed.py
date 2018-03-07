from pyduino import *
import datetime

noLoop=True

filepath=""
filename=""
myDataPath=""

filepath2=""
filename2=""
myDataPath2=""

compt=0
refTime=None
intervalle=1

minute0=""
today0=""
hour0=""

temperatureC=""

def setup():
	
	global filepath, filename, myDataPath,filepath2, filename2, myDataPath2, today0, hour0, minute0, refTime
	
	myDataPath=("test2/")
	myDataPath2=("DailyLog/")
	
	createFilename()
	if exists(filepath):
			print "le fichier existe"
			myFile=open(filepath, 'w')
			myFile.close()
	else :
			print "le fichier n'existe pas : creation du fichier"
			myFile=open(filepath, 'w')
			myFile.close()
	
	createFilename2()
	if exists(filepath2):
			print "le fichier existe"
			myFile=open(filepath2, 'w')
			myFile.close()
	else :
			print "le fichier n'existe pas : creation du fichier"
			myFile=open(filepath2, 'w')
			myFile.close()
	loop()
	
def loop():
	
	global filepath, filename, myDataPath, filepath2, filename2, myDataPath2, today0, hour0, minute0, refTime, compt, temperatureC
	
	#val =
	value = analogRead(A2);
	tension = value * 3.3 / 4096.0;
	temperatureC = (tension - 0.55) * 100 ;
	
	for sec in range(1) :
		addDataToFile(filepath)

	compt=compt+1
	timer(intervalle*1000, loop)
	
	if minute0!=minute() :
		createFilename2()
		if exists(filepath2):
			print "le fichier existe"
		else :
			print "creation du dailylog"
			myFile=open(filepath2, 'w')
			myfile.close()
		addDataToFile(filepath2)
	else :
		addDataToFile(filepath2)

		compt=compt+1
		timer(intervalle*1000, loop)

def addDataToFile(filepathIn):
	
	global filepath, filename, myDataPath, filepath2, filename2, myDataPath2, today0, hour0, minute0, refTime, compt, temperatureC
	
	myFile=open(filepathIn, 'a')
	dataValue=str(temperatureC)
	
	# format des donneees : JJ/MM/YYYY hh:mm, val \n
	dataLine=today("-") + " " + hour() + ":" + minute() + ":" + second() + "," + dataValue+"\n"
	
	print dataLine
	myFile.write(dataLine)
	myFile.close()

def createFilename() :
	
	global filepath, filename, myDataPath, filepath2, filename2, myDataPath2, today0, hour0, minute0, refTime, compt
	
	today0=today("-")
	hour0=hour()
	minute0=minute()
	
	path=("/var/www/")+myDataPath
	filename="datafile.csv"
	filepath=path+filename

def createFilename2() :
	global filepath, filename, myDataPath, filepath2, filename2, myDataPath2, today0, hour0, minute0, refTime, compt
	
	today0=today("-")
	hour0=hour()
	minute0=minute()
	
	path2=("/var/www/")+myDataPath2
	filename2=today0+".csv"
	filepath2=path2+filename2
	
if __name__=="__main__":
	setup()
	while not noLoop: loop()
	
	
