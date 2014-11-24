#!/usr/bin/python

"""
Auther:zhangcong
Time: 2014-11-17
Describe:
    create net-topo and do some testing

Topo: Create a network ,where three different hosts are connected to
 a switch, which is connected a controller.

Testing: the bandwith
        between h1 and h3 ,h1 and h3 ,when loadbalancer is enable and activated

Modify: liuwenxue
Comment : fix some bug, make more readable
"""


from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller,RemoteController

from mininet.topolib import TreeTopo # ????????????
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCLink #tcp?
from mininet.node import CPULimitedHost#cup usage per host
from mininet.util import dumpNodeConnections
import time
import os 
import os.path
import sys



#ip_controller,ip_switch,bw_link,delay_link,loss_link

def loaderbanlanceNet(control_ip):

    "Create a network from semi-scratch with one controller."
    if not control_ip:
        sys.exit(1)
    ip_controller=control_ip
    ip_switch="10.0.0.5"
    bw_link=100 # 100 M
    delay_link='0ms'
    loss_link=0 # 0%
    total_client_num = 6 # clint ip total number must <=25600
    total_time_per = 1
    inter_time_per = 1
    ip_vip ="10.0.0.100" 

    #net
    net = Mininet( controller=Controller, switch=OVSSwitch, build=False, host=CPULimitedHost, link=TCLink)
    #controller
    print "*** Creating (reference) controller"
    c1 = RemoteController( 'c1', ip=ip_controller )
    #switch
    print "*** Creating and configuring switche"
    s1 = net.addSwitch( 's1' )
    s1.setIP(ip_switch, 8 )
    #hosts
    print "*** Creating and configuring hosts"
    hosts1 = [ net.addHost( 'h%d' % n,cpu=.5 / 4) for n in 1, 2, 3 ] #  4 hosts and Each host gets 50%/n of system CPU
    #links
    print "*** Creating links"
    for h in hosts1:
        net.addLink( s1, h, bw=bw_link, delay=delay_link, loss=loss_link, use_htb=True)#  10 Mbps, 5ms delay, 10% loss

    # start network
    print "*** Starting network"
    net.build()# NOTE build() at this time
    c1.start()
    s1.start( [ c1 ] )

    #set host ip
    print "*** get node and set nodeip after net start"
    h1, h2, h3 = net.getNodeByName('h1', 'h2', 'h3')# NOTE you must get the host name before you use it
    h1.setIP('10.0.0.1', 8 )
    h2.setIP('10.0.0.2', 8 )
    h3.setIP('10.0.0.3', 8 )

    print "*** Testing network connectivity"
    net.pingAll()# you must pingall to add???? the floadbalancer low-entry for ip 10.0.0.100

    print "*** Testing load-balance module "
    curdir = os.path.abspath(os.curdir)
    h3.cmd('rm %s/loaddata/*.data' % curdir)
    h3.cmd('mkdir -p %s/loaddata/' % curdir)
    h3.cmd('touch %s/loaddata/h1.data %s/loaddata/h2.data %s/loaddata/h3.data' %
    (curdir, curdir, curdir))
    h1.cmd('iperf -s >> %s/loaddata/h1.data &' % curdir)
    h2.cmd('iperf -s >> %s/loaddata/h2.data &' % curdir)

    client_num = 0
    #default_ip = '10.0.0.6', controller ip  :10.0.0.100
    i=0
    j=6
    while client_num < total_client_num:
        h3.setIP('10.0.%d.%d' %(i,j),8)
        if j%256 == 0:
            i+=1
            j=1
        client_num +=1
        j+=1
        print 'client: %d ip: %s' % (client_num,h3.IP())
        if h3.IP() == ip_controller: # NOTE:host ip is not able to equal controller ip
            continue 
        h3.cmd("iperf -c 10.0.0.100 -t%d -i%d >> %s/loaddata/h3.data " %
        (total_time_per, inter_time_per, curdir))
        time.sleep(2)
    else:
        print 'The test loop is over,total client num :%d' % client_num

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        loaderbanlanceNet(argv[1])
    else:
        print "Usage: python %s control_ip" %sys.argv[0]
        sys.exit(1)
