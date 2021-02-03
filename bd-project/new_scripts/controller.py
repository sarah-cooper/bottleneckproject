import subprocess
from subprocess import PIPE, Popen, check_output

pid = 0
def transfer_file(i):
    global pid
    comm_ss = ['python2', 'client.py']
    strings = ""
    proc = subprocess.Popen(comm_ss, stdout=subprocess.PIPE)
    pid = check_output(['pidof', '-s', 'python2', 'client.py'])
    print(pid)
    while(True):
        line = str(proc.stdout.readline()).replace("\r", "\n")
        strings+= line
        if not line.decode("utf-8"):
            break
        strings.replace("\r", "\n")


# transfer_file(0)
def get_disk_stat():
    drive_name = "sda"
    proc = Popen(['iostat','-x',drive_name], universal_newlines=True, stdout=PIPE)
    res = proc.communicate()[0]
    parts = res.split("\n")

    for part in parts:
        # print(part)
        if len(part.strip())>0 and drive_name in part:
            lst = part.split(" ")
            lst_without_space=[]
            for element in lst:
                if len(element)>0:
                    lst_without_space.append(element)
            # print(lst_without_space)
            
            # r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
            read_req = lst_without_space[1]
            write_req = lst_without_space[2]
            rkB = lst_without_space[3]
            wkB = lst_without_space[4]
            rrqm = lst_without_space[5]
            wrqm = lst_without_space[6]
            rrqm_perc = lst_without_space[7]
            wrqm_perc = lst_without_space[8]
            r_await = lst_without_space[9]
            w_await = lst_without_space[10]
            areq_sz = lst_without_space[11]
            rareq_sz = lst_without_space[12]
            wareq_sz = lst_without_space[13]
            svctm = lst_without_space[14]
            util = lst_without_space[15]

    print(read_req," ",write_req," ",rkB," ",wkB," ",rrqm," ",wrqm," ",rrqm_perc," ",wrqm_perc," ",r_await," ",w_await," ",areq_sz," ",rareq_sz," ",wareq_sz," ",svctm," ",util)
    return read_req,write_req,rkB,wkB,rrqm,wrqm,rrqm_perc,wrqm_perc,r_await,w_await,areq_sz,rareq_sz,wareq_sz,svctm,util

print(get_disk_stat())