#!/usr/bin/python3

### Version 0.0.1

import argparse
import socket
import ast

import sys
sys.stdout = None

from pycomfoconnect import *

#TODO check for version
#pip3 show pycomfoconnect | grep Version
#print(socket.__version__)

############# Argumentparsing and definition #################

pin = 0
local_name = 'FHEM'
local_uuid = bytes.fromhex('00000000000000000000000000000010')


parser = argparse.ArgumentParser()
parser.add_argument('--host', help='fhem server address. (localhost)')
parser.add_argument('--port', help='fhem telnet port. (7072)')
parser.add_argument('--servport', help='port to listen for commands. (7077)')
parser.add_argument('--ip', help='ip address of the comfocontrol bridge (auto)')
parser.add_argument('--fhemdummy', help='name of the fhem dummy (comfoconnect)')
args = parser.parse_args()

args.host = 'localhost' if args.host == None else args.host
args.port = 7072 if args.port == None else args.port

args.servport = 7077 if args.servport == None else args.servport
servhost = 'localhost'

args.fhemdummy = "comfoconnect" if args.fhemdummy == None else args.fhemdummy


conf = {
 16 : {
  'NAME' : 'ModusAbwesend',
  'TYPE' : 1
 },
 33 : {
  'NAME' : 'Test33',
  'TYPE' : 1
 },
 37 : {
  'NAME' : 'Test37',
  'TYPE' : 1
 },
 49 : {
  'NAME' : 'Modus',
  'TYPE' : 1
 },
 53 : {
  'NAME' : 'Test53',
  'TYPE' : 1
 },
 56 : {
  'NAME' : 'ModusAutoManuell',
  'TYPE' : 1
 },
 65 : {
  'NAME' : 'Stufe',
  'TYPE' : 1,
  'CONV' : 'str(%i)[-1:]'
 },
 66 : {
  'NAME' : 'ModusBypass',
  'TYPE' : 1
 },
 67 : {
  'NAME' : 'ModusTemperaturprofil',
  'TYPE' : 1
 },
 70 : {
  'NAME' : 'ModusNurZuluftventilator',
  'TYPE' : 1
 },
 71 : {
  'NAME' : 'ModusNurAbluftventilator',
  'TYPE' : 1
 },
 81 : {
  'NAME' : 'ZeitAllgemeinHex',
  'TYPE' : 3
 },
 82 : {
  'NAME' : 'ZeitBypassHex',
  'TYPE' : 3
 },
 85 : {
  'NAME' : 'Test85',
  'TYPE' : 3
 },
 86 : {
  'NAME' : 'ZeitZuluftHEX',
  'TYPE' : 3
 },
 87 : {
  'NAME' : 'ZeitAbluftHEX',
  'TYPE' : 3
 },
 117 : {
  'NAME' : 'AuslastungAbluft',
  'TYPE' : 1,
  'UNIT' : '%'
 },
 118 : {
  'NAME' : 'AuslastungZuluft',
  'TYPE' : 1,
  'UNIT' : '%'
 },
 119 : {
  'NAME' : 'VentilatorvolumenAbluft',
  'TYPE' : 2,
  'UNIT' : 'm³/h'
 },
 120 : {
  'NAME' : 'VentilatorvolumenZuluft',
  'TYPE' : 2,
  'UNIT' : 'm³/h'
 },
 121 : {
  'NAME' : 'DrehzahlAbluftventilator',
  'TYPE' : 2,
  'UNIT' : 'U/min'
 },
 122 : {
  'NAME' : 'DrehzahlZuluftventilator',
  'TYPE' : 2,
  'UNIT' : 'U/min'
 },
 128 : {
  'NAME' : 'LeistungLueftung',
  'TYPE' : 2,
  'UNIT' : 'W'
 },
 129 : {
  'NAME' : 'VerbrauchLueftungProJahr',
  'TYPE' : 2
 },
 130 : {
  'NAME' : 'VerbrauchLueftungGesamt',
  'TYPE' : 2
 },
 144 : {
  'NAME' : 'VerbrauchVorheizregisterProJahr',
  'TYPE' : 2,
  'UNIT' : 'W'
 },
 145 : {
  'NAME' : 'VerbrauchVorheizregisterGesamt',
  'TYPE' : 2,
  'UNIT' : 'kWh'
 },
 146 : {
  'NAME' : 'LeistungVorheizregisterIST',
  'TYPE' : 2,
  'UNIT' : 'kWh' 
 },
 176 : {
  'NAME' : 'SETTING RF PAIRING',
  'TYPE' : 1
 },
 192 : {
  'NAME' : 'ZeitFilterwechsel',
  'TYPE' : 2,
  'UNIT' : 'Tage'
 },
 208 : {
  'NAME' : 'EinstellungEinheitGUI',
  'TYPE' : 1
 },
 209 : {
  'NAME' : 'GrenztemeraturAktuell',
  'TYPE' : 6,
  'CONV' : "%i / 10",
  'UNIT' : '°C'
 },
 210 : {
  'NAME' : 'ModusHeizperiode',
  'TYPE' : 0
 },
 211 : {
  'NAME' : 'ModusKuehlperiode',
  'TYPE' : 0
 },
 212 : {
  'NAME' : 'TemperaturSollRegelung',
  'TYPE' : 6,
  'CONV' : "%i / 10",
  'UNIT' : '°C'
 },
 213 : {
  'NAME' : 'LeistunHeizstromVermieden',
  'TYPE' : 2,
  'UNIT' : 'W'
 },
 214 : {
  'NAME' : 'VerbrauchVermiedenerHeizstromJahr',
  'TYPE' : 2,
  'UNIT' : 'kWh'
 },
 215 : {
  'NAME' : 'VerbrauchVermiedenerHeizstromGesamt',
  'TYPE' : 2,
  'UNIT' : 'kWh'
 },
 219 : {
  'NAME' : 'LeistungVorheizregisterSOLL',
  'TYPE' : 2
 },
 221 : {
  'NAME' : 'TemperaturZuluftInnen',
  'TYPE' : 6,
  'CONV' : "%i / 10",
  'UNIT' : '°C'
 },
 224 : {
  'NAME' : 'Test224',
  'TYPE' : 1
 },
 225 : {
  'NAME' : 'ModusKomfortregelung',
  'TYPE' : 1
 },
 226 : {
  'NAME' : 'Test226',
  'TYPE' : 2
 },
 227 : {
  'NAME' : 'ZustandBypass',
  'TYPE' : 1,
  'UNIT' : '%'
 },
 228 : {
  'NAME' : 'ZustandFrostschutzAusgleich',
  'TYPE' : 1
 },
 274 : {
  'NAME' : 'TemperaturAbluftInnen',
  'TYPE' : 6,
  'CONV' : "%i / 10",
  'UNIT' : '°C'
 },
 275 : {
  'NAME' : 'TemperaturAbluftAussen',
  'TYPE' : 6,
  'CONV' : "%i / 10",
  'UNIT' : '°C'
 },
 276 : {
  'NAME' : 'TemperaturZuluftAußen',
  'TYPE' : 6,
  'CONV' : "%i / 10",
  'UNIT' : '°C'
 },
 277 : {
  'NAME' : 'TemperaturNachVorheizregister',
  'TYPE' : 6,
  'CONV' : "%i / 10",
  'UNIT' : '°C'
 },
 290 : {
  'NAME' : 'LuftfeuchteAbluftInnen',
  'TYPE' : 1,
  'UNIT' : '%'
 },
 291 : {
  'NAME' : 'LuftfeuchteAbluftAussen',
  'TYPE' : 1,
  'UNIT' : '%'
 },
 292 : {
  'NAME' : 'LuftfeuchteZuluftAussen',
  'TYPE' : 1,
  'UNIT' : '%'
 },
 293 : {
  'NAME' : 'LuftfeuchtNachVorheizregister',
  'TYPE' : 1,
  'UNIT' : '%'
 },
 294 : {
  'NAME' : 'LuftfeuchteZuluftInnen',
  'TYPE' : 1,
  'UNIT' : '%'
 },
 321 : {
  'NAME' : 'Test321',
  'TYPE' : 2
 },
 325 : {
  'NAME' : 'Test325',
  'TYPE' : 3
 },
 341 : {
  'NAME' : 'Test341',
  'TYPE' : 3
 },
 369 : {
  'NAME' : 'Test369',
  'TYPE' : 1
 },
 370 : {
  'NAME' : 'Test370',
  'TYPE' : 1
 },
 371 : {
  'NAME' : 'Test371',
  'TYPE' : 1
 },
 372 : {
  'NAME' : 'Test372',
  'TYPE' : 1
 },
 384 : {
  'NAME' : 'Test384',
  'TYPE' : 6
 },
 386 : {
  'NAME' : 'Test386',
  'TYPE' : 0
 },
 400 : {
  'NAME' : 'Test400',
  'TYPE' : 6
 },
 401 : {
  'NAME' : 'Test401',
  'TYPE' : 1
 },
 402 : {
  'NAME' : 'Test402',
  'TYPE' : 0
 },
 416 : {
  'NAME' : 'Test416',
  'TYPE' : 6
 },
 417 : {
  'NAME' : 'Test417',
  'TYPE' : 6
 },
 418 : {
  'NAME' : 'Test418',
  'TYPE' : 1
 },
 419 : {
  'NAME' : 'Test419',
  'TYPE' : 0
 }

}


