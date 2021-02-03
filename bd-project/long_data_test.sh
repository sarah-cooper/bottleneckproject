#!/bin/bash
function run_tstat()
{
        tstat -l -i enp0s31f6 -s  $1 &
        TSTAT_PID=$!
        echo "TSTAT Started, PID = $TSTAT_PID"
        sleep 1
        for i in {1..6}
                do
                        for j in {1..6}
                                do
                                        echo "Starting iPerf Test #$i.$j"
                                        globus-url-copy -vb -t 30 largefile1.txt ftp://134.197.40.114:50505/home/masudulhasanmasudb/
                                        echo "iPerf Complete"
                                done
                done
        kill -s INT $TSTAT_PID
}

stress -i 1000 &
run_tstat  OUT_DATA/high_io
sudo killall stress

stress -m 15 &
run_tstat  OUT_DATA/high_memory
sudo killall stress

stress stress -d 1000 &
run_tstat  OUT_DATA/high_disk_load
sudo killall stress

