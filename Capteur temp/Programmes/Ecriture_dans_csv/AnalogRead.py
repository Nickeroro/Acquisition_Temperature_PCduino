
from pyduino import * # importe les fonctions Arduino pour Python

def setup():
	return
	
def loop():
	
	value = analogRead(A2);
	tension = value * 3.3 / 4096.0;
	temperatureC = (tension - 0.55) * 100 ;
		
	Serial.println ("temperature (C) = " + str("%.2f" % temperatureC))
	
	delay(1000)

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction main
	while not noLoop: loop() # appelle fonction loop sans fin




