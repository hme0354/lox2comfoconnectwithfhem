#!/bin/bash

echo	"--------------------------------------------------------------------------"
echo 	"     Install Skript comfoconnect for Loxone with loxberry & FHEM V0.0     "
echo 	"--------------------------------------------------------------------------"
echo

echo "Update durchgeführen"

apt update

echo

python3=$(python3 --version | grep "Python 3." | wc -l)

if [ $python3 == 1 ]; then
	export PYTHON3_VERSION=`python3 -c 'import sys; version=sys.version_info[:3]; print("{0}.{1}.{2}".format(*version))'`
	paresed_PYTHON3_Version=$(echo "${PYTHON3_VERSION//./}")
	echo "Python3 Version" $PYTHON3_VERSION "installiert"
	echo
else
	echo "Python3 nicht installiert"
fi

if [ "$paresed_PYTHON3_Version" -ge "373" ]; then 
    echo "Korrekte Python3 Version installiert"
else
    echo "Falsche Python3 Version installiert!"
	echo 
	echo "Python3 installieren"
	apt install git python3
fi

echo
echo "Paket python3-setuptools installieren"

apt-get install python3-setuptools

echo
echo "Comfoconnect herunterladen von github"
echo

cd Scripts/
git clone https://github.com/hme0354/comfoconnect.git
cd comfoconnect/

echo "Paket Comfoconnect installieren"

python3 setup.py install

cd Scripts/lox2comfoconnectwithfhem/

#cd ~
#mkdir Scripts
#git clone https://github.com/hme0354/lox2comfoconnectwithfhem.git

echo

echo	"--------------------------------------------------------"
echo	"     Einstellungen Comfoconnect LAN-C Schnittstelle     "
echo	"--------------------------------------------------------"

echo

echo	"Passwort-Abfrage für Zehnder Q-Serie"
echo	"NUR ZAHLEN ERLAUBT"
echo	"Bei keinem gesetzten Passwort 0 eingeben oder leer lassen"

echo

for ((i=1; i<3; i++))
do
	read -p "Passwort Comfoconnect eingeben:" -r -s pw1
	echo
	if [ -z "$pw1" ]; then
		pw1=0
	fi

	read -p "Passwort erneut eingeben: " -r -s pw2
	echo
	if [ -z "$pw2" ]; then
		pw2=0
	fi

	if [ "$pw1" -ge "$pw2" ]; then
		echo "Eingabe korrekt!"
		pw=$pw1
		i=3
	else
		echo "Falsche Eingabe! Bitte wiederholen."
		echo
		i=0
	fi
done

pw_text="pin = $pw1"

cd Scripts/lox2comfoconnectwithfhem
perl -npi -e 's/pin = 0/'"$pw_text"'/g' ccfhem.py

mkdir -p /opt/loxberry/webfrontend/legacy/fhem/scripts
cp -i -r ccfhem.py /opt/loxberry/webfrontend/legacy/fhem/scripts
chmod 755 /opt/loxberry/webfrontend/legacy/fhem/scripts/ccfhem.py

rm ccfhem.py

echo

for ((i=1; i<4; i++));
do
	echo "IP-Adresse Comfoconnect LAN-C Schnittstelle eingeben:"
	read IP_Comfo
	
	if echo $IP_Comfo |egrep '.*\..*\..*\..*' >/dev/null 2>&1; then

		counter=1
		start=0
		stop=255

		while [ $counter -le '4' ]; do
			if [ ! `echo $IP_Comfo|awk -F. '{print $'$counter'}'` -ge $start ] || \
			[ ! `echo $IP_Comfo|awk -F. '{print $'$counter'}'` -le $stop ]; then
				echo "IP ungültig"
				exit 1
			fi
			counter=`expr $counter + 1`
			if [ $counter -eq '4' ]; then
				start=`expr $start + 1`
			fi
		done
		echo "IP-Adresse gültig!"
		i=4
	else
		echo "falscher Syntax!"
		echo
	fi
	
	if	[[	$i -eq 3 ]]; then
		echo	"Dritte falsche Eingabe!"
		echo	"Abbruch!"
		exit 1
	fi
