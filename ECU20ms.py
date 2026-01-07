import can
import time

try:
    bus = can.interface.Bus('vcan0', interface='socketcan')
except Exception as e:
    print(f"Error connecting to bus: {e}")
    exit()

# ID 0x188: Periodic message for Turn Signals
# Baseline [0x00, 0x00, 0x00, 0x00] keeps blinkers OFF
msg = can.Message(arbitration_id=0x188, data=[0x00, 0x00, 0x00, 0x00], is_extended_id=False)

print("Baseline: Sending periodic messages (ID 0x188) every 20ms...")

try:
    while True:
        bus.send(msg)
        time.sleep(0.02) 
except KeyboardInterrupt:
    print("\nLegitimate ECU simulation stopped.")