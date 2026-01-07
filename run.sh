#!/bin/bash

INTERFACE="vcan0"
LEGIT_SCRIPT="ECU20ms.py"
BASELINE_DURATION=30
ATTACK_DURATION=20
POST_ATTACK_DURATION=20

DUMPS_DIR="./Dumps"
CIDS_DIR="./CIDS"
mkdir -p $DUMPS_DIR
mkdir -p $CIDS_DIR

echo "--- CPS Project: Automated Orchestrator ---"
echo "Select the type of attack to perform:"
echo "1) Fabrication"
echo "2) Suspension"
echo "3) Masquerade"
read -p "Enter the number (1-3): " ATK_CHOICE
case $ATK_CHOICE in
  1) 
    ATK_NAME="fabrication"
    ATK_SCRIPT="attack_fabrication.py" 
    ;;
  2) 
    ATK_NAME="suspension"
    ATK_SCRIPT="attack_suspension.py" 
    ;;
  3) 
    ATK_NAME="masquerade"
    ATK_SCRIPT="attack_masquerade.py" 
    ;;
  *) echo "Invalid choice. Exiting."; exit 1 ;;
esac

DUMP_FILENAME="dump_${ATK_NAME}_attack.log"

echo "[+] Configuring interface $INTERFACE..."
sudo modprobe vcan
sudo ip link add dev $INTERFACE type vcan 2>/dev/null
sudo ip link set up $INTERFACE

# --- STARTING PROCESSES ---
./icsim $INTERFACE > /dev/null 2>&1 &
PID_ICS=$!
./controls $INTERFACE > /dev/null 2>&1 &
PID_CTRL=$!


echo "[+] Starting Logger..."
candump -l $INTERFACE > /dev/null 2>&1 &
PID_LOG=$!

sleep 2

echo "[+] Starting Legitimate ECU (ID 0x188)..."
python3 $LEGIT_SCRIPT > /dev/null 2>&1 &
PID_ECU=$!

echo "[+] PHASE 1: Baseline ($BASELINE_DURATION sec)..."
sleep $BASELINE_DURATION

echo "[+] PHASE 2: LAUNCHING ATTACK ($ATK_NAME) for $ATTACK_DURATION sec..."
python3 $ATK_SCRIPT > /dev/null 2>&1 &
PID_ATK=$!
sleep $ATTACK_DURATION

echo "[+] PHASE 3: Recovery ($POST_ATTACK_DURATION sec)..."
kill $PID_ATK
sleep $POST_ATTACK_DURATION

echo "[+] Experiment completed. Cleaning up processes..."
kill $PID_ICS $PID_CTRL $PID_LOG $PID_ECU

LATEST_LOG=$(ls -t candump-*.log | head -1)
mv "$LATEST_LOG" "$DUMPS_DIR/$DUMP_FILENAME"
echo "[+] Log saved in: $DUMPS_DIR/$DUMP_FILENAME"

echo "[+] Starting CIDS analysis..."
python3 plot_cids.py "$DUMPS_DIR/$DUMP_FILENAME" "$ATK_NAME"

echo "[+] Process completed. Plot saved in $CIDS_DIR/cids_${ATK_NAME}.png"