import serial
from utility.data import YAMLDataHandler
from datetime import datetime

if __name__ == "__main__":
    try:
        print(f"[INFO] Serial Communication Initialize")
        coms = serial.Serial('COM6', 9600, timeout=1)  # serial config
        coms.reset_input_buffer()
        data = YAMLDataHandler("out/cats-output-data.yaml")
        nanoData = []
        while True:
            try:
                condition = 1 if data.read()['condition'] else 0
                writeData = f"{condition};{data.read()['dc-fan-a']};{data.read()['dc-fan-b']};{data.read()['dc-fan-c']}\n"
                coms.write(writeData.encode('utf-8'))
                coms.flush()
                if coms.in_waiting > 0:
                    bufferData = coms.readline().decode('utf-8', 'ignore').strip().split()
                    bufferData = [value.replace('C', '') for value in bufferData]
                    nanoData = bufferData if len(bufferData) == 3 else nanoData
                    if len(nanoData):
                        data.update("temperature", nanoData[0])
                        data.update("humidity", nanoData[1])
                    coms.reset_input_buffer()
            except (TypeError, Exception) as e:
                pass
    except (RuntimeError, Exception) as e:
        print(f"[ERROR] {datetime.timestamp(datetime.now())} Serial Initialize Failed: \n{e}")
