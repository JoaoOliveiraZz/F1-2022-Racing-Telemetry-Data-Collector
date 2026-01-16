import socket
import struct

UDP_IP = "0.0.0.0"
UDP_PORT = 20777

# Formato do cabeçalho
HEADER_FORMAT = '<HBBBBBQfIIBB'
HEADER_SIZE = 29 # Size em Bytes


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"📡 Ouvindo telemetria em {UDP_IP}:{UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(2048)


    if len(data) < HEADER_SIZE:
        continue

    # Desempacota cabeçalho
    header = struct.unpack(HEADER_FORMAT, data[:HEADER_SIZE])
    packet_id = header[5]
    player_car_index = header[-2]

    print(header, packet_id, player_car_index)
