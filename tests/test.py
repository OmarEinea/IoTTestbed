from threading import Thread
from time import time, sleep
import socket, sys

PORT = 10000
MAGIC = b'\x68\x64'
CONTROL = b'\x00\x17\x64\x63'
SUBSCRIBE = b'\x00\x1e\x63\x6c'
DISCOVERY = b'\x00\x06\x71\x61'
DISCOVERY_RESP = b'\x00\x2a\x71\x61'
PADDING_1 = b'\x20\x20\x20\x20\x20\x20'
PADDING_2 = b'\x00\x00\x00\x00'
OFF = b'\x00'
ON = b'\x01'


def receive_packets():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_socket.bind(('', PORT))
    print("Started listening to all packets sent in the network")
    while True:
        packet, ip = receiver_socket.recvfrom(1024)
        packets[ip[0]] = packet


def get_ip_and_mac():
    print("Searching for a Wi-Fi socket...")
    while True:
        udp_socket.sendto(MAGIC + DISCOVERY, (local_ip, PORT))
        end = time() + 1
        while time() < end:
            for ip, packet in packets.copy().items():
                if packet[0:6] == MAGIC + DISCOVERY_RESP:
                    return ip, packet[7:13]


def send_packets(command):
    for _ in range(50):
        udp_socket.sendto(command, (s20_ip, PORT))


def subscribe():
    print("Trying to subscribe to the socket...")
    send_packets(MAGIC + SUBSCRIBE + s20_mac + PADDING_1 + s20_rev_mac + PADDING_1)
    sleep(1)


def switch(state):
    send_packets(MAGIC + CONTROL + s20_mac + PADDING_1 + PADDING_2 + state)


# Declare local ip, a UDP socket and an empty dictionary for packets
local_ip = socket.gethostbyname_ex(socket.gethostname())[-1][-1].rsplit('.', 1)[0] + ".255"
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
packets = {}
print("Initialized UDP socket on local IP:", local_ip)

# Start a thread to listen to packets sent by s20 socket
thread = Thread(target=receive_packets)
thread.daemon = True
thread.start()

# Get s20 socket ip and mac address
s20_ip, s20_mac = get_ip_and_mac()
print("Found Wiwo s20 Wi-Fi smart socket on IP:", s20_ip)

# Reverse s20's mac and store it
s20_rev_mac = bytearray(s20_mac)
s20_rev_mac.reverse()
s20_rev_mac = bytes(s20_rev_mac)

# Subscribe to s20 socket
subscribe()
print("Successfully subscribed to the socket")

# Get toggle (ON/OFF) from command line (default is OFF)
toggle = sys.argv[1] if len(sys.argv) > 1 else 'off'

# Switch s20 socket ON/OFF
print("Switching the socket", toggle)
switch(locals()[toggle.upper()])
print("Done. The socket is switched", toggle)