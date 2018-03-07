from pyduino import * # importe les fonctions Arduino pour Python

# entete declarative
compt=0 # variable de comptage
ipLocale='127.0.0.1'

print ipLocale # affiche l'adresse IP

port=8080 # attention port doit etre au dessus de 1024 sinon permission refusee par securite - 8080 pour http

serverHTTP=EthernetServer(ipLocale, port) 

files=None 

def setup():

        
        global serverHTTP, ipLocale, port

        
        serverHTTP.begin()

        print ("Serveur TCP actif avec ip : " + ipLocale + " sur port : " + str(port) )


def loop():

        global serverHTTP

        print ("Attente nouvelle connexion entrante...")
        clientDistant, ipDistante = serverHTTP.clientAvailable() 
        

        print "Client distant connecte avec ip :"+str(ipDistante) 

        #--- requete client ---
        requete=serverHTTP.readDataFrom(clientDistant)

        print requete 

        if requete.startswith("GET /ajax"):

                lignesRequete=requete.splitlines() # recupere la requete est list de lignes
                print lignesRequete[0]  # premiere ligne = la requete utile

                params=lignesRequete[0].split('=') # isole la valeur - requete de la forme /ajax=val= donc split "=" isole la valeur
                param=int(params[1]) # 2eme valeur est la valeur recue avec requete ajax
                print param

                
                reponse=( # ( ... ) pour permettre multiligne..
                httpResponse() # entete http OK 200 automatique fournie par la librairie Pyduino

                
                +

                reponseAJAX(param) # voir la fonction separee - pour clarte du code - ici on passe le parametre

                                +"\n") # fin reponse

                serverHTTP.writeDataTo(clientDistant, reponse) # envoie donnees vers client d'un coup

                print "Reponse envoyee au client distant : "
                
                print (reponse) # affiche la reponse envoyee

        #====== si requete GET simple = premiere requete => envoi page HTML+JS initiale ======
        elif requete.startswith("GET"): # si la requete commence par GET seul = premiere page

                print "Requete GETrecue valide"

                
                reponse=( # ( ... ) pour permettre multiligne..
                httpResponse() # entete http OK 200 automatique fournie par la librairie Pyduino

                # contenu page HTML+ JS initiale
                +

                pageInitialeHTMLJS() # voir la fonction separee - pour clarte du code

                +"\n") # fin reponse

                serverHTTP.writeDataTo(clientDistant, reponse) # envoie donnees vers client d'un coup

                print "Reponse envoyee au client distant : "
                #print (bytes(reponse))
                print (reponse) # affiche la reponse envoyee

        #====== si requete pas valide ======
        else : # sinon requete pas valide

                print ("Requete pas valide")


       
        delay(10) # entre 2 loop()

# -- fin loop --

#========== fonction fournissant la page HTML + JS initiale incluant code javascript AJAX ======
def pageInitialeHTMLJS():

        global files

        dirPath=homePath()+"data/text"
        print dirPath

        files=listfiles(dirPath)
        print files

        optionsFiles=""

        # ajoute en premier option choisir
        optionsFiles=optionsFiles+"\t\t\t<option value=\"Choisir\" label=\"Choisir\">Choisir un fichier</option> \n"

        for filename in files:
                print filename

                optionsFiles=optionsFiles+"\t\t\t<option value=\""+filename+"\" label=\""+filename+"\">"+filename+"</option> \n"

        print optionsFiles # debug

        contenuPageInitialeHTMLJS=( # debut page HTML
"""
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>Test reponse Ajax</title>

        <!-- Debut du code Javascript  -->
        <script language="javascript" type="text/javascript">
        <!--

        //--- variables globales ---
        var myselect=null; // objet global
        var mytextarea=null; // objet global

        var delai=1000; // delai auto entre 2 requete Ajax en ms

        //---------- fonction initiale executee au lancement -----
        window.onload = function () { // au chargement de la page

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

                        //setTimeout(function () {requeteAjax(manageReponseAjax);}, delai); // relance delai avant nouvelle requete Ajax

                } // fin fonction gestion de la reponse Ajax

                //-->
                </script>
                <!-- Fin du code Javascript -->


    </head>

    <body>  

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

)  # fin page HTML+JS initiale
        return contenuPageInitialeHTMLJS # la fonction renvoie la page HTML

#===================== Reponse AJAX ==================

#--- fonction fournissant la page de reponse AJAX
def reponseAJAX(indexIn):

        # definition des variables a uiliser dans la reponse
        global files

        if indexIn==0:
                return "Sélectionner un fichier"

        dirPath=homePath()+"data/text/"
        filename=files[indexIn-1] # -1 pour prendre compte option choisir
        filepath=dirPath+filename

        print filepath

        #-- lecture du fichier -- pour debug
        myFile=open(filepath,'r') # ouverture en lecture
        print ("Contenu du fichier : ")
        myFile.seek(0) # se met au debut du fichier
        fileContent= myFile.read() # lit le fichier
        print fileContent

        myFile.close() # fermeture du fichier

        # la reponse
        reponseAjax=( # debut page reponse AJAX

        #filename # renvoie le nom du fichier
        #+"\n"
        fileContent  # contenu du fichier

)  # fin page reponse AJAX
        return reponseAjax# la fonction renvoie la page HTML

#--- obligatoire pour lancement du code --
if __name__=="__main__": # pour rendre le code executable
        setup() # appelle la fonction setup
        while not noLoop: loop() # appelle fonction loop sans fin
