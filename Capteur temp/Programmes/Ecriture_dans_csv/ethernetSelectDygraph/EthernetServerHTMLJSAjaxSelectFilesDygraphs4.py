
from pyduino import * 
import numpy as np


compt=0 # variable de comptage 
#ipLocale=Ethernet.localIP()
 
#ipLocale='192.168.1.25'
ipLocale='127.0.0.1'


print ipLocale 

port=8080 # attention port doit etre au dessus de 1024 sinon permission refusee par securite - 8080 pour http

serverHTTP=EthernetServer(ipLocale, port) 

data=None 

files=None # liste des fichiers

def setup():
	
	# -- serveur TCP -- 
	global serverHTTP, ipLocale, port
	
	#serverHTTP.begin(10) # initialise le serveur - fixe nombre max connexion voulu
	serverHTTP.begin() # nombre max connexion par defaut = 5
	
	print ("Serveur TCP actif avec ip : " + ipLocale + " sur port : " + str(port) )

# -- loop -- 
def loop():
	
	global serverHTTP
	
	print ("Attente nouvelle connexion entrante...")
	clientDistant, ipDistante = serverHTTP.clientAvailable() # attend client entrant 
	
	
	print "Client distant connecte avec ip :"+str(ipDistante) # affiche IP du client

	#--- requete client ---
	requete=serverHTTP.readDataFrom(clientDistant) # lit les donnees en provenance client d'un coup
	
	print requete # affiche requete recue
	
	# analyse de la requete
	
	#====== si requete ajax ======
	if requete.startswith("GET /ajax"): # si la requete recue est une requete ajax
		
		lignesRequete=requete.splitlines() # recupere la requete est list de lignes
		print lignesRequete[0]  # premiere ligne = la requete utile
		
		params=lignesRequete[0].split('=') # isole la valeur - requete de la forme /ajax=val= donc split "=" isole la valeur
		param=int(params[1]) # 2eme valeur est la valeur recue avec requete ajax
		print param
		
		#--- reponse serveur requete formulaire --- 
		reponse=( # ( ... ) pour permettre multiligne.. 
		httpResponse() # entete http OK 200 automatique fournie par la librairie Pyduino
		
		# contenu reponse AJAX
		+
		
		reponseAJAX(param) # voir la fonction separee - pour clarte du code - ici on passe le parametre 
		
				+"\n") # fin reponse 
		
		serverHTTP.writeDataTo(clientDistant, reponse) # envoie donnees vers client d'un coup
		
		print "Reponse envoyee au client distant : "
		#print (bytes(reponse))
		print (reponse) # affiche la reponse envoyee

	#====== si requete GET simple = premiere requete => envoi page HTML+JS initiale ======
	elif requete.startswith("GET"): # si la requete commence par GET seul = premiere page 
		
		print "Requete GETrecue valide"
		
		#-- code Pyduino a executer au besoin 
		global compt
		compt=0 # RAZ compt
		
		#--- reponse serveur requete initiale --- 
		reponse=( # ( ... ) pour permettre multiligne.. 
		httpResponse() # entete http OK 200 automatique fournie par la librairie Pyduino
		
		# contenu page HTML+ JS initiale
		+
		
		pageInitialeHTMLJS() # voir la fonction separee - pour clarte du code
		
		+"\n") # fin reponse 
		
		serverHTTP.writeDataTo(clientDistant, reponse) # envoie donnees vers client d'un coup
		
		print "Reponse envoyee au client distant : "

		print (reponse) 
		
	#====== si requete pas valide ======
	else : 
	
		print ("Requete pas valide")
		

	delay(10) 
	