############# Create incomming connections #################

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind((servhost, args.servport))
serv.listen(5)

print("Socket opened: %s listen to %s" % (servhost,args.servport))

def send(client, msg):
	msg+="\r\n"
	client.send(msg.encode('ascii'))


############# Create Outgoing FHEM connection ###################

print(args.host)
print(args.port)
fhem = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
fhem.connect((args.host, args.port))

def fhemsend(msg):
	## fhem send here for comfoconnect requests
	msg+="\r\n"
	fhem.send(msg.encode('ascii'))

def setreading(var, value):
	# setreading <devspec> <reading> <value>
	#cmd = "setreading " + args.fhemdummy + " " + var + " " + value
	#temp = eval(conf[var]['CONV'] % (val))
	#print("%s hat %s " % (conf[var]['CONST'], temp))
	if var in conf:
		if 'CONV' in conf[var]:
			value = eval(conf[var]['CONV'] % (value))
		var = conf[var]['NAME']
	cmd = "setreading %s %s %s" % (args.fhemdummy, str(var), str(value))
	#print(cmd)
	fhemsend(cmd)



############## Bridge discovery ###################################

def bridge_discovery():

    bridges = Bridge.discover(args.ip)
    if bridges:
        bridge = bridges[0]
    else:
        bridge = None

    # Method 3: Setup bridge manually
    # bridge = Bridge(args.ip, bytes.fromhex('0000000000251010800170b3d54264b4'))

    if bridge is None:
        print("No bridges found!")
        exit(1)

    print("Bridge found: %s (%s)" % (bridge.uuid.hex(), bridge.host))
    bridge.debug = True

    return bridge


