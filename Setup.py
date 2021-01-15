#!/bin/bash

echo	"-------------------------------------------------------------------------------"
echo 	"     Install Skript comfoconnect for Loxone with loxberry V2.2 & FHEM V0.0     "
echo 	"-------------------------------------------------------------------------------"
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

cd
cd Scripts/
git clone https://github.com/hme0354/comfoconnect.git
cd comfoconnect/

echo "Paket Comfoconnect installieren"

python3 setup.py install

cd
cd Scripts/lox2comfoconnectwithfhem/

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

cd
cd Scripts/lox2comfoconnectwithfhem
perl -npi -e 's/pin = 0/'"$pw_text"'/g' ccfhem.py

mkdir -p /opt/loxberry/webfrontend/legacy/fhem/scripts
cp -i -r ccfhem.py /opt/loxberry/webfrontend/legacy/fhem/scripts
chmod 755 /opt/loxberry/webfrontend/legacy/fhem/scripts/ccfhem.py

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

Network.Ipv4.Ipaddress

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
	pfad_fhem="/opt/fhem/FHEM"
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

#ip="$(ip addr show eth0 | grep -vw "inet6" | grep "global" | grep -w "inet" | cut -d/ -f1 | awk '{ print $2 }')"

Network.Ipv4.Ipaddress

ip=$(jq -r '.Network.Ipv4.Ipaddress' "$LBSCONFIG/general.json")

echo	$ip
echo

echo	"Datei 99_myUtils.pm IP-Adresse Miniserver einstellen und verschieben"

cd
cd Scripts/lox2comfoconnectwithfhem
perl -npi -e 's/MS_IP/'"$IP_MS"'/g' 99_myUtils.pm
cp -i -r 99_myUtils.pm $pfad_fhem

echo
echo	"Telnet einstellen"

curl -q "http://$ip:8083/fhem?cmd=define%20telnetPort%20telnet%207072%20global"
curl -q "http://$ip:8083/fhem?cmd=attr%20telnetPort%20room%20Zentral"

echo
echo	"Comfoconnect erstellen"

curl -q "http://$ip:8083/fhem?cmd=define%20comfoconnect%20dummy"



echo
echo	"Symbol erstellen"

curl -q "http://$ip:8083/fhem?cmd=attr%20comfoconnect%20devStateIcon%20%7B%22%2E%2A%3Avent_ventilation_level_%22%2EReadingsVal(%22comfoconnect%22%2C%22Stufe%22%2C0)%2E(ReadingsVal(%22comfoconnect%22%2C%22Modus%22%2C0)%20ne%20%2D1%20%3F%20%27%40green%27%20%3A%20%22%22)%7D"

echo
echo	"Einstellungen vornehmen"

perl /opt/fhem/fhem.pl 7072 "attr comfoconnect userReadings ModusTXT {if(ReadingsVal("comfoconnect","Modus","") == -1) {return "Auto"} elsif (ReadingsVal("comfoconnect","Modus","") == 1) {return "Manuell' 'Zeit"} elsif (ReadingsVal("comfoconnect","Modus","") == 5) {return "Manuell"} elsif (ReadingsVal("comfoconnect","Modus","") == 6) {return "Partymodus"} elsif (ReadingsVal("comfoconnect","Modus","") == 7) {return "AbwesendAPP"} else {return "Fehler"}}, NextTime {hex(substr(ReadingsVal("comfoconnect","Next",0),4,2))*65280+hex(substr(ReadingsVal("comfoconnect","Next",0),2,2))*255+hex(substr(ReadingsVal("comfoconnect","Next",0),0,2))}, BypassZeit {hex(substr(ReadingsVal("comfoconnect","BypassZeitHEX",0),4,2))*65280+hex(substr(ReadingsVal("comfoconnect","BypassZeitHEX",0),2,2))*255+hex(substr(ReadingsVal("comfoconnect","BypassZeitHEX",0),0,2))}, AbluftZeit {hex(substr(ReadingsVal("comfoconnect","AbluftHEX",0),4,2))*65280+hex(substr(ReadingsVal("comfoconnect","AbluftZeitHEX",0),2,2))*255+hex(substr(ReadingsVal("comfoconnect","AbluftZeitHEX",0),0,2))}"

echo	"Abfrage Daten konfigurieren"

curl -q "http://$ip:8083/fhem?cmd=define%20Q350ToLoxone%20notify%20.*:DrehzahlAbluftventilator.*%20{Q350ToLoxone(%22%24NAME%22)}"

echo	
echo	"Autostart vom CCFHEM Skript konfigurieren"

curl -q "http://$ip:8083/fhem?cmd=define%20FHEMStart%20notify%20global:INITIALIZED.*%20%7Bsystem(%22python3%20/opt/loxberry/webfrontend/legacy/fhem/scripts/ccfhem.py%20--ip%20"$IP_Comfo"%20%26%22)%7D"

echo
echo	"Raum Zentral zuweisen"

curl -q "http://$ip:8083/fhem?cmd=attr%20comfoconnect%20room%20Zentral"
curl -q "http://$ip:8083/fhem?cmd=attr%20FHEMStart%20room%20Zentral"
curl -q "http://$ip:8083/fhem?cmd=attr%20Q350ToLoxone%20room%20Zentral"

echo
echo	"Einstellungen in FHEM speichern"
echo

perl /opt/fhem/fhem.pl 7072 "save"

echo	"-------------------------------------------"
echo	"	Installationsdateien werden gelöscht	"
echo	"-------------------------------------------"
echo

cd
rm -r Scripts/

echo	"-----------------------------------"
echo	"     Installation beendet!         "
echo	"          Viel Spaß!               "
echo	"     Copyright © 2020  hme0354     "
echo
echo	"     All rights reserved           "
echo	"-----------------------------------"