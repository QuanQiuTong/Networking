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
} dt0;


/* students to write the following two routines, and maybe some others */

extern float clocktime;
#define INFINITY 999

void rtinit0() {
    int i, j;
    
    /* 初始化距离表为无穷大 */
    for(i = 0; i < 4; i++)
        for(j = 0; j < 4; j++)
            dt0.costs[i][j] = INFINITY;
    
    /* 设置直接相连的开销 */
    dt0.costs[0][0] = 0;
    dt0.costs[1][1] = 1;    /* 到节点1的开销 */
    dt0.costs[2][2] = 3;    /* 到节点2的开销 */
    dt0.costs[3][3] = 7;    /* 到节点3的开销 */
    
    /* 打印初始距离表 */
    printf("\nAt time t=%.3f, rtinit0() called\n", clocktime);
    printf("Initial distance table at node 0:\n");
    printdt0(&dt0);
    
    /* 创建并发送更新包给邻居 */
    struct rtpkt packet;
    packet.sourceid = 0;
    for(i = 0; i < 4; i++) {
        packet.mincost[i] = dt0.costs[i][i];
    }
    
    /* 发送给节点1、2、3 */
    packet.destid = 1;
    tolayer2(packet);
    packet.destid = 2;
    tolayer2(packet);
    packet.destid = 3;
    tolayer2(packet);
    
    printf("Node 0 sends update to neighbors 1,2,3\n");
}


void rtupdate0(struct rtpkt *rcvdpkt) {
    int i;
    int changed = 0;
    
    printf("\nAt time t=%.3f, rtupdate0() called, received packet from node %d\n", 
           clocktime, rcvdpkt->sourceid);
    
    /* 更新距离表 */
    for(i = 0; i < 4; i++) {
       if(i == 0)
            continue;
        int newcost = dt0.costs[rcvdpkt->sourceid][rcvdpkt->sourceid] + 
                     rcvdpkt->mincost[i];
        if(newcost < dt0.costs[i][rcvdpkt->sourceid]) {
            dt0.costs[i][rcvdpkt->sourceid] = newcost;
            changed = 1;
        }
    }
    
    /* 打印当前距离表 */
    printf("Current distance table at node 0:\n");
    printdt0(&dt0);
    
    /* 如果有改变，通知邻居 */
    if(changed) {
        struct rtpkt packet;
        packet.sourceid = 0;
        /* 计算到每个目标的最小开销 */
        for(i = 0; i < 4; i++) {
            int min = INFINITY;
            int j;
            for(j = 0; j < 4; j++) {
                if(dt0.costs[i][j] < min) {
                    min = dt0.costs[i][j]; 
                }
            }
            packet.mincost[i] = min;
        }
        
        /* 发送给所有邻居 */
        packet.destid = 1;
        tolayer2(packet);
        packet.destid = 2;
        tolayer2(packet);
        packet.destid = 3;
        tolayer2(packet);
        
        printf("Node 0 sends update to neighbors 1,2,3\n");
    } else {
        printf("Distance table unchanged\n");
    }
}


printdt0(dtptr)
  struct distance_table *dtptr;
  
{
  printf("                via     \n");
  printf("   D0 |    1     2    3 \n");
  printf("  ----|-----------------\n");
  printf("     1|  %3d   %3d   %3d\n",dtptr->costs[1][1],
   dtptr->costs[1][2],dtptr->costs[1][3]);
  printf("dest 2|  %3d   %3d   %3d\n",dtptr->costs[2][1],
   dtptr->costs[2][2],dtptr->costs[2][3]);
  printf("     3|  %3d   %3d   %3d\n",dtptr->costs[3][1],
   dtptr->costs[3][2],dtptr->costs[3][3]);
}


/* called when cost from 0 to linkid changes from current value to newcost */
/* You can leave this routine empty if you're an undergrad. If you want */
/* to use this routine, you'll need to change the value of the LINKCHANGE */
/* constant definition in prog3.c from 0 to 1 */
void linkhandler0(int linkid, int newcost) 
{
    /* 更新到linkid的直接链路成本 */
    dt0.costs[linkid][linkid] = newcost;
    
    printf("\nAt time t=%.3f, linkhandler0() called for link to %d, new cost=%d\n", 
           clocktime, linkid, newcost);
    printf("Current distance table at node 0:\n");
    printdt0(&dt0);

    /* 重新计算最小开销并通知邻居 */
    struct rtpkt packet;
    packet.sourceid = 0;
    int i;
    for(i = 0; i < 4; i++) {
        int min = INFINITY;
        int j;
        for(j = 0; j < 4; j++) {
            if(dt0.costs[i][j] < min) {
                min = dt0.costs[i][j];
            }
        }
        packet.mincost[i] = min;
    }
    
    /* 发送给所有邻居 */
    packet.destid = 1;
    tolayer2(packet);
    packet.destid = 2; 
    tolayer2(packet);
    packet.destid = 3;
    tolayer2(packet);
    
    printf("Node 0 sends update to neighbors due to link cost change\n");
}
