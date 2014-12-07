/*
 *  Author: Maarten Vandersteegen
 *  Wrapper to initialize PicoTCP
 */
#include "pico_stack.h"
#include "pico_ipv4.h"
#include "pico_dev_tun.h"
#include <pico_icmp4.h>
#include <unistd.h>

int picotcp_init(char *ip, char *nm, char *tun)
{
    struct pico_device *dev = NULL;
    struct pico_ip4 ipaddr, netmask;

    pico_stack_init();
    dev = pico_tun_create(tun);
    if (!dev) {
        perror("Creating tun failed");
        return -1;
    }

    pico_string_to_ipv4(ip, &ipaddr.addr);
    pico_string_to_ipv4(nm, &netmask.addr);
    pico_ipv4_link_add(dev, ipaddr, netmask);
    return 0;
}
