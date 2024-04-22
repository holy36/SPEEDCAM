import bluetooth
from bluetooth import Protocols

def search_devices():
    print("Đang tìm kiếm các thiết bị Bluetooth xung quanh...")
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True)
    print("Các thiết bị Bluetooth xung quanh:")
    for addr, name in nearby_devices:
        # Create a Bluetooth socket and connect to the target device
        print(f"{addr} - {name}")   

def connect_to_device(device_address):
    port = 1  # RFCOMM port number
    try:
        print(f"Đang kết nối đến thiết bị có địa chỉ {device_address}...")
        sock = bluetooth.BluetoothSocket(Protocols.RFCOMM)
        sock.connect((device_address, port))
        print("Đã kết nối thành công!")
        return sock
    except Exception as e:
        print(e)
        return None
# D8:3A:DD:BF:33:D1 - raspberrypi 
def main():
    search_devices()
    device_address = input("Nhập địa chỉ của thiết bị bạn muốn kết nối: ")
    sock = connect_to_device(device_address)
    if sock:
        # Thực hiện các hoạt động sau khi kết nối thành công
        pass

if __name__ == "__main__":
    main()
