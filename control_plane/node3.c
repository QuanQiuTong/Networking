#include <stdio.h>
struct distance_table {
    int costs[4][4];
} dt3;

#define NODE_ID 3
#define CONNECTCOSTS {7, 999, 2, 0}
#include "node.h"

void rtinit3()
{
    rtinit();
}

void rtupdate3(struct rtpkt *rcvdpkt)
{
    rtupdate(rcvdpkt);
}

void printdt3(struct distance_table *dtptr)
{
    printf("                via     \n");
    printf("   D3 |    0    1     2    3 \n");
    printf("  ----|----------------------\n");
    printf("     0|  %3d   %3d   %3d  %3d\n", dtptr->costs[0][0],
           dtptr->costs[0][1], dtptr->costs[0][2], dtptr->costs[0][3]);
    printf("     1|  %3d   %3d   %3d  %3d\n", dtptr->costs[1][0],
           dtptr->costs[1][1], dtptr->costs[1][2], dtptr->costs[1][3]);
    printf("     2|  %3d   %3d   %3d  %3d\n", dtptr->costs[2][0],
           dtptr->costs[2][1], dtptr->costs[2][2], dtptr->costs[2][3]);
    printf("     3|  %3d   %3d   %3d  %3d\n", dtptr->costs[3][0],
           dtptr->costs[3][1], dtptr->costs[3][2], dtptr->costs[3][3]);
}