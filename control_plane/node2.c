#include <stdio.h>


extern int TRACE;
extern int YES;
extern int NO;

struct distance_table {
    int costs[4][4];
} dt2;

#define NODE_ID 2
#define CONNECTCOSTS {3, 1, 0, 2}
#include "node.h"

void rtinit2()
{
    rtinit();
}

void rtupdate2(struct rtpkt *rcvdpkt)
{
    rtupdate(rcvdpkt);
}

void printdt2(dtptr)
struct distance_table *dtptr;
{
    printf("                via     \n");
    printf("   D2 |    0    1     2    3 \n");
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