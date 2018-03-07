#!/bin/bash

# by X. HINAULT - 2013 - 2016 - GPL v3

echo "--- Installation de la librairie Pyduino sur votre système ---"

echo "Installation de l'utilitaire unzip..."
sudo apt-get install unzip --yes

echo "Installation des dépendances utiles..."
sudo apt-get install python-scipy --yes # sans virgules



# installation des fichiers de la lib pyduino - utiliser chemins absolus pour eviter problemes
echo "Téléchargement de l'archive pyduino.zip..."

cd /tmp
sudo wget -4 -N http://cloud-mon-club-elec.fr:8080/ateliers_python/libs_python/__pyduino -O /tmp/pyduino.zip
#sudo wget -4 -N http://cloud-mon-club-elec.fr:8080/ateliers_python/libs_python/__pyqtcv_dev -O /tmp/pyqtcv.zip

echo "Extraction de l'archive pyduino.zip..."

sudo unzip /tmp/pyduino.zip

echo "Sauvegarde de la librairie pyduino installée précédemment..."
now=$(date +"%m_%d_%Y_%H_%M_%S")
sudo mkdir /usr/lib/python2.7/dist-packages/pyduino_bak_$now/
sudo mv /usr/lib/python2.7/dist-packages/pyduino/* /usr/lib/python2.7/dist-packages/pyduino_bak_$now/


echo "Effacement du répertoire de la librairie pyduino installée précédemment..."
sudo rm /usr/lib/python2.7/dist-packages/pyduino/ -r

echo "Installation des nouveaux fichiers de la librairie pyqtcv..."
sudo mv /tmp/__pyduino /usr/lib/python2.7/dist-packages/pyduino

echo "Finalisation installation du module pyduino..."
FILE="/usr/lib/python2.7/dist-packages/pyduino.pth"
 
if [ -f "$FILE" ];
then
   echo "Le fichier $FILE existe."
else
   echo "Le $FILE n'existe pas et va être créé" 
   #sudo touch $FILE # cree le fichier
   # sudo echo "pyqtcv" > /usr/lib/python2.7/dist-packages/pyqtcv.pth # ne fonctionne pas !
   echo 'pyduino' | sudo tee --append $FILE
fi

echo "Installation terminée"
read -p "<OK>" 
# pour attendre entrée pour sortir

exit 0;