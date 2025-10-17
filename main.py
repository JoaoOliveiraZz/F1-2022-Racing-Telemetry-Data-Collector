import socket
import struct

UDP_IP = "0.0.0.0"
UDP_PORT = 20777

# Cada carro tem 64 bytes no pacote de telemetria
CAR_SIZE = 64
NUM_CARS = 22

# Formato do cabeçalho
HEADER_FORMAT = '<HBBBBQfIBB'  # 24 bytes
HEADER_SIZE = 24

# Formato de um carro
CAR_FORMAT = '<HfffBbHBBHHBBHfB'  # 64 bytes

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"📡 Ouvindo telemetria em {UDP_IP}:{UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(2048)

    # Verifica se tem pelo menos o cabeçalho
    if len(data) < HEADER_SIZE:
        continue

    # Desempacota cabeçalho
    header = struct.unpack(HEADER_FORMAT, data[:HEADER_SIZE])
    packet_id = header[4]
    player_car_index = header[8]

    # Processa apenas pacote de telemetria (packetId = 6)
    if packet_id == 6:
        car_data_start = 24
        car_data_size = 60  # bytes por carro (aprox)
        player_car_index = header[8]

        start = car_data_start + (player_car_index * car_data_size)
        car_data = data[start:start + car_data_size]

        # velocidade (unsigned short), RPM (unsigned short), marcha (unsigned byte)
        car_information = struct.unpack_from(CAR_FORMAT, car_data, offset=0)

        speed = car_information[0]
        throttle = car_information[1] * 100
        brake = car_information[3] * 100
        gear = car_information[5]

        print(f"Speed: {speed}, throttle: {float.__floor__(throttle)}, brake: {float.__floor__(brake)}, gear: {gear}")