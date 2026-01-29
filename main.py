import socket
import struct
import pandas as pd
from excel.importDataToExcel import append_to_excel
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "excel", "telemetryData.xlsx")

UDP_IP = "0.0.0.0"
UDP_PORT = 20777

# Formato do cabeçalho
HEADER_FORMAT = '<HBBBBBQfIIBB'
HEADER_SIZE = 29 # Size em Bytes

CAR_TELEMETRY_FORMAT = '<HfffBbHBBH4H4B4BH4f4B'

CAR_SIZE = struct.calcsize(CAR_TELEMETRY_FORMAT)



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"📡 Ouvindo telemetria em {UDP_IP}:{UDP_PORT}...")

def unpack_package_header(data, offset = 0):

    if len(data) < HEADER_SIZE:
        exit(0)
    
    # Desempacota cabeçalho
    header = struct.unpack(HEADER_FORMAT, data[:HEADER_SIZE])


    size = struct.calcsize(HEADER_FORMAT)

    return {
        "package_format": header[0],
        "gameYear": header[1],
        "gameMajorVersion": header[2],
        "gameMinorVersion": header[3],
        "packageVersion": header[4],
        "packageId": header[5],
        "sessionUID": header[6],
        "sessionTime": header[7],
        "frameIdentifier": header[8],
        "overallFrameIdentifier": header[9],
        "playerCarIndex": header[10],
        "secondaryPlayerCarIndex": header[11]
    }, offset + size


def unpack_car_telemetry(data, offset):
    
    size = struct.calcsize(CAR_TELEMETRY_FORMAT)
    values = struct.unpack_from(CAR_TELEMETRY_FORMAT, data, offset)

    return {
        "speed": values[0],
        "throttle": values[1],
        "steer": values[2],
        "brake": values[3],
        "clutch": values[4],
        "gear": values[5],
        "engineRPM": values[6],
        "drs": values[7],
        "revLightsPercent": values[8],
        "revLightsBitValue": values[9],
        "brakesTemperature": values[10:14],
        "tyresSurfaceTemperature": values[14:18],
        "tyresInnerTemperature": values[18:22],
        "engineTemperature": values[22],
        "tyresPressure": values[23:27],
        "surfaceType": values[27:31],
    }, offset + size


rows = []

while True:
    data, addr = sock.recvfrom(2048)

    header, offset = unpack_package_header(data, 0)

    if header["packageId"] == 6:

        player_car_index = header["playerCarIndex"]

        player_offset = HEADER_SIZE + (player_car_index * CAR_SIZE)

        player_car, _ = unpack_car_telemetry(data, player_offset)

        player_car_data = {
            "speed": player_car['speed'],
            "throttle": player_car['throttle'],
            "steer": player_car['steer'],
            "brake": player_car['brake'],
            "gear": player_car['gear'],
            "drs": player_car['drs'],
            "breakTemperatureFL": player_car['brakesTemperature'][0],
            "breakTemperatureFR": player_car['brakesTemperature'][1],
            "breakTemperatureRL": player_car['brakesTemperature'][2],
            "breakTemperatureRR": player_car['brakesTemperature'][3]
        }

        rows.append(player_car_data)

        if len(rows) > 200:
            df = pd.DataFrame(rows)
            append_to_excel(df)
            print("DATA SAVE")
            rows.clear()




    
