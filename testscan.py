import bluetooth

def search_devices():
    print("Đang tìm kiếm các thiết bị Bluetooth xung quanh...")
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True)
    print("Các thiết bị Bluetooth xung quanh:")
    for addr, name in nearby_devices:
        # Create a Bluetooth socket and connect to the target device
        print(f"{addr} - {name}")   


# D8:3A:DD:BF:33:D1 - raspberrypi 
def main():
    search_devices()
if __name__ == "__main__":
    main()