done

echo

ping -c1 $IP_Comfo > /dev/null
if [ $? -eq 0 ]
then 
	echo	"Comfoconnect erreichbar"
else
	echo	"Comfoconnect nicht erreichbar"
	echo	"Möglicherweise falsche IP-Adresse"
	echo	"Bitte nochmals ausführen!"
	exit 1
fi

echo
echo	"---------------------------------------"
echo	"     Abfrage IP-Adresse Miniserver     "
echo	"---------------------------------------"
echo

IP_MS=$(jq -r '.Miniserver["1"].Ipaddress' "$LBSCONFIG/general.json")

if [[ "$IP_MS" == "null" ]]; then
	echo	"Miniserver nicht konfiguriert!"
	echo	"Miniserver in Loxberry konfigurieren und Skript erneut ausführen."
	exit 1
fi

echo	$IP_MS

echo
echo	"-------------------------------------"
echo	"     Analyse ob FHEM installiert     "
echo	"-------------------------------------"
echo

if	[ -d "/opt/fhem"	];
then
	pfad_fhem="/opt/fhem"
	echo	"FHEM im Pfad" $pfad_fhem "installiert"
elif	[ -d "/opt/loxberry/data/plugins/fhem/FHEM"	];
then
	pfad_fhem="/opt/loxberry/data/plugins/fhem/FHEM"
	echo	"FHEM im Pfad" $pfad_fhem "installiert"
else
	echo	"FHEM nicht installiert!"
	echo	"Programm wird beendet!"
	exit 1
fi

echo
echo	"----------------------------"
echo	"     FHEM konfigurieren     "
echo	"----------------------------"
echo
echo	"IP-Adresse auslesen"
echo

ip="$(ip addr show eth0 | grep -vw "inet6" | grep "global" | grep -w "inet" | cut -d/ -f1 | awk '{ print $2 }')"

echo	$ip
echo

echo	"Datei 99_myUtils.pm IP-Adresse Miniserver einstellen und verschieben"

cd Scripts/lox2comfoconnectwithfhem
perl -npi -e 's/MS_IP/'"$IP_MS"'/g' rm 99_myUtils.pm
cp -i -r rm 99_myUtils.pm $pfad_fhem

echo
echo	"Telnet einstellen"

curl -q "http://$ip:8083/fhem?cmd=define%20telnetPort%20telnet%207072%20global"
curl -q "http://$ip:8083/fhem?cmd=attr%20telnetPort%20room%20Zentral"

#echo
#echo	"Sicherheitsmodus deaktivieren"

perl /opt/fhem/fhem.pl 7072 "attr WEB.* csrfToken none"
#curl -q "http://$ip:8083/fhem?cmd=attr%20WEB.*%20scrfToken%20none"

echo
echo	"Comfoconnect erstellen"

curl -q "http://$ip:8083/fhem?cmd=define%20comfoconnect%20dummy"

echo
echo	"Symbol erstellen"

perl /opt/fhem/fhem.pl 7072 "attr comfoconnect devStateIcon {".*:vent_ventilation_level_".ReadingsVal("comfoconnect","Stufe",0).(ReadingsVal("comfoconnect","Modus",0) ne -1 ? '@green' : "")}"
##################curl -q "http://$ip:8083/fhem?cmd=attr%20comfoconnect%20devStateIcon%20{%22.*:vent_ventilation_level_%22.ReadingsVal(%22comfoconnect%22,%22Stufe%22,0).(ReadingsVal(%22comfoconnect%22,%22Modus%22,0)%20ne%20-1%20?%20'@green'%20:%20%22%22)}"

echo
echo	"Einstellungen vornehmen"

