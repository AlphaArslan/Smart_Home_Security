sleep 180
cd /home/pi/project
cd webpage/
sudo pyhton3 webStream.py &
sleep 10
cd ..
sudo pyhton3 -r 192.168.0.4 -p 1080 -e encoding.pickle &
