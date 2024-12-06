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

struct distance_table 
{
  int costs[4][4];
} dt3;

/* students to write the following two routines, and maybe some others */

extern float clocktime;
#define INFINITY 999

void rtinit3() {
    int i, j;
    
    /* 初始化距离表 */
    for(i = 0; i < 4; i++)
        for(j = 0; j < 4; j++)
            dt3.costs[i][j] = INFINITY;
            
    dt3.costs[0][0] = 7;    /* 到节点0的开销 */
    dt3.costs[2][2] = 2;    /* 到节点2的开销 */
    dt3.costs[3][3] = 0;
    
    printf("\nAt time t=%.3f, rtinit3() called\n", clocktime);
    printdt3(&dt3);
    
    /* 发送初始路由信息 */
    struct rtpkt packet;
    packet.sourceid = 3;
    for(i = 0; i < 4; i++) {
        packet.mincost[i] = dt3.costs[i][i];
    }
    
    packet.destid = 0;
    tolayer2(packet);
    packet.destid = 2;
    tolayer2(packet);
    
    printf("Node 3 sends update to neighbors 0,2\n");
}


void rtupdate3(struct rtpkt *rcvdpkt) {
    int changed = 0;
    int i;
    
    printf("\nAt time t=%.3f, rtupdate3() from node %d\n", 
           clocktime, rcvdpkt->sourceid);
           
    for(i = 0; i < 4; i++) {
        if(i == 3)
            continue;
        int newcost = dt3.costs[rcvdpkt->sourceid][rcvdpkt->sourceid] + 
                     rcvdpkt->mincost[i];
        if(newcost < dt3.costs[i][rcvdpkt->sourceid]) {
            dt3.costs[i][rcvdpkt->sourceid] = newcost;
            changed = 1;
        }
    }
    
    printdt3(&dt3);
    
    if(changed) {
        struct rtpkt packet;
        packet.sourceid = 3;
        /* 计算到每个目标的最小开销 */
        for(i = 0; i < 4; i++) {
            int min = INFINITY;
            int j;
            for(j = 0; j < 4; j++) {
                if(dt3.costs[i][j] < min) {
                    min = dt3.costs[i][j]; 
                }
            }
            packet.mincost[i] = min;
        }
        packet.destid = 0;
        tolayer2(packet);
        packet.destid = 2;
        tolayer2(packet);
        
        printf("Node 3 sends update to neighbors 0,2\n");
    } else {
        printf("Distance table unchanged\n");
    }
}


printdt3(dtptr)
  struct distance_table *dtptr;
  
{
  printf("             via     \n");
  printf("   D3 |    0     2 \n");
  printf("  ----|-----------\n");
  printf("     0|  %3d   %3d\n",dtptr->costs[0][0], dtptr->costs[0][2]);
  printf("dest 1|  %3d   %3d\n",dtptr->costs[1][0], dtptr->costs[1][2]);
  printf("     2|  %3d   %3d\n",dtptr->costs[2][0], dtptr->costs[2][2]);

}