################# Callback sensors ####################################

def callback_sensor(var, value):

    print("%s = %s" % (var, value))
    setreading(var, value)





def main():
    def request(req):
     if req.startswith("CMD_"):
      comfoconnect.cmd_rmi_request(eval(req))
     else:
      print("Unkown Command: " + req)
    # Discover the bridge
    bridge = bridge_discovery()

    ## Setup a Comfoconnect session  ###################################################################################

    comfoconnect = ComfoConnect(bridge, local_uuid, local_name, pin)
    comfoconnect.callback_sensor = callback_sensor

    try:
        # Connect to the bridge
        # comfoconnect.connect(False)  # Don't disconnect existing clients.
        comfoconnect.connect(True)  # Disconnect existing clients.

    except Exception as e:
        print('ERROR: %s' % e)
        exit(1)

    ## Register sensors ################################################################################################

    # comfoconnect.register_sensor(SENSOR_FAN_NEXT_CHANGE)  # General: Countdown until next fan speed change
    # comfoconnect.register_sensor(SENSOR_FAN_SPEED_MODE)  # Fans: Fan speed setting
    # comfoconnect.register_sensor(SENSOR_FAN_SUPPLY_DUTY)  # Fans: Supply fan duty
    # comfoconnect.register_sensor(SENSOR_FAN_EXHAUST_DUTY)  # Fans: Exhaust fan duty
    # comfoconnect.register_sensor(SENSOR_FAN_SUPPLY_FLOW)  # Fans: Supply fan flow
    # comfoconnect.register_sensor(SENSOR_FAN_EXHAUST_FLOW)  # Fans: Exhaust fan flow
    # comfoconnect.register_sensor(SENSOR_FAN_SUPPLY_SPEED)  # Fans: Supply fan speed
    # comfoconnect.register_sensor(SENSOR_FAN_EXHAUST_SPEED)  # Fans: Exhaust fan speed
    # comfoconnect.register_sensor(SENSOR_POWER_CURRENT)  # Power Consumption: Current Ventilation
    # comfoconnect.register_sensor(SENSOR_POWER_TOTAL_YEAR)  # Power Consumption: Total year-to-date
    # comfoconnect.register_sensor(SENSOR_POWER_TOTAL)  # Power Consumption: Total from start
    # comfoconnect.register_sensor(SENSOR_DAYS_TO_REPLACE_FILTER)  # Days left before filters must be replaced
    # comfoconnect.register_sensor(SENSOR_AVOIDED_HEATING_CURRENT)  # Avoided Heating: Avoided actual
    # comfoconnect.register_sensor(SENSOR_AVOIDED_HEATING_TOTAL_YEAR)  # Avoided Heating: Avoided year-to-date
    # comfoconnect.register_sensor(SENSOR_AVOIDED_HEATING_TOTAL)  # Avoided Heating: Avoided total
    # comfoconnect.register_sensor(SENSOR_TEMPERATURE_SUPPLY)  # Temperature & Humidity: Supply Air (temperature)
    # comfoconnect.register_sensor(SENSOR_TEMPERATURE_EXTRACT)  # Temperature & Humidity: Extract Air (temperature)
    # comfoconnect.register_sensor(SENSOR_TEMPERATURE_EXHAUST)  # Temperature & Humidity: Exhaust Air (temperature)
    # comfoconnect.register_sensor(SENSOR_TEMPERATURE_OUTDOOR)  # Temperature & Humidity: Outdoor Air (temperature)
    # comfoconnect.register_sensor(SENSOR_HUMIDITY_SUPPLY)  # Temperature & Humidity: Supply Air (temperature)
    # comfoconnect.register_sensor(SENSOR_HUMIDITY_EXTRACT)  # Temperature & Humidity: Extract Air (temperature)
    # comfoconnect.register_sensor(SENSOR_HUMIDITY_EXHAUST)  # Temperature & Humidity: Exhaust Air (temperature)
    # comfoconnect.register_sensor(SENSOR_HUMIDITY_OUTDOOR)  # Temperature & Humidity: Outdoor Air (temperature)
    # comfoconnect.register_sensor(SENSOR_BYPASS_STATE)  # Bypass state
    for regno in conf.keys():
       comfoconnect.register_sensor(regno)

    ## Execute functions ###############################################################################################

    # ListRegisteredApps
    devices=''
    for app in comfoconnect.cmd_list_registered_apps():
        # print('%s: %s' % (app['uuid'].hex(), app['devicename']))
        devices+=app['devicename']+" "
    setreading('registeredDevices', devices)


    # DeregisterApp
    # comfoconnect.cmd_deregister_app(bytes.fromhex('00000000000000000000000000000001'))

    # VersionRequest
    version = comfoconnect.cmd_version_request()
    for key in version:
      setreading(key, version[key])
    # TimeRequest
    #timeinfo = comfoconnect.cmd_time_request()
    #print(timeinfo)

    ## Executing functions #############################################################################################

#     comfoconnect.cmd_rmi_request(CMD_FAN_MODE_AWAY)  # Go to away mode
#     comfoconnect.cmd_rmi_request(CMD_FAN_MODE_LOW)  # Set fan speed to 1
#     comfoconnect.cmd_rmi_request(CMD_FAN_MODE_MEDIUM)  # Set fan speed to 2
#     comfoconnect.cmd_rmi_request(CMD_FAN_MODE_HIGH)  # Set fan speed to 3

    ## Example interaction #############################################################################################

    try:
        print('Waiting... Stop with CTRL+C')
        while True:
            # Callback messages will arrive in the callback method.
            clien,addr = serv.accept()
            print("Got a connection from %s" % str(addr))
            send(clien, "Connection accepted")
            msg=clien.recv(1024)
            # commandhandler here
            strdec=str(msg.decode('ascii'))
            print ('Message received: ' + strdec)
            request(strdec)
            clien.close()

            if not comfoconnect.is_connected():
                print('We are not connected anymore...')




    except KeyboardInterrupt:
        pass

    ## Closing the session #############################################################################################

    fhem.close()
    comfoconnect.disconnect()


if __name__ == "__main__":
    main()
