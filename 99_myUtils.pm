##############################################
# $Id: myUtilsTemplate.pm 7570 2015-01-14 18:31:44Z rudolfkoenig $
#
# Save this file as 99_myUtils.pm, and create your own functions in the new
# file. They are then available in every Perl expression.

package main;

use strict;
use warnings;
use POSIX;

sub
myUtils_Initialize($$)
{
  my ($hash) = @_;
}

# Enter you functions below _this_ line.

#UDP Befehle senden
sub UDP_Msg($$$)
{
my ($dest,$port,$cmd) = @_;
my $sock = IO::Socket::INET->new(
 Proto => 'udp',
 PeerPort => $port,
 PeerAddr => $dest
) or die "Could not create socket: $!\n";
$sock->send($cmd) or die "Send error: $!\n";
return "send $cmd";
}

#HarmonyActivityToLoxone
#1 currentActivity
#2 state

sub Q350ToLoxone($)
{
 my ($device) = @_;
my 
$Abluftfeuchte=ReadingsVal("$device","Abluftfeuchte","-1");
my 
$Ablufttemperatur=ReadingsVal("$device","Ablufttemperatur","-1");
my 
$Abluftventilatorvolumen=ReadingsVal("$device","Abluftventilatorvolumen","-1");
my 
$Aussenluftfeuchte=ReadingsVal("$device","Aussenluftfeuchte","-1");
my 
$Aussenlufttemperatur=ReadingsVal("$device","Aussenlufttemperatur","-1");
my 
$Bypass=ReadingsVal("$device","Bypass","-1");
my 
$Filterwechsel=ReadingsVal("$device","Filterwechsel","-1");
my 
$Fortluftfeuchte=ReadingsVal("$device","Fortluftfeuchte","-1");
my 
$Fortlufttemperatur=ReadingsVal("$device","Fortlufttemperatur","-1");
my 
$Leistung=ReadingsVal("$device","Leistung","-1");
my 
$ModusTXT=ReadingsVal("$device","Modus","-1");
my 
$Stufe=ReadingsVal("$device","Stufe","-1");
my 
$Zuluftfeuchte=ReadingsVal("$device","Zuluftfeuchte","-1");
 my 
$Zulufttemperatur=ReadingsVal("$device","Zulufttemperatur","-1");
 my 
$Zuluftventilatorvolumen=ReadingsVal("$device","Zuluftventilatorvolumen","-1");
 my 
$NextTime=ReadingsVal("$device","NextTime","-1");
 my 
$BYPASS_MODUS=ReadingsVal("$device","BYPASS_MODUS","-1");
 my 
$BypassZeit=ReadingsVal("$device","BypassZeit","-1");
 my 
$Temperaturprofil=ReadingsVal("$device","Temperaturprofil","-1");
 my 
$FrostschutzUnbalance=ReadingsVal("$device","FrostschutzUnbalance","-1");
 my 
$DrehzahlAbluftventilator=ReadingsVal("$device","DrehzahlAbluftventilator","-1");
 my 
$DrehzahlZuluftventilator=ReadingsVal("$device","DrehzahlZuluftventilator","-1");

UDP_Msg("MS_IP" , "7002" , "$device: $Abluftfeuchte $Ablufttemperatur $Abluftventilatorvolumen $Aussenluftfeuchte $Aussenlufttemperatur $Bypass $Filterwechsel $Fortluftfeuchte $Fortlufttemperatur $Leistung $ModusTXT $Stufe $Zuluftfeuchte $Zulufttemperatur $Zuluftventilatorvolumen $NextTime $BYPASS_MODUS $BypassZeit $Temperaturprofil $FrostschutzUnbalance $DrehzahlAbluftventilator $DrehzahlZuluftventilator");
}

1;
