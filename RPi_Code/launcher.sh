sleep 180
cd /home/pi/project
sudo python3 udpStream.py &
sleep 20
sudo python3 Plate.py > plate_log.txt &
sleep 10
sudo python3 command_handler.py &
