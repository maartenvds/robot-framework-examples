#
# PicoTCP test library
# Author: Maarten Vandersteegen
#

import os
import time
from ctypes import *

#----------------------------------------------------------------------------#
#                          Custom C data types                               #
#----------------------------------------------------------------------------#

class pico_ip4(Structure):
    _pack_ = 1
    _fields_ = [("addr", c_uint)]

class pico_icmp4_stats(Structure):
    _fields_ = [("dst", pico_ip4),
                ("size", c_ulong),
                ("seq", c_ulong),
                ("time", c_ulonglong),
                ("ttl", c_ulong),
                ("err", c_int)]
    
#----------------------------------------------------------------------------#
#                              Test library                                  #
#----------------------------------------------------------------------------#

class PicoTCP(object):
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, dll="target/libpicotcp.so"):
        """Load device under test
        """
        self.dut = CDLL(os.getcwd() + "/" + dll)
        self.ping_stats = []

    def stack_init(self, ip, netmask, tun="tun0"):
        """Initialize PicoTCP
        """
        r = self.dut.picotcp_init(c_char_p(ip), c_char_p(netmask), c_char_p(tun))
        assert r == 0, "Initialize failed, rc = %d"%r

    def get_ping_stats(self):
        """Retreive the ping stats
        """
        return self.ping_stats

    def stack_tick(self, period, interval=0.005):
        """Tick the stack for some period of time
        """
        start = time.time()
        while time.time() < (start + period):
            self.dut.pico_stack_tick()
            time.sleep(interval)

    def ping(self, dest, count, interval, timeout, size):
        """Run ping client
        """
        self.ping_stats = []
        def cb_ping(s):
            """Ping client callback as closure to be able to access the self
            object without the need to provide it as an argument
            """
            print "Callback called"
            assert s.contents.err == 0, \
                    "Ping callback reports error code %d"%s.contents.err
            stats = {}
            host = create_string_buffer(30)
            self.dut.pico_ipv4_to_string(host, s.contents.dst.addr)
            stats["host"] = host.value
            stats["size"] = s.contents.size
            stats["seq"] = s.contents.seq
            stats["time"] = s.contents.time
            stats["ttl"] = s.contents.ttl
            self.ping_stats.append(stats)

        # C signature: void(struct pico_icmp4_stats *s)
        Callback = CFUNCTYPE(None, POINTER(pico_icmp4_stats))
        cb = Callback(cb_ping)
        self.dut.pico_icmp4_ping(c_char_p(dest), c_int(count), c_int(interval), 
                                            c_int(timeout), c_int(size), cb)
        self.stack_tick(timeout/1000)

if __name__ == "__main__":

    dut = PicoTCP("../target/libpicotcp.so")
    dut.stack_init("192.168.3.3", "255.255.255.0")
    os.system("ifconfig tun0 inet 192.168.3.1 netmask 255.255.255.0")
    dut.ping("192.168.3.1", 10, 1000, 15000, 64)
    print dut.get_ping_stats()
