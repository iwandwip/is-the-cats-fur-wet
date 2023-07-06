import serial
from utility.data import YAMLDataHandler
from datetime import datetime
from modules.utils import Ticks

if __name__ == "__main__":
    try:
        print(f"[INFO] Serial Communication Initialize")
        coms = serial.Serial('COM6', 9600, timeout=1)  # serial config
        coms.reset_input_buffer()
        print(f"[INFO] Serial Communication Success")
        data = YAMLDataHandler("out/cats-output-data.yaml")
        nano_data = []
        write_time = 0
        while True:
            try:
                if Ticks() - write_time >= 1000:
                    condition = 1 if data.read()['condition'] else 0
                    writeData = f"{condition};{(data.read()['dc-fan-a'])};{data.read()['dc-fan-b']};{data.read()['dc-fan-c']};{data.read()['dc-fan-d']}\n"
                    # print(f"[INFO] Write Data {writeData}")
                    coms.write(writeData.encode('utf-8'))
                    coms.flush()
                    write_time = Ticks()
                if coms.in_waiting > 0:
                    bufferData = coms.readline().decode('utf-8', 'ignore').strip().split()
                    bufferData = [value.replace('C', '') for value in bufferData]
                    nano_data = bufferData if len(bufferData) == 7 else nano_data
                    print(f"[INFO] Len: {len(bufferData)} | Act: {nano_data}")
                    if len(nano_data):
                        data.update("temperature", nano_data[0])
                        data.update("humidity", nano_data[1])
                    coms.reset_input_buffer()
            except (TypeError, Exception) as e:
                pass
    except (RuntimeError, Exception) as e:
        print(f"[ERROR] {datetime.timestamp(datetime.now())} Serial Initialize Failed: \n{e}")
