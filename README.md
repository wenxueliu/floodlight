Floodlight is the leading open source SDN controller. It is supported by a community of developers including a number of engineers from Big Switch Networks (http://www.bigswitch.com/).

OpenFlow is a open standard managed by Open Networking Foundation. It specifies a protocol through switch a remote controller can modify the behavior of networking devices through a well-defined “forwarding instruction set”. Floodlight is designed to work with the growing number of switches, routers, virtual witches, and access points that support the OpenFlow standard.

Feature Highlights:

- Offers a module loading system that make it simple to extend and enhance.
- Easy to set up with minimal dependencies
- Supports a broad range of virtual- and physical- OpenFlow switches
- Can handle mixed OpenFlow and non-OpenFlow networks – it can manage multiple “islands” of OpenFlow hardware switches
- Designed to be high-performance – is the core of a commercial product from Big Switch Networks.
- Support for OpenStack Quantum cloud orchestration platform}

To download a pre-built VM appliance, access documentation, and sign up for the mailing list, go to:

  http://www.projectfloodlight.org/floodlight


###LoadBalance

$ ./floodlight
$ ./loadbalance_add
$ sudo mn --topo single,3 --mac --switch ovsk --controller=remote,ip=192.168.1.103 // IP is you controller IP
 mininet > xterm h1 h2 h3

in h1 : nc -k -l 7777
in h2 : nc -k -l 7777
in h3 : nc 10.0.0.100 7777 //ENTER
        "abc"

in h1 or h2 echo "abc"

see the log ouput :

    sw 00:00:00:00:00:00:00:01 useage 2/5000
    sw 00:00:00:00:00:00:00:01 useage 1/5000
