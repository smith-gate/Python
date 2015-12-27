#!/usr/bin/env python
import socket
import sys
import threading
import time
import re

TIMEOUT = 5


def scan(ip, port):
    try:
        cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        cs.settimeout(float(TIMEOUT))
        status = cs.connect_ex((str(ip), int(port)))
        if status == 0:
            print str(ip) + ':' + str(port) + '\topen'
    except Exception, e:
        print 'error:%s' % e
        return -1
    cs.close()
    return 1

def hostname(ip):
    try:
        hostname, aliases, addresses = socket.gethostbyaddr(ip)
        print '+++++++++++++++++++++++++++++++++++++'
        print '[+]Hostname :', hostname
        print '[+]Aliases  :', aliases
        print '[+]Addresses:', addresses
        print '+++++++++++++++++++++++++++++++++++++'
    except socket.herror, e:
        pass

def thread_scan(ports):
    global ips, mutex
    #print ips
    while 1:
        if len(ips) > 0:
            mutex.acquire()
            ip = ips[-1]
            ips.pop()
            mutex.release()
            #run hostnama
            hostname(ip)
            #run scan
            for x in ports:
                scan(ip, x)
        else:
            break
            return 1

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print '[-]Usage::scan.py startip-endip port1,port2,port3.... threads\n'
        print '[-]Ex   ::scan.py 192.168.0.1-255 22,135,3389 100\n'

    ip_se = sys.argv[1]
    port_se = sys.argv[2]
    t_num = sys.argv[3]

    global mutex, ips
    ips = []
    ports = []
    threads = []
    #get ips
    ilist = re.split(r'[\.|\-]', ip_se)
    snum = int(ilist[3])
    for x in xrange(int(ilist[4]) - snum + 1):
        ips.append('.'.join((ilist[0], ilist[1], ilist[2], ilist[3])))
        ilist[3] = str(int(ilist[3]) + 1)
    #
    #get ports
    ports = port_se.split(',')
    #
    #print begin time
    print str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    print '=========================='
    #creating threads
    mutex = threading.Lock()
    for x in xrange(int(t_num)):
        t = threading.Thread(target = thread_scan, args = (ports, ))
        threads.append(t)
    for x in threads:
        x.start()
    for x in threads:
        x.join()
    #print end time
    print '=========================='
    print str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
