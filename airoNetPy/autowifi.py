import json
import yaml
import netmiko
from netmiko import ConnectHandler

# read json file containing aironet settings
with open('autoAP-temp.json', 'r') as file:
    deviceData = json.load(file)

# read yaml file
# with open('autoAP-temp.yml', 'r') as file:
#     deviceData = yaml.safe_load(file)
    
# parse info from json file
aironet = deviceData['aironetInfo']
apConfig = deviceData['aironetConfig']

deviceConfig = [
    f'hostname {apConfig["hostname"]}',
    f'dot11 ssid {apConfig["ssid"]}',
    f'vlan {apConfig["vlan"]}',
    f'authentication {apConfig["authentication"]}',
    f'authentication key-management {apConfig["key-man"]}',
    f'wpa-psk ascii {apConfig["wifi-pass"]}',
    'guest-mode',
    'default Int Dot11Radio 0',
    'default interface gigabitEthernet 0',
    'int dot11radio 0',
    'no shut',
    f'channel {apConfig["channel"]}',
    f'encryption mode ciphers {apConfig["encr-mod"]}',
    f'encryption vlan {apConfig["vlan"]} mode ciphers {apConfig["encr-mod"]}',
    f'ssid {apConfig["ssid"]}',
    'exit',
    f'interface dot11radio 0.{apConfig["vlan"]}',
    f'encapsulation dot1q {apConfig["vlan"]} native',
    'bridge-group 1',
    'exit'
]

# connect to the device
accessAutoAP = ConnectHandler(**aironet)

# use enable command to enter privilege exec mode
accessAutoAP.enable()

# push configurations through global configuration mode
output = accessAutoAP.send_config_set(deviceConfig)
print('Configuration Successfull!')
print(output)

# create a show run output file
with open('show_run_output.txt', 'w') as file:
    file.write(output)


# close connection
accessAutoAP.disconnect()
