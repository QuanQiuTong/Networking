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
} dt2;


/* students to write the following two routines, and maybe some others */

extern float clocktime;
#define INFINITY 999

void rtinit2() {
    int i, j;
    
    /* 初始化距离表 */
    for(i = 0; i < 4; i++)
        for(j = 0; j < 4; j++)
            dt2.costs[i][j] = INFINITY;
            
    dt2.costs[0][0] = 3;    /* 到节点0的开销 */
    dt2.costs[1][1] = 1;    /* 到节点1的开销 */
    dt2.costs[2][2] = 0;    
    dt2.costs[3][3] = 2;    /* 到节点3的开销 */
    
    printf("\nAt time t=%.3f, rtinit2() called\n", clocktime);
    printdt2(&dt2);
    
    /* 发送初始路由信息 */
    struct rtpkt packet;
    packet.sourceid = 2;
    for(i = 0; i < 4; i++) {
        packet.mincost[i] = dt2.costs[i][i];
    }
    
    packet.destid = 0;
    tolayer2(packet);
    packet.destid = 1;
    tolayer2(packet);
    packet.destid = 3;
    tolayer2(packet);
    
    printf("Node 2 sends update to neighbors 0,1,3\n");
}


void rtupdate2(struct rtpkt *rcvdpkt) {
    int changed = 0;
    int i;
    
    printf("\nAt time t=%.3f, rtupdate2() from node %d\n", 
           clocktime, rcvdpkt->sourceid);
           
    for(i = 0; i < 4; i++) {
        if(i == 2)
            continue;
        int newcost = dt2.costs[rcvdpkt->sourceid][rcvdpkt->sourceid] + 
                     rcvdpkt->mincost[i];
        if(newcost < dt2.costs[i][rcvdpkt->sourceid]) {
            dt2.costs[i][rcvdpkt->sourceid] = newcost;
            changed = 1;
        }
    }
    
    printdt2(&dt2);
    
    if(changed) {
        struct rtpkt packet;
        packet.sourceid = 2;
        /* 计算到每个目标的最小开销 */
        for(i = 0; i < 4; i++) {
            int min = INFINITY;
            int j;
            for(j = 0; j < 4; j++) {
                if(dt2.costs[i][j] < min) {
                    min = dt2.costs[i][j]; 
                }
            }
            packet.mincost[i] = min;
        }
        packet.destid = 0;
        tolayer2(packet);
        packet.destid = 1;
        tolayer2(packet);
        packet.destid = 3;
        tolayer2(packet);
        
        printf("Node 2 sends update to neighbors 0,1,3\n");
    } else {
        printf("Distance table unchanged\n");
    }
}


printdt2(dtptr)
  struct distance_table *dtptr;
  
{
  printf("                via     \n");
  printf("   D2 |    0     1    3 \n");
  printf("  ----|-----------------\n");
  printf("     0|  %3d   %3d   %3d\n",dtptr->costs[0][0],
   dtptr->costs[0][1],dtptr->costs[0][3]);
  printf("dest 1|  %3d   %3d   %3d\n",dtptr->costs[1][0],
   dtptr->costs[1][1],dtptr->costs[1][3]);
  printf("     3|  %3d   %3d   %3d\n",dtptr->costs[3][0],
   dtptr->costs[3][1],dtptr->costs[3][3]);
}
