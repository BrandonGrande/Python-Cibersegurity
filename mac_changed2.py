from locale import currency
import subprocess
import optparse
import re 

def get_arguments():
    
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",dest = "interface", help="Interface para cambiar direccion MAC")
    parser.add_option("-m","--mac",dest = "new_mac", help="Nueva direccion MAC")
    (options,arguments) = parser.parse_args()
    if not options.interface:
        parser.error("- Por favor indicar una interfaz, usa --help para mas informacion") 
    elif not options.new_mac: 
        parser.error("- Por favor indicar una direccion MAC, usa --help para mas informacion")
    return (options,arguments) 


def change_mac(interface, new_mac):
    print("[+] Cambiando direccion MAC para " + interface + " a " + new_mac)
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
    subprocess.call(["ifconfig",interface,"up"])

def get_current_mac(interface):
    ifconfig_results=subprocess.check_output(["ifconfig",interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(ifconfig_results))
    if mac_address_search_result: 
        return mac_address_search_result.group(0)
    else:
        print("- No se pudo leer la direccion MAC")
    
(options,arguments) = get_arguments()

current_mac = get_current_mac(options.interface)
print("Curret MAC" + str(current_mac)) 
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface) 
if current_mac == options.new_mac:
    print('[+] Direccion MAC cambio correctamente a '+ current_mac)
else: 
    print('[+] Direccion MAC no fue cambiado')  




