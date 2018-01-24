#!/usr/bin/python

from datetime import datetime, timedelta

import os


def main():
    # LogFormat "%h %l %u %t \"%r\" %>s %D %O \"%{Referer}i\" \"%{User-Agent}i\"" combined

    zabbixserver = "127.0.0.1"
    host = "example.com"
    apachelog = open("/var/log/apache2/access.log", "r")

    ttime = (datetime.now()-timedelta(minutes=1)).strftime("%d/%b/%Y:%H:%M")

    responsecode, outputtime = 0, 0
    rmstime, avgtime = 0, 0
    rmscount, avgcount = 0, 0
    code500 = 0
    gtime, atime, btime = 0, 0, 0

    for line in apachelog.readlines():
        split_line = line.split()
        
        if split_line[5] == "\"GET" and split_line[3][1:-3] == ttime:
            responsecode = line.split(' ')[8]
            outputtime = float(line.split(' ')[9])
            if int(split_line[8]) < 500:
                if outputtime > 230000:
                    rmstime += outputtime
                    rmscount += 1

                avgtime += outputtime
                avgcount += 1
                if outputtime < 500000:
                    gtime += 1
                elif outputtime < 1000000:
                    atime += 1
                else:
                    btime += 1
            else:
                code500 += 1

    status = ["apache.response.good", "apache.response.avg", "apache.response.bad", "apache.response.5xx", "apache.response.time"]
    args = [gtime, atime, btime, code500, 0.000001*avgtime/avgcount]

    if rmscount > 0:
        status += ["apache.response.rmstime"]
        args += [0.000001*rmstime/rmscount]

    for stat, arg in zip(status, args):
        cmd = "/usr/bin/zabbix_sender -z %s -s %s -k %s -o %s" % (zabbixserver, host, stat, arg)
        os.system(cmd)


if __name__ == '__main__':
    main()
