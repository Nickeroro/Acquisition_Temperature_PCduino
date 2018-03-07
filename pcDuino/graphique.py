#!/usr/bin/python
# -*- coding: utf-8 -*-


from pyduino import * 

import numpy as np

compt=0 
ipLocale=Ethernet.localIP() 

print ipLocale 
port=8080 
serverHTTP=EthernetServer(ipLocale, port) 

data=None 
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

        requete=serverHTTP.readDataFrom(clientDistant) 

        print requete 
        
        if requete.startswith("GET /ajax"): 
        
                lignesRequete=requete.splitlines()
                print lignesRequete[0]  

                params=lignesRequete[0].split('=') 
                param=int(params[1]) 
                print param

                reponse=( 
                httpResponse() 

                +

                reponseAJAX(param) 

                                +"\n") 

                serverHTTP.writeDataTo(clientDistant, reponse) 

                print "Reponse envoyee au client distant : "
                print (reponse) 

        elif requete.startswith("GET"):  

                print "Requete GETrecue valide"

                global compt
                compt=0 

                reponse=( 
                httpResponse() 
                
                +

                pageInitialeHTMLJS() 

                +"\n") 

                serverHTTP.writeDataTo(clientDistant, reponse) 

                print "Reponse envoyee au client distant : "
                
                print (reponse) 

       
        else :

                print ("Requete pas valide")


        
        delay(10) 

def pageInitialeHTMLJS():

        myDataPath=("temperatures/")

        path=("/var/www/SD_card/lost+found/data/")+myDataPath  
        filename="data_"+today("_")+".csv" 
        filepath=path+filename 

        myFile=open(filepath,'r') 
        print ("Contenu du fichier : ")
        myFile.seek(0) 

        linesList=myFile.readlines() 

        myFile.close() 

        print linesList

        dataGraph=""

        for dataLine in linesList[:-1]:
                dataGraph=dataGraph+"\""+dataLine.rstrip('\n')+" \\n \" +" + "\n" # dataLine.rstrip('\n') = enleve \n de la ligne

        dataGraph=dataGraph+"\""+linesList[-1].rstrip('\n')+" \\n \" "

        global files

        dirPath="/var/www/SD_card/lost+found/data/temperatures/"
        print dirPath

        files=listfiles(dirPath)
        print files

        optionsFiles=""

        for filename in files:
                print filename

                optionsFiles=optionsFiles+"\t\t\t<option value=\""+filename+"\" label=\""+filename+"\">"+filename+"</option> \n"
                print optionsFiles
                
        optionsGraph="""
        labels: [ "Date", "Temperature"], // labels series
        width : 800,
        height: 400, 
        ylabel: 'Temperature (C)',
        xlabel: 'Temps (h)',
        title: 'Temperature de la salle du moteur hydraulique',
        valueRange: [10,40],
        showRangeSelector: true ,
        """



        contenuPageInitialeHTMLJS=( 
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
    <head>
        <meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7; IE=EmulateIE9" />
		<title>Temperature Graphique</title>

<style type="text/css">
	html {
		background: #cfcfcf;
		height: 100%;
		background-image: url(http://"""+ Ethernet.localIP()+"""/logo.png);
		background-position: right top;
		background-repeat: no-repeat;
		 }
</style>

        <!-- Debut du code Javascript  -->
        <script language="javascript" type="text/javascript">
        <!--

        function path(jsFileNameIn) { // fonction pour fixer chemin absolu                              
                        var js = document.createElement("script");
                        js.type = "text/javascript";
                        js.src = "http://"+window.location.hostname+":80"+"/javascript/dygraphs/"+jsFileNameIn;

                        document.head.appendChild(js);

                }
                          
                path('dygraph-combined.js');

        var myselect=null;
        var mytextarea=null;

        var textInputDygraphs=null;
 
        window.onload = function () { 


                        textInputDygraphs=document.getElementById("valeurDygraphs");

                        g = new Dygraph( 
                        
                        document.getElementById("graphdiv"),

"""
        +
        dataGraph
        +
""",

                        {
"""
        +
        optionsGraph
        +
"""
                        } 


                        ); 

                        myselect=document.getElementById("liste");
                        mytextarea=document.getElementById("text");

                        mytextarea.value="Selectionner un fichier";

                        for (var i=0; i<myselect.options.length; i++){

                        }                

                        myselect.onchange=function () {
                                var index=this.selectedIndex
                                requeteAjax(index,manageReponseAjax);
                                }


        } 
         function println(textIn) { 
                                        var txt=textIn;

                                        var newtext = document.createTextNode(txt);
                                        document.body.appendChild(newtext);

                                        document.body.appendChild(document.createElement("br")); // ajoute saut de ligne

                                        document.body.appendChild(newtext);  

                                }

        function requeteAjax(chaineIn, callback) { 

						var xhr;
						if (window.XMLHttpRequest) {
						xhr = new XMLHttpRequest();
						} else {
						xhr = new ActiveXObject("Microsoft.XMLHTTP");
						} 
						
						xhr.open("GET", "/ajax="+chaineIn+"=", true); 
                        xhr.send(null);

                        xhr.onreadystatechange = function() { 
                                if (xhr.readyState == 4 && xhr.status == 200) {
                                        callback(xhr.responseText); 
                                }
                        };

                }

                function manageReponseAjax(stringDataIn) { 

                        mytextarea.value=stringDataIn; 

                        g.updateOptions( { 'file': stringDataIn } ); 
                        
                        textInputDygraphs.value=Number(g.getValue(0,g.numColumns()-1) );

                }

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

        dirPath="/var/www/SD_card/lost+found/data/temperatures/"
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
