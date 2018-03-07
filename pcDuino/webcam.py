#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyduino import * 
from pyduinoMultimedia import *

ipLocale=Ethernet.localIP() 

print ipLocale 

port=8081

serverHTTP=EthernetServer(ipLocale, port) 
filepath=""
today0=""

def setup():
	global serverHTTP, ipLocale, port, filepath
	
	serverHTTP.begin() 
	
	print ("Serveur TCP actif avec ip : " + ipLocale + " sur port : " + str(port) )
	filepath=("/var/www/SD_card/lost+found/data/photos/")

	print filepath # debug

	# initialisation webcam
	initWebcam(0,320,240)
	


def loop():
	
	global serverHTTP, filepath, today0
	
	print ("Attente nouvelle connexion entrante...")
	clientDistant, ipDistante = serverHTTP.clientAvailable() 
	
	print "Client distant connecte avec ip :"+str(ipDistante)

	requete=serverHTTP.readDataFrom(clientDistant) 
	
	print requete 
	
	if requete.startswith("GET /?"): # si la requete recue est une reponse de formulaire
		today0=today("_")
		filenameImage=today0+"-"+nowtime("_")+".jpg" # nom image horodate

		print filepath+filenameImage

		captureImage(filepath+filenameImage) 
		
		addTextOnImage(nowdatetime(), 10,height()-20, blue,1) # ajoute texte sur image 

		saveImage(filepath+filenameImage)
		
		
		reponse=( 
		httpResponse() 
		
				+
"""
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>Photographie</title>
        <style type="text/css">
		html {
		background: #cfcfcf;
		height: 100%;
		background-image: url(http://"""+ Ethernet.localIP()+"""/logo.png);
		background-position: right top;
		background-repeat: no-repeat;
		 }
		</style>
    </head>

    <body>    
        <h2>Photo: """+filenameImage+"""</h2> <br>
        <img src="http://"""+ Ethernet.localIP()+"""/SD_card/lost+found/data/photos/"""+filenameImage+""" " class="imageGauche" alt="Photo" />
		<form method=get action="http://"""+ Ethernet.localIP()+""":8081">
            <INPUT type="submit" value="Prendre une autre" name="Envoie">
        </form>
	</body>

</html>
"""
		+"\n") 
		
		serverHTTP.writeDataTo(clientDistant, reponse) # envoie donnees vers client d'un coup
		
		print "Reponse envoyee au client distant"
		
		print (reponse)

	#====== si requete simple = premiere requete ======
	elif requete.startswith("GET"): # si la requete commence par GET seul = premiere page 
		
		print "Requete recue valide"
		
		#--- reponse serveur --- 
		reponse=( # ( ... ) pour permettre multiligne.. 
		httpResponse() # entete http OK 200 automatique fournie par la librairie Pyduino
		
		# contenu page
		+
"""
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>Photographie</title>
      
        <style type="text/css">
	html {
		background: #cfcfcf;
		height: 100%;
		background-image: url(http://"""+ Ethernet.localIP()+"""/logo.png);
		background-position: right top;
		background-repeat: no-repeat;
		 }
	</style>
    </head>

    <body>    
       <h1>Page d'acceuil WebCam</h1>
        <p><h3>Cliquez sur le bouton pour prendre une photographie avec la WebCam du pcDuino.</h3>
        <form method=get action="http://"""+ Ethernet.localIP()+""":8081">
            <INPUT type="submit" value="Prendre une photo" name="Envoi">
        </form>
        </body>

</html>
"""
		+"\n") 
		
		serverHTTP.writeDataTo(clientDistant, reponse) 
		
		print "Reponse envoyee au client distant : "

		print (reponse) 
		
	else : 
		
		print ("Requete pas valide")
		
	delay(10) 
	
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
