echo "wait for 1 minute"
sleep 60
cd /home/pi/project
sudo modprobe bcm2835-v4l2
echo "starting video stream"
sudo python3 udpStream.py wlan0 > udpStream_log.txt &
sleep 20
echo "starting plate recognition"
sudo python3 Plate.py > Plate_log.txt &
sleep 10
echo "starting handler"
sudo python3 command_handler.py > command_handler_log.txt &
