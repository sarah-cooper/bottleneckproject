#!/bin/sh
python2 test_commands.py 0;

# stress-ng --vm-bytes $(awk '/MemAvailable/{printf "%d\n", $2 * 0.98;}' < /proc/meminfo)k --vm-keep -m 10 & ;
# sleep 10;
# python2 test_commands.py 1;
#  killall stress-ng;
# sleep 10;

stress -d 16 &
sleep 10;
python2 test_commands.py 2;
killall stress;
sleep 10;

stress -i 1000 &
sleep 10;
python2 test_commands.py 3;
killall stress;
sleep 10;

stress -c 16 &
sleep 10;
python2 test_commands.py 4;
killall stress;
sleep 10;

#packet loss

tc qdisc add dev ens3f0 root netem loss .1%;
sleep 10;
python2 test_commands.py 5;
tc qdisc del dev ens3f0 root;

tc qdisc add dev ens3f0 root netem loss .05%;
sleep 10;
python2 test_commands.py 6;
 tc qdisc del dev ens3f0 root;

tc qdisc add dev ens3f0 root netem loss 1%;
sleep 10;
python2 test_commands.py 7;
tc qdisc del dev ens3f0 root;

#packet delay
tc qdisc add dev ens3f0 root netem delay 5ms 1ms distribution normal;
sleep 10;
python2 test_commands.py 8;
tc qdisc del dev ens3f0 root;

 tc qdisc add dev ens3f0 root netem delay 10ms 2ms distribution normal;
sleep 10;
python2 test_commands.py 9;
 tc qdisc del dev ens3f0 root;

tc qdisc add dev ens3f0 root netem delay 15ms 10ms distribution normal;
sleep 10;
python2 test_commands.py 10;
tc qdisc del dev ens3f0 root;

#packet duplicate

tc qdisc add dev ens3f0 root netem duplicate .1%;
sleep 10;
python2 test_commands.py 11;
tc qdisc del dev ens3f0 root;

tc qdisc add dev ens3f0 root netem duplicate .05%;
sleep 10;
python2 test_commands.py 12;
tc qdisc del dev ens3f0 root;

tc qdisc add dev ens3f0 root netem duplicate 1%;
sleep 10;
python2 test_commands.py 13;
tc qdisc del dev ens3f0 root;

#packet corrupt

tc qdisc add dev ens3f0 root netem corrupt 0.1%;
sleep 10;
python2 test_commands.py 14;
tc qdisc del dev ens3f0 root;

tc qdisc add dev ens3f0 root netem corrupt .05%;
sleep 10;
python2 test_commands.py 15;
tc qdisc del dev ens3f0 root;

tc qdisc add dev ens3f0 root netem corrupt 1.0%;
sleep 10;
python2 test_commands.py 16;
tc qdisc del dev ens3f0 root;

#packet reordering

tc qdisc add dev ens3f0 root netem reorder 0.1%;
sleep 10;
python2 test_commands.py 17;
tc qdisc del dev ens3f0 root;

tc qdisc add dev ens3f0 root netem reorder .05%;
sleep 10;
python2 test_commands.py 18;
tc qdisc del dev ens3f0 root;

tc qdisc add dev ens3f0 root netem reorder 1.0%;
sleep 10;
python2 test_commands.py 19;
tc qdisc del dev ens3f0 root;

#bandwith limit
tc qdisc add dev ens3f0 root tbf rate 10MBit burst 32Mbit limit 30000;
sleep 10;
python2 test_commands.py 20;
tc qdisc del dev ens3f0 root;

tc qdisc add dev ens3f0 root tbf rate 5MBit burst 32Mbit limit 30000;
sleep 10;
python2 test_commands.py 21;
tc qdisc del dev ens3f0 root;

tc qdisc add dev ens3f0 root tbf rate 1MBit burst 32Mbit limit 30000;
sleep 10;
python2 test_commands.py 22;
tc qdisc del dev ens3f0 root;