#!/bin/sh
python3 all_metrics.py 0

stress-ng --vm-bytes 100k --vm-keep -m 5 &
sleep 10;
python3 all_metrics.py 1
killall stress-ng;
sleep 10;

stress-ng --vm-bytes 5000k --vm-keep -m 10 &
sleep 10;
python3 all_metrics.py 2
killall stress-ng;
sleep 10;

stress-ng --vm-bytes 20000k --vm-keep -m 20 &
sleep 10;
python3 all_metrics.py 3
killall stress-ng;
sleep 10;

stress -d 5 &
sleep 10;
python3 all_metrics.py 4
killall stress;
sleep 10;

stress -d 10 &
sleep 10;
python3 all_metrics.py 5
killall stress;
sleep 10;

stress -d 16 &
sleep 10;
python3 all_metrics.py 6
killall stress;
sleep 10;

stress -i 100 &
sleep 10;
python3 all_metrics.py 7
killall stress;
sleep 10;

stress -i 500 &
sleep 10;
python3 all_metrics.py 8
killall stress;
sleep 10;

stress -i 1000 &
sleep 10;
python3 all_metrics.py 9
killall stress;
sleep 10;

stress -c 10 &
sleep 10;
python3 all_metrics.py 10
killall stress;
sleep 10;

stress -c 25 &
sleep 10;
python3 all_metrics.py 11
killall stress;
sleep 10;

stress -c 40 &
sleep 10;
python3 all_metrics.py 12
killall stress;
sleep 10;

#packet loss

tc qdisc add dev eno1 root netem loss 0.001%;
sleep 10;
python3 all_metrics.py 13
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem loss 0.005%;
sleep 10;
python3 all_metrics.py 14
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem loss 0.01%;
sleep 10;
python3 all_metrics.py 15
tc qdisc del dev eno1 root;

#packet delay
tc qdisc add dev eno1 root netem delay 1ms 1ms distribution normal;
sleep 10;
python3 all_metrics.py 16
tc qdisc del dev eno1 root;

 tc qdisc add dev eno1 root netem delay 2ms 1ms distribution normal;
sleep 10;
python3 all_metrics.py 17
 tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem delay 3ms 1ms distribution normal;
sleep 10;
python3 all_metrics.py 18
tc qdisc del dev eno1 root;

#packet duplicate

tc qdisc add dev eno1 root netem duplicate 0.001%;
sleep 10;
python3 all_metrics.py 19
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem duplicate 0.005%;
sleep 10;
python3 all_metrics.py 20
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem duplicate 0.01%;
sleep 10;
python3 all_metrics.py 21
tc qdisc del dev eno1 root;

#packet corrupt

tc qdisc add dev eno1 root netem corrupt 0.001%;
sleep 10;
python3 all_metrics.py 22
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem corrupt 0.005%;
sleep 10;
python3 all_metrics.py 23
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem corrupt 0.01%;
sleep 10;
python3 all_metrics.py 24
tc qdisc del dev eno1 root;

#packet reordering

tc qdisc add dev eno1 root netem reorder 0.001%;
sleep 10;
python3 all_metrics.py 25
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem reorder 0.005%;
sleep 10;
python3 all_metrics.py 26
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root netem reorder 0.01%;
sleep 10;
python3 all_metrics.py 27
tc qdisc del dev eno1 root;

#bandwith limit
tc qdisc add dev eno1 root tbf rate 7MBit burst 32Mbit limit 30000;
sleep 10;
python3 all_metrics.py 28
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root tbf rate 8MBit burst 32Mbit limit 30000;
sleep 10;
python3 all_metrics.py 29
tc qdisc del dev eno1 root;

tc qdisc add dev eno1 root tbf rate 9MBit burst 32Mbit limit 30000;
sleep 10;
python3 all_metrics.py 30
tc qdisc del dev eno1 root;
