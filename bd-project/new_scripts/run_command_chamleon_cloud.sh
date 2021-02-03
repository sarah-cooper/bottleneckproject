#!/bin/sh
python2 main_program.py 0;

stress-ng --vm-bytes $(awk '/MemAvailable/{printf "%d\n", $2 * 0.98;}' < /proc/meminfo)k --vm-keep -m 10 &
sleep 10;
python2 main_program.py 1;
killall stress-ng;
sleep 10;

stress -d 16 &
sleep 10;
python2 main_program.py 2;
killall stress;
sleep 10;

stress -i 1000 &
sleep 10;
python2 main_program.py 3;
killall stress;
sleep 10;

stress -c 40 &
sleep 10;
python2 main_program.py 4;
killall stress;
sleep 10;

#packet loss

tc qdisc add dev eno1 root netem loss 0.001%;
sleep 10;
python2 main_program.py 5;
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem loss 0.005%;
sleep 10;
python2 main_program.py 6;
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem loss 0.01%;
sleep 10;
python2 main_program.py 7;
tc qdisc del dev eno1 root;

#packet delay
tc qdisc add dev eno1 root netem delay 1ms 1ms distribution normal;
sleep 10;
python2 main_program.py 8;
tc qdisc del dev eno1 root;

 tc qdisc add dev eno1 root netem delay 2ms 1ms distribution normal;
sleep 10;
python2 main_program.py 9;
 tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem delay 3ms 1ms distribution normal;
sleep 10;
python2 main_program.py 10;
tc qdisc del dev eno1 root;

#packet duplicate

tc qdisc add dev eno1 root netem duplicate 0.001%;
sleep 10;
python2 main_program.py 11;
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem duplicate 0.005%;
sleep 10;
python2 main_program.py 12;
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem duplicate 0.01%;
sleep 10;
python2 main_program.py 13;
tc qdisc del dev eno1 root;

#packet corrupt

tc qdisc add dev eno1 root netem corrupt 0.001%;
sleep 10;
python2 main_program.py 14;
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem corrupt 0.005%;
sleep 10;
python2 main_program.py 15;
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem corrupt 0.01%;
sleep 10;
python2 main_program.py 16;
tc qdisc del dev eno1 root;

#packet reordering

tc qdisc add dev eno1 root netem reorder 0.001%;
sleep 10;
python2 main_program.py 17;
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem reorder 0.005%;
sleep 10;
python2 main_program.py 18;
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem reorder 0.01%;
sleep 10;
python2 main_program.py 19;
tc qdisc del dev eno1 root;

#bandwith limit
tc qdisc add dev eno1 root tbf rate 7MBit burst 32Mbit limit 30000;
sleep 10;
python2 main_program.py 20;
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root tbf rate 8MBit burst 32Mbit limit 30000;
sleep 10;
python2 main_program.py 21;
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root tbf rate 9MBit burst 32Mbit limit 30000;
sleep 10;
python2 main_program.py 22;
tc qdisc del dev eno1 root;
