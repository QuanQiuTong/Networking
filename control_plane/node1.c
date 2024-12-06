#include <stdio.h>

struct rtpkt {
  int sourceid;       /* id of sending router sending this pkt */
  int destid;         /* id of router to which pkt being sent 
                       (must be an immediate neighbor) */
  int mincost[4];    /* min cost to node 0 ... 3 */
  };


extern int TRACE;
extern int YES;
extern int NO;

int connectcosts1[4] = { 1,  0,  1, 999 };

struct distance_table 
{
  int costs[4][4];
} dt1;


/* students to write the following two routines, and maybe some others */

extern float clocktime;
#define INFINITY 999

void rtinit1() {
    int i, j;
    
    for(i = 0; i < 4; i++)
        for(j = 0; j < 4; j++)
            dt1.costs[i][j] = INFINITY;
            
    dt1.costs[0][0] = 1;    /* 到节点0的开销 */
    dt1.costs[1][1] = 0;    
    dt1.costs[2][2] = 1;    /* 到节点2的开销 */
    
    printf("\nAt time t=%.3f, rtinit1() called\n", clocktime);
    printdt1(&dt1);
    
    struct rtpkt packet;
    packet.sourceid = 1;
    for(i = 0; i < 4; i++) {
        packet.mincost[i] = dt1.costs[i][i];
    }
    
    packet.destid = 0;
    tolayer2(packet);
    packet.destid = 2;
    tolayer2(packet);
}


void rtupdate1(struct rtpkt *rcvdpkt) {
    int changed = 0;
    int i;
    
    printf("\nAt time t=%.3f, rtupdate1() from node %d\n", 
           clocktime, rcvdpkt->sourceid);
           
    for(i = 0; i < 4; i++) {
        if(i == 1)
            continue;
        int newcost = dt1.costs[rcvdpkt->sourceid][rcvdpkt->sourceid] + 
                     rcvdpkt->mincost[i];
        if(newcost < dt1.costs[i][rcvdpkt->sourceid]) {
            dt1.costs[i][rcvdpkt->sourceid] = newcost;
            changed = 1;
        }
    }
    
    printdt1(&dt1);
    
    if(changed) {
        struct rtpkt packet;
        packet.sourceid = 1;
        /* 计算到每个目标的最小开销 */
        for(i = 0; i < 4; i++) {
            int min = INFINITY;
            int j;
            for(j = 0; j < 4; j++) {
                if(dt1.costs[i][j] < min) {
                    min = dt1.costs[i][j]; 
                }
            }
            packet.mincost[i] = min;
        }
        packet.destid = 0;
        tolayer2(packet);
        packet.destid = 2;
        tolayer2(packet);
    }
}


printdt1(dtptr)
  struct distance_table *dtptr;
  
{
  printf("             via   \n");
  printf("   D1 |    0     2 \n");
  printf("  ----|-----------\n");
  printf("     0|  %3d   %3d\n",dtptr->costs[0][0], dtptr->costs[0][2]);
  printf("dest 2|  %3d   %3d\n",dtptr->costs[2][0], dtptr->costs[2][2]);
  printf("     3|  %3d   %3d\n",dtptr->costs[3][0], dtptr->costs[3][2]);

}


/* called when cost from 1 to linkid changes from current value to newcost*/
/* You can leave this routine empty if you're an undergrad. If you want */
/* to use this routine, you'll need to change the value of the LINKCHANGE */
/* constant definition in prog3.c from 0 to 1 */
void linkhandler1(int linkid, int newcost) {
    dt1.costs[linkid][linkid] = newcost;
    
    printf("\nAt time t=%.3f, linkhandler1() called for link to %d\n", 
           clocktime, linkid);
    printdt1(&dt1);
    
    struct rtpkt packet;
    packet.sourceid = 1;
    int i;
    for(i = 0; i < 4; i++) {
        packet.mincost[i] = dt1.costs[i][i];
    }
    
    packet.destid = 0;
    tolayer2(packet);
    packet.destid = 2;
    tolayer2(packet);
}
