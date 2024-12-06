#ifndef NODE_H
#define NODE_H

#include <stdio.h>

struct rtpkt {
	int sourceid;       /* id of sending router sending this pkt */
	int destid;         /* id of router to which pkt being sent
						   (must be an immediate neighbor) */
	int mincost[4];    /* min cost to node 0 ... 3 */
};

static struct distance_table dt;

extern float clocktime;
#define INFINITY 999

extern void tolayer2(struct rtpkt packet);
static void printdt(struct distance_table *dtptr);

/* 节点的直接开销，由宏定义 */
static int connectcosts[4] = CONNECTCOSTS;

/* 从本节点到其他节点的最小成本 */
static int mincost[4];

/* 初始化路由表 */
static void rtinit()
{
    int i, j;
    struct rtpkt pkt;

    printf("时间 %.3f：节点%d的rtinit()被调用。\n", clocktime, NODE_ID);

    /* 初始化距离表 */
    for (i = 0; i < 4; i++) {
        for (j = 0; j < 4; j++) {
            dt.costs[i][j] = INFINITY;
        }
    }

    /* 设置自身到各节点的直接成本 */
    for (i = 0; i < 4; i++) {
        dt.costs[i][NODE_ID] = connectcosts[i];
        dt.costs[i][i] = connectcosts[i];
        mincost[i] = connectcosts[i];
    }

    printdt(&dt);

    /* 向直接邻居发送初始路由包 */
    for (i = 0; i < 4; i++) {
        if (i != NODE_ID && connectcosts[i] < INFINITY) {
            pkt.sourceid = NODE_ID;
            pkt.destid = i;
            for (j = 0; j < 4; j++) {
                pkt.mincost[j] = mincost[j];
            }
            tolayer2(pkt);
            printf("节点%d向节点%d发送路由包：mincost = [%d, %d, %d, %d]\n", NODE_ID, i,
                   pkt.mincost[0], pkt.mincost[1], pkt.mincost[2], pkt.mincost[3]);
        }
    }
}

/* 更新路由表 */
static void rtupdate(struct rtpkt *rcvdpkt)
{
    int i, j;
    int src = rcvdpkt->sourceid;
    int updated = 0;

    printf("时间 %.3f：节点%d的rtupdate()被调用。\n", clocktime, NODE_ID);
    printf("节点%d接收到来自节点%d的路由包：mincost = [%d, %d, %d, %d]\n", NODE_ID, src,
           rcvdpkt->mincost[0], rcvdpkt->mincost[1], rcvdpkt->mincost[2], rcvdpkt->mincost[3]);

    /* 更新距离表 */
    for (i = 0; i < 4; i++) {
        int cost = connectcosts[src] + rcvdpkt->mincost[i];
        if (cost > INFINITY) cost = INFINITY;
        if (dt.costs[i][src] != cost) {
            dt.costs[i][src] = cost;
            /* 重新计算到节点i的最小成本 */
            int min = INFINITY;
            for (j = 0; j < 4; j++) {
                if (dt.costs[i][j] < min) {
                    min = dt.costs[i][j];
                }
            }
            if (min != mincost[i]) {
                mincost[i] = min;
                updated = 1;
            }
        }
    }

    printdt(&dt);

    /* 如果最小成本更新了，向邻居发送新的路由包 */
    if (updated) {
        struct rtpkt pkt;
        for (i = 0; i < 4; i++) {
            if (i != NODE_ID && connectcosts[i] < INFINITY) {
                pkt.sourceid = NODE_ID;
                pkt.destid = i;
                for (j = 0; j < 4; j++) {
                    pkt.mincost[j] = mincost[j];
                }
                tolayer2(pkt);
                printf("节点%d向节点%d发送路由包：mincost = [%d, %d, %d, %d]\n", NODE_ID, i,
                       pkt.mincost[0], pkt.mincost[1], pkt.mincost[2], pkt.mincost[3]);
            }
        }
    } else {
        printf("节点%d的距离表未更新。\n", NODE_ID);
    }
}

static void printdt(struct distance_table *dtptr)
{
    printf("                via     \n");
    printf("   D%d |    0    1     2    3 \n", NODE_ID);
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

static void linkhandler(int linkid, int newcost)
{
    int i, j, change;
    int temp[4];
    struct rtpkt pkt;

    connectcosts[linkid] = newcost;

    /* 更新到邻居的直接成本 */
    dt.costs[linkid][linkid] = newcost;

    /* 记录旧的最短路径 */
    for (i = 0; i < 4; i++) {
        temp[i] = dt.costs[i][i];
    }

    /* 重新计算最短路径 */
    change = 0;
    for (i = 0; i < 4; i++) {
        int min = INFINITY;
        for (j = 0; j < 4; j++) {
            int cost = connectcosts[j] + dt.costs[i][j];
            if (cost < min) {
                min = cost;
                mincost[i] = j;
            }
        }
        if (min != dt.costs[i][i]) {
            dt.costs[i][i] = min;
            change = 1;
        }
    }

    /* 如果有更新，发送新的距离向量 */
    if (change) {
        pkt.sourceid = 0;
        for (i = 0; i < 4; i++) {
            pkt.mincost[i] = dt.costs[i][i];
        }
        for (i = 0; i < 4; i++) {
            if (i != 0 && connectcosts[i] != 999) {
                pkt.destid = i;
                tolayer2(pkt);
            }
        }
    }
}


#endif /* NODE_H */