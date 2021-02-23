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

sub Q350ToLoxone($)
{
 my ($device) = @_;
my 
$LeistungLueftung=ReadingsVal("$device","LeistungLueftung","-1");
my 
$LeistungVorheizregisterIST=ReadingsVal("$device","LeistungVorheizregisterIST","-1");
my 
$LuftfeuchteAbluftAussen=ReadingsVal("$device","LuftfeuchteAbluftAussen","-1");
my 
$LuftfeuchteAbluftInnen=ReadingsVal("$device","LuftfeuchteAbluftInnen","-1");
my 
$LuftfeuchteZuluftAussen=ReadingsVal("$device","LuftfeuchteZuluftAussen","-1");
my 
$LuftfeuchteZuluftInnen=ReadingsVal("$device","LuftfeuchteZuluftInnen","-1");
my 
$LuftfeuchtNachVorheizregister=ReadingsVal("$device","LuftfeuchtNachVorheizregister","-1");
my 
$Modus=ReadingsVal("$device","Modus","-1");
my 
$ModusBypass=ReadingsVal("$device","ModusBypass","-1");
my 
$ModusKomfortregelung=ReadingsVal("$device","ModusKomfortregelung","-1");
my 
$ModusTemperaturprofil=ReadingsVal("$device","ModusTemperaturprofil","-1");
my 
$Stufe=ReadingsVal("$device","Stufe","-1");
my 
$TemperaturAbluftAussen=ReadingsVal("$device","TemperaturAbluftAussen","-1");
 my 
$TemperaturAbluftInnen=ReadingsVal("$device","TemperaturAbluftInnen","-1");
 my 
$TemperaturNachVorheizregister=ReadingsVal("$device","TemperaturNachVorheizregister","-1");
 my 
$TemperaturZuluftAußen=ReadingsVal("$device","TemperaturZuluftAußen","-1");
 my 
$TemperaturZuluftInnen=ReadingsVal("$device","TemperaturZuluftInnen","-1");
 my 
$VentilatorvolumenAbluft=ReadingsVal("$device","VentilatorvolumenAbluft","-1");
 my 
$VentilatorvolumenZuluft=ReadingsVal("$device","VentilatorvolumenZuluft","-1");
 my 
$VerbrauchLueftungGesamt=ReadingsVal("$device","VerbrauchLueftungGesamt","-1");
 my 
$VerbrauchVorheizregisterGesamt=ReadingsVal("$device","VerbrauchVorheizregisterGesamt","-1");
 my 
$ZeitAllgemein=ReadingsVal("$device","ZeitAllgemein","-1");
 my 
$ZeitBypass=ReadingsVal("$device","ZeitBypass","-1");
 my 
$ZeitFilterwechsel=ReadingsVal("$device","ZeitFilterwechsel","-1");
 my 
$ZustandBypass=ReadingsVal("$device","ZustandBypass","-1");
 my 
$ZustandFrostschutzAusgleich=ReadingsVal("$device","ZustandFrostschutzAusgleich","-1");

UDP_Msg("MS_IP" , "7002" , "$device: $LeistungLueftung $LeistungVorheizregisterIST $LuftfeuchteAbluftAussen $LuftfeuchteAbluftInnen $LuftfeuchteZuluftAussen $LuftfeuchteZuluftInnen $LuftfeuchtNachVorheizregister $Modus $ModusBypass $ModusKomfortregelung $ModusTemperaturprofil $Stufe $TemperaturAbluftAussen $TemperaturAbluftInnen $TemperaturNachVorheizregister $TemperaturZuluftAußen $TemperaturZuluftInnen $VentilatorvolumenAbluft $VentilatorvolumenZuluft $VerbrauchLueftungGesamt $VerbrauchVorheizregisterGesamt $ZeitAllgemein $ZeitBypass $ZeitFilterwechsel $ZustandBypass $ZustandFrostschutzAusgleich");
}

1;