perl /opt/fhem/fhem.pl 7072 "attr comfoconnect userReadings ModusTXT {if(ReadingsVal("comfoconnect","Modus","") == -1) {return "Auto"} elsif (ReadingsVal("comfoconnect","Modus","") == 1) {return "Manuell Zeit"} elsif (ReadingsVal("comfoconnect","Modus","") == 5) {return "Manuell"} elsif (ReadingsVal("comfoconnect","Modus","") == 6) {return "Partymodus"} elsif (ReadingsVal("comfoconnect","Modus","") == 7) {return "AbwesendAPP"} else {return "Fehler"}}, NextTime {hex(substr(ReadingsVal("comfoconnect","Next",0),4,2))*65280+hex(substr(ReadingsVal("comfoconnect","Next",0),2,2))*255+hex(substr(ReadingsVal("comfoconnect","Next",0),0,2))}, BypassZeit {hex(substr(ReadingsVal("comfoconnect","BypassZeitHEX",0),4,2))*65280+hex(substr(ReadingsVal("comfoconnect","BypassZeitHEX",0),2,2))*255+hex(substr(ReadingsVal("comfoconnect","BypassZeitHEX",0),0,2))}"
##################curl -q "http://$ip:8083/fhem?cmd=attr%20comfoconnect%20userReadings%20ModusTXT%20{if(ReadingsVal(%22comfoconnect%22,%22Modus%22,%22%22)%20==%20-1)%20{return%20%22Auto%22}%20elsif%20(ReadingsVal(%22comfoconnect%22,%22Modus%22,%22%22)%20==%201)%20{return%20%22Manuell%20Zeit%22}%20elsif%20(ReadingsVal(%22comfoconnect%22,%22Modus%22,%22%22)%20==%205)%20{return%20%22Manuell%22}%20elsif%20(ReadingsVal(%22comfoconnect%22,%22Modus%22,%22%22)%20==%206)%20{return%20%22Partymodus%22}%20elsif%20(ReadingsVal(%22comfoconnect%22,%22Modus%22,%22%22)%20==%207)%20{return%20%22AbwesendAPP%22}%20else%20{return%20%22Fehler%22}},%20NextTime%20{hex(substr(ReadingsVal(%22comfoconnect%22,%22Next%22,0),4,2))*65280+hex(substr(ReadingsVal(%22comfoconnect%22,%22Next%22,0),2,2))*255+hex(substr(ReadingsVal(%22comfoconnect%22,%22Next%22,0),0,2))},%20BypassZeit%20{hex(substr(ReadingsVal(%22comfoconnect%22,%22BypassZeitHEX%22,0),4,2))*65280+hex(substr(ReadingsVal(%22comfoconnect%22,%22BypassZeitHEX%22,0),2,2))*255+hex(substr(ReadingsVal(%22comfoconnect%22,%22BypassZeitHEX%22,0),0,2))}"

echo
echo	"Abfrage Daten konfigurieren"

curl -q "http://$ip:8083/fhem?cmd=define%20Q350ToLoxone%20notify%20.*:DrehzahlAbluftventilator.*%20{Q350ToLoxone(%22%24NAME%22)}"

echo	
echo	"Autostart vom CCFHEM Skript konfigurieren"

curl -q "http://$ip:8083/fhem?cmd=define%20FHEMStart%20notify%20global:INITIALIZED.*%20{system(%22python3%20/opt/loxberry/webfrontend/legacy/fhem/scripts/ccfhem.py%20--ip%20$IP_Comfo%20&%22)}"

echo
echo	"Raum Zentral zuweisen"

curl -q "http://$ip:8083/fhem?cmd=attr%20comfoconnect%20room%20Zentral"
curl -q "http://$ip:8083/fhem?cmd=attr%20FHEMStart%20room%20Zentral"
curl -q "http://$ip:8083/fhem?cmd=attr%20Q350ToLoxone%20room%20Zentral"

echo
echo	"Einstellungen in FHEM speichern"
echo

curl -q "http://$ip:8083/fhem?cmd=save"

echo	"-------------------------------------------"
echo	"	Installationsdateien werden gelöscht	"
echo	"-------------------------------------------"
echo

#rm -r Scripts/

echo	"-----------------------------------"
echo	"     Installation beendet!         "
echo	"          Viel Spaß!               "
echo	"     Copyright © 2020  hme0354     "
echo
echo	"     All rights reserved           "
echo	"-----------------------------------"

#exec restart