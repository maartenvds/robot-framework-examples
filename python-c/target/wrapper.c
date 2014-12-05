/*
 *  Author: Maarten Vandersteegen
 *  Wrapper for PicoTCP's ping functionailty
 */
#include "pico_stack.h"
#include "pico_ipv4.h"
#include "pico_dev_tun.h"
#include <pico_icmp4.h>
#include <unistd.h>

static void (*callback_ping)(void) = NULL;

void cb_ping(struct pico_icmp4_stats *s)
{
    char host[30];
    pico_ipv4_to_string(host, s->dst.addr);
    if (callback_ping != NULL)
        callback_ping();
    /*
    if (s->err == 0) {
        dbg("%lu bytes from %s: icmp_req=%lu ttl=%lu time=%lu ms\n", s->size, host, s->seq,
                s->ttl, (long unsigned int)s->time);
        if (s->seq >= NUM_PING)
            exit(0);
    } else {
        dbg("PING %lu to %s: Error %d\n", s->seq, host, s->err);
        exit(1);
    }*/
}

void app_ping(char *dest, int count, int interval, int timeout, int size, void (*cb)(void))
{
    callback_ping = cb;
    pico_icmp4_ping(dest,  count, interval, timeout, size, cb_ping);
}

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