#========== fonction fournissant la page HTML + JS initiale incluant code javascript AJAX ======
def pageInitialeHTMLJS():
	
	# code Python a executer avant envoyer page 
	
	myDataPath=("data/text/")
	
	path=homePath()+myDataPath  
	filename=today("_",-1)+".txt" # nom du fichier du jour 
	filepath=path+filename 
	
	myFile=open(filepath,'r') 
	print ("Contenu du fichier : ")
	myFile.seek(0) 
	
	linesList=myFile.readlines() 
	
	myFile.close()

	print linesList
	
	dataGraph=""
	
	for dataLine in linesList[:-1]: 
		dataGraph=dataGraph+"\""+dataLine.rstrip('\n')+" \\n \" +" + "\n" 
	
	dataGraph=dataGraph+"\""+linesList[-1].rstrip('\n')+" \\n \" " 
	
	global files
	
	dirPath=homePath()+"data/text"
	print dirPath
	
	files=listfiles(dirPath)
	print files
	
	optionsFiles=""
	
	for filename in files:
		print filename
		
		optionsFiles=optionsFiles+"\t\t\t<option value=\""+filename+"\" label=\""+filename+"\">"+filename+"</option> \n"
		print optionsFiles
		
	optionsGraph=	"""
		labels: [ "Date", "Temperature(C)"],      
		width: 800,
		heigh: 400,
		valueRange: [0,70],
		showRangeSelector: true,
		rangeSelectorPlotStrokeColor: 'green',
		ylabel: 'Temperature (C)',
		title: 'Temperature de la salle du moteur hydraulique',
					"""
	

	
	contenuPageInitialeHTMLJS=( 
"""
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="X-UA-Compatible" content="text/html; charset=UTF-8; IE=EmulateIE6; IE=EmulateIE7; IE=EmulateIE9" /> <!-- Encodage de la page -->
        <title>Test reponse Ajax</title>
        
        <!-- Debut du code Javascript  -->
        <script language="javascript" type="text/javascript">
        <!-- 
        
        // code javascript par X. HINAULT - www.mon-club-elec.fr - tous droits reserves - 2013 - GPL v3

        function path(jsFileNameIn) { // fonction pour fixer chemin absolu                              
			var js = document.createElement("script");
			js.type = "text/javascript";
			js.src = " http://www.mon-club-elec.fr/mes_javascripts/dygraphs/dygraph-combined.js"; // <=== serveur externe - modifier chemin ++ si besoin
			js.src = "http://127.0.0.1/javascript/dygraphs/dygraph-combined.js";
			js.src = "http://"+window.location.hostname+":80"+"/javascript/dygraphs/dygraph-combined.js"; // si utilisation server http local port 80

			document.head.appendChild(js);                                  
			//alert(js.src); // debug

		} // fin fonction path

        //--- variables globales ---
        var myselect=null; // objet global
        var mytextarea=null; // objet global 
        
        var textInputDygraphs=null; // objet global 
        
        //var delai=1000; // delai en ms entre 2 requetes AJAX - pas utilise ici 
		var val=0;
        
        
        //---------- fonction initiale executee au lancement -----
        window.onload = function () { // au chargement de la page
        
        
			// dygraphs 
			textInputDygraphs=document.getElementById("valeurDygraphs");
			
			g = new Dygraph( // cree l'objet du graphique

			// containing div
			document.getElementById("graphdiv"), // objet div utilise appele par son nom

			// CSV ou chemin fichier CSV.

"""
	+ 
	dataGraph 
	+
""",

			//-- parametres a utiliser pour le graphique
			{
"""
	+ 
	optionsGraph
	+
"""
			} // fin parametres


			); // fin declaration Dygraph
			
			// liste deroulante 
			
			myselect=document.getElementById("liste");
			mytextarea=document.getElementById("text");
			
			mytextarea.value="Selectionner un fichier"; 
			
			for (var i=0; i<myselect.options.length; i++){

				//println("Option index "+i + ":" + myselect.options[i].text + " (" + myselect.options[i].value + ")") // affiche la liste des options - debug

			} // fin for                  

            // fonction de gestion d'un changement select - ici placee dans le code JS initial
			myselect.onchange=function () {

				var index=this.selectedIndex
				//println ("Index courant ="+index + " soit : " + this.options[index].text); // this represent myselect - debug
				
				requeteAjax(index,manageReponseAjax);
				//println("Envoi requete Ajax"); - debug
				
				} // fin fonction onchangeSelect
        
        
            //setTimeout(function () {requeteAjax(manageReponseAjax);}, delai); // setTimeOut avec fonction inline : 1er appel de la fonction requete Ajax
            // nb : setTimeout() n'applique delai qu'une fois
        } // fin onload
        
        //---- fonctions utiles ---

         function println(textIn) { // fonction pour ajouter un element a la page - utile ++ pour debug

        // Ajouter un element a la page sans effacer le reste
        //var txt = 'Hello';

                                        var txt=textIn;

                                        var newtext = document.createTextNode(txt);
                                        document.body.appendChild(newtext);

                                        document.body.appendChild(document.createElement("br")); // ajoute saut de ligne

                                        document.body.appendChild(newtext);  

                                } // fin println
                                
        //---------- fonction de requete AJAX -----
        function requeteAjax(chaineIn, callback) { // la fonction recoit en parametre la fonction de callback qui gere la reponse Ajax
			// la fonction de callback appelee sera celle definie dans setTimeOut : manageAjaxData
			var xhr = XMLHttpRequest(); // declare objet de requete AJAX  - OK Firefox
			
			xhr.open("GET", "/ajax="+chaineIn+"=", true); // definition de la requete envoyee au serveur ici : GET /ajax
			xhr.send(null); // envoi de la requete
			
			xhr.onreadystatechange = function() { // fonction de gestion de l'evenement onreadystatechange
				if (xhr.readyState == 4 && xhr.status == 200) { // si reponse OK
					callback(xhr.responseText); // appel fonction gestion reponse en passant texte reponse en parametre
				} // fin if 
			}; // fin function onreadystatechange
			
		} // fin fonction requeteAjax
		
		//------ fonction qui sera utilisee en fonction de callback = gestion de la reponse Ajax
		function manageReponseAjax(stringDataIn) { // la fonction recoit en parametre la chaine de texte de la reponse Ajax
			
			
			//println (stringDataIn) // debug
			
			mytextarea.value=stringDataIn; // affiche le contenu du fichier dans le champ
			
			// ici la fonction assure actualise le graphique
			
			
			// met a jour donnees a partir chaine recue
			g.updateOptions( { 'file': stringDataIn } ); // met a jour les donnees du graphique
			
			// recupere derniere valeur
			textInputDygraphs.value=Number(g.getValue(0,g.numColumns()-1) ); // derniere valeur du graphique
			// voir : http://dygraphs.com/jsdoc/symbols/Dygraph.html
			
			//setTimeout(function () {requeteAjax(manageReponseAjax);}, delai); // relance delai avant nouvelle requete Ajax
			
		} // fin fonction gestion de la reponse Ajax
		
		//-->
		</script>
		<!-- Fin du code Javascript -->
	
        
    </head>

    <body>  
      
    <div id="graphdiv"></div>
	<br/>
	Valeur courante = <input type="text" id="valeurDygraphs" />
	
	<br/>
	
	
		<select  style="width: 300px" id="liste" >
"""
+

optionsFiles

+
"""
		</select>
		
		<br/>
	
	<textarea id="text" rows="30" cols="100"></textarea>
	
	</body>

</html>
"""

)  
	return contenuPageInitialeHTMLJS 


def reponseAJAX(indexIn):
	
	
	global files
	
	dirPath=homePath()+"data/text/"
	filename=files[indexIn]
	filepath=dirPath+filename
	
	print filepath
	
	
	myFile=open(filepath,'r') 
	print ("Contenu du fichier : ")
	myFile.seek(0) 
	fileContent= myFile.read() 
	print fileContent
	
	myFile.close() 
	
	
	reponseAjax=( 
	
	fileContent  	
) 
	return reponseAjax
        

if __name__=="__main__": 
	setup() 
	while not noLoop: loop() 
