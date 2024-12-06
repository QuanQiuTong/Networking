#include <stdio.h>


extern int TRACE;
extern int YES;
extern int NO;

struct distance_table {
	int costs[4][4];
} dt0;

/* students to write the following two routines, and maybe some others */

#define NODE_ID 0
#define CONNECTCOSTS {0, 1, 3, 7}
#include "node.h"

void rtinit0()
{
    rtinit();
}

void rtupdate0(struct rtpkt *rcvdpkt)
{
    rtupdate(rcvdpkt);
}

void printdt0(dtptr)
struct distance_table *dtptr;
{
	printf("                via     \n");
	printf("   D0 |    0    1     2    3 \n");
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

void linkhandler0(int linkid, int newcost)
{
    linkhandler(linkid, newcost);
}
