import serial
from utility.data import YAMLDataHandler

if __name__ == "__main__":
    coms = serial.Serial('COM6', 9600, timeout=1)  # serial config
    coms.reset_input_buffer()
    data = YAMLDataHandler("out/output.yaml")
    nanoData = []
    print("[INFO] Serial Communication Initialize")
    try:
        while True:
            try:
                condition = data.read()['condition']
                coms.write(b"1\n" if condition else b"0\n")
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
    except RuntimeError as e:
        pass
