```log
(base) PS D:\Projects\Networking\control_plane> .\prog3.exe
Enter TRACE:2

At time t=0.000, rtinit0() called
Initial distance table at node 0:
                via     
   D0 |    1     2    3 
  ----|-----------------
     1|    1   999   999
dest 2|  999     3   999
     3|  999   999     7
Node 0 sends update to neighbors 1,2,3

At time t=0.000, rtinit1() called
             via   
   D1 |    0     2 
  ----|-----------
     0|    1   999
dest 2|  999     1
     3|  999   999

At time t=0.000, rtinit2() called
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3   999   999
dest 1|  999     1   999
     3|  999   999     2
Node 2 sends update to neighbors 0,1,3

At time t=0.000, rtinit3() called
             via
   D3 |    0     2
  ----|-----------
     0|    7   999
dest 1|  999   999
     2|  999     2
Node 3 sends update to neighbors 0,2
MAIN: rcv event, t=0.094, at 1 src: 0, dest: 1, contents:   0   1   3   7

At time t=0.094, rtupdate1() from node 0
             via
   D1 |    0     2
  ----|-----------
     0|    1   999
dest 2|    4     1
     3|    8   999
MAIN: rcv event, t=0.427, at 1 src: 2, dest: 1, contents:   3   1   0   2

At time t=0.427, rtupdate1() from node 2
             via
   D1 |    0     2
  ----|-----------
     0|    1     4
dest 2|    4     1
     3|    8     3
MAIN: rcv event, t=0.998, at 0 src: 1, dest: 0, contents:   1   0   1 999

At time t=0.998, rtupdate0() called, received packet from node 1
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1   999   999
dest 2|    2     3   999
     3|  999   999     7
Node 0 sends update to neighbors 1,2,3
MAIN: rcv event, t=1.244, at 3 src: 0, dest: 3, contents:   0   1   3   7

At time t=1.244, rtupdate3() from node 0
             via
   D3 |    0     2
  ----|-----------
     0|    7   999
dest 1|    8   999
     2|   10     2
Node 3 sends update to neighbors 0,2
MAIN: rcv event, t=1.514, at 2 src: 0, dest: 2, contents:   0   1   3   7

At time t=1.514, rtupdate2() from node 0
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3   999   999
dest 1|    4     1   999
     3|   10   999     2
Node 2 sends update to neighbors 0,1,3
MAIN: rcv event, t=1.685, at 0 src: 2, dest: 0, contents:   3   1   0   2

At time t=1.685, rtupdate0() called, received packet from node 2
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4   999
dest 2|    2     3   999
     3|  999     5     7
Node 0 sends update to neighbors 1,2,3
MAIN: rcv event, t=2.171, at 3 src: 2, dest: 3, contents:   3   1   0   2

At time t=2.171, rtupdate3() from node 2
             via
   D3 |    0     2
  ----|-----------
     0|    7     5
dest 1|    8     3
     2|   10     2
Node 3 sends update to neighbors 0,2
MAIN: rcv event, t=2.399, at 0 src: 3, dest: 0, contents:   7 999   2   0

At time t=2.399, rtupdate0() called, received packet from node 3
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4   999
dest 2|    2     3     9
     3|  999     5     7
Node 0 sends update to neighbors 1,2,3
MAIN: rcv event, t=2.489, at 0 src: 1, dest: 0, contents:   1   0   1   8

At time t=2.489, rtupdate0() called, received packet from node 1
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4   999
dest 2|    2     3     9
     3|    9     5     7
Node 0 sends update to neighbors 1,2,3
MAIN: rcv event, t=2.667, at 2 src: 1, dest: 2, contents:   1   0   1 999

At time t=2.667, rtupdate2() from node 1
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2   999
dest 1|    4     1   999
     3|   10   999     2
Node 2 sends update to neighbors 0,1,3
MAIN: rcv event, t=2.823, at 1 src: 0, dest: 1, contents:   0   1   2   7

At time t=2.823, rtupdate1() from node 0
             via
   D1 |    0     2
  ----|-----------
     0|    1     4
dest 2|    3     1
     3|    8     3
MAIN: rcv event, t=3.242, at 1 src: 2, dest: 1, contents:   3   1   0   2

At time t=3.242, rtupdate1() from node 2
             via
   D1 |    0     2
  ----|-----------
     0|    1     4
dest 2|    3     1
     3|    8     3
MAIN: rcv event, t=3.361, at 0 src: 1, dest: 0, contents:   1   0   1   3

At time t=3.361, rtupdate0() called, received packet from node 1
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4   999
dest 2|    2     3     9
     3|    4     5     7
Node 0 sends update to neighbors 1,2,3
MAIN: rcv event, t=3.780, at 3 src: 0, dest: 3, contents:   0   1   2   7

At time t=3.780, rtupdate3() from node 0
             via
   D3 |    0     2
  ----|-----------
     0|    7     5
dest 1|    8     3
     2|    9     2
Node 3 sends update to neighbors 0,2
MAIN: rcv event, t=3.798, at 2 src: 3, dest: 2, contents:   7 999   2   0

At time t=3.798, rtupdate2() from node 3
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     9
dest 1|    4     1   999
     3|   10   999     2
Node 2 sends update to neighbors 0,1,3
MAIN: rcv event, t=3.915, at 0 src: 3, dest: 0, contents:   7   8   2   0

At time t=3.915, rtupdate0() called, received packet from node 3
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    15
dest 2|    2     3     9
     3|    4     5     7
Node 0 sends update to neighbors 1,2,3
MAIN: rcv event, t=4.774, at 2 src: 1, dest: 2, contents:   1   0   1   8

At time t=4.774, rtupdate2() from node 1
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     9
dest 1|    4     1   999
     3|   10     9     2
Node 2 sends update to neighbors 0,1,3
MAIN: rcv event, t=4.967, at 1 src: 0, dest: 1, contents:   0   1   2   5

At time t=4.967, rtupdate1() from node 0
             via
   D1 |    0     2
  ----|-----------
     0|    1     4
dest 2|    3     1
     3|    6     3
MAIN: rcv event, t=5.190, at 0 src: 2, dest: 0, contents:   3   1   0   2

At time t=5.190, rtupdate0() called, received packet from node 2
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    15
dest 2|    2     3     9
     3|    4     5     7
Distance table unchanged
MAIN: rcv event, t=5.464, at 3 src: 2, dest: 3, contents:   3   1   0   2

At time t=5.464, rtupdate3() from node 2
             via
   D3 |    0     2
  ----|-----------
     0|    7     5
dest 1|    8     3
     2|    9     2
Distance table unchanged
MAIN: rcv event, t=5.742, at 0 src: 3, dest: 0, contents:   5   3   2   0

At time t=5.742, rtupdate0() called, received packet from node 3
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    10
dest 2|    2     3     9
     3|    4     5     7
Node 0 sends update to neighbors 1,2,3
MAIN: rcv event, t=5.755, at 0 src: 2, dest: 0, contents:   2   1   0   2

At time t=5.755, rtupdate0() called, received packet from node 2
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    10
dest 2|    2     3     9
     3|    4     5     7
Distance table unchanged
MAIN: rcv event, t=5.760, at 2 src: 1, dest: 2, contents:   1   0   1   3

At time t=5.760, rtupdate2() from node 1
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     9
dest 1|    4     1   999
     3|   10     4     2
Node 2 sends update to neighbors 0,1,3
MAIN: rcv event, t=6.259, at 3 src: 0, dest: 3, contents:   0   1   2   5

At time t=6.259, rtupdate3() from node 0
             via
   D3 |    0     2
  ----|-----------
     0|    7     5
dest 1|    8     3
     2|    9     2
Distance table unchanged
MAIN: rcv event, t=6.529, at 1 src: 0, dest: 1, contents:   0   1   2   5

At time t=6.529, rtupdate1() from node 0
             via
   D1 |    0     2
  ----|-----------
     0|    1     4
dest 2|    3     1
     3|    6     3
MAIN: rcv event, t=6.771, at 2 src: 0, dest: 2, contents:   0   1   2   7

At time t=6.771, rtupdate2() from node 0
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     9
dest 1|    4     1   999
     3|   10     4     2
Distance table unchanged
MAIN: rcv event, t=6.947, at 3 src: 0, dest: 3, contents:   0   1   2   5

At time t=6.947, rtupdate3() from node 0
             via
   D3 |    0     2
  ----|-----------
     0|    7     5
dest 1|    8     3
     2|    9     2
Distance table unchanged
MAIN: rcv event, t=7.501, at 1 src: 0, dest: 1, contents:   0   1   2   5

At time t=7.501, rtupdate1() from node 0
             via
   D1 |    0     2
  ----|-----------
     0|    1     4
dest 2|    3     1
     3|    6     3
MAIN: rcv event, t=7.607, at 0 src: 1, dest: 0, contents:   1   0   1   3

At time t=7.607, rtupdate0() called, received packet from node 1
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    10
dest 2|    2     3     9
     3|    4     5     7
Distance table unchanged
MAIN: rcv event, t=7.613, at 3 src: 0, dest: 3, contents:   0   1   2   5

At time t=7.613, rtupdate3() from node 0
             via
   D3 |    0     2
  ----|-----------
     0|    7     5
dest 1|    8     3
     2|    9     2
Distance table unchanged
MAIN: rcv event, t=7.650, at 2 src: 3, dest: 2, contents:   7   8   2   0

At time t=7.650, rtupdate2() from node 3
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     9
dest 1|    4     1    10
     3|   10     4     2
Node 2 sends update to neighbors 0,1,3
MAIN: rcv event, t=8.631, at 1 src: 2, dest: 1, contents:   2   1   0   2

At time t=8.631, rtupdate1() from node 2
             via
   D1 |    0     2
  ----|-----------
     0|    1     3
dest 2|    3     1
     3|    6     3
MAIN: rcv event, t=8.713, at 3 src: 2, dest: 3, contents:   2   1   0   2

At time t=8.713, rtupdate3() from node 2
             via
   D3 |    0     2
  ----|-----------
     0|    7     4
dest 1|    8     3
     2|    9     2
Node 3 sends update to neighbors 0,2
MAIN: rcv event, t=8.714, at 3 src: 0, dest: 3, contents:   0   1   2   4

At time t=8.714, rtupdate3() from node 0
             via
   D3 |    0     2
  ----|-----------
     0|    7     4
dest 1|    8     3
     2|    9     2
Distance table unchanged
MAIN: rcv event, t=8.897, at 1 src: 0, dest: 1, contents:   0   1   2   4

At time t=8.897, rtupdate1() from node 0
             via
   D1 |    0     2
  ----|-----------
     0|    1     3
dest 2|    3     1
     3|    5     3
MAIN: rcv event, t=8.958, at 2 src: 0, dest: 2, contents:   0   1   2   5

At time t=8.958, rtupdate2() from node 0
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     9
dest 1|    4     1    10
     3|    8     4     2
Node 2 sends update to neighbors 0,1,3
MAIN: rcv event, t=9.381, at 1 src: 2, dest: 1, contents:   2   1   0   2

At time t=9.381, rtupdate1() from node 2
             via
   D1 |    0     2
  ----|-----------
     0|    1     3
dest 2|    3     1
     3|    5     3
MAIN: rcv event, t=9.529, at 0 src: 3, dest: 0, contents:   5   3   2   0

At time t=9.529, rtupdate0() called, received packet from node 3
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    10
dest 2|    2     3     9
     3|    4     5     7
Distance table unchanged
MAIN: rcv event, t=9.809, at 2 src: 3, dest: 2, contents:   5   3   2   0

At time t=9.809, rtupdate2() from node 3
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     7
dest 1|    4     1     5
     3|    8     4     2
Node 2 sends update to neighbors 0,1,3
MAIN: rcv event, t=10.058, at 0 src: 2, dest: 0, contents:   2   1   0   2

At time t=10.058, rtupdate0() called, received packet from node 2
Current distance table at node 0:
                via     
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    10
dest 2|    2     3     9
     3|    4     5     7
Distance table unchanged
MAIN: rcv event, t=10.212, at 3 src: 2, dest: 3, contents:   2   1   0   2

At time t=10.212, rtupdate3() from node 2
             via
   D3 |    0     2
  ----|-----------
     0|    7     4
dest 1|    8     3
     2|    9     2
Distance table unchanged
MAIN: rcv event, t=10.448, at 2 src: 0, dest: 2, contents:   0   1   2   5

At time t=10.448, rtupdate2() from node 0
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     7
dest 1|    4     1     5
     3|    8     4     2
Distance table unchanged
MAIN: rcv event, t=11.154, at 1 src: 0, dest: 1, contents:   0   1   2   4

At time t=11.154, rtupdate1() from node 0
             via
   D1 |    0     2
  ----|-----------
     0|    1     3
dest 2|    3     1
     3|    5     3
MAIN: rcv event, t=11.358, at 1 src: 2, dest: 1, contents:   2   1   0   2

At time t=11.358, rtupdate1() from node 2
             via
   D1 |    0     2
  ----|-----------
     0|    1     3
dest 2|    3     1
     3|    5     3
MAIN: rcv event, t=11.418, at 1 src: 0, dest: 1, contents:   0   1   2   4

At time t=11.418, rtupdate1() from node 0
             via
   D1 |    0     2
  ----|-----------
     0|    1     3
dest 2|    3     1
     3|    5     3
MAIN: rcv event, t=11.431, at 3 src: 0, dest: 3, contents:   0   1   2   4

At time t=11.431, rtupdate3() from node 0
             via
   D3 |    0     2
  ----|-----------
     0|    7     4
dest 1|    8     3
     2|    9     2
Distance table unchanged
MAIN: rcv event, t=11.462, at 2 src: 0, dest: 2, contents:   0   1   2   5

At time t=11.462, rtupdate2() from node 0
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     7
dest 1|    4     1     5
     3|    8     4     2
Distance table unchanged
MAIN: rcv event, t=11.648, at 0 src: 2, dest: 0, contents:   2   1   0   2

At time t=11.648, rtupdate0() called, received packet from node 2
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    10
dest 2|    2     3     9
     3|    4     5     7
Distance table unchanged
MAIN: rcv event, t=12.200, at 2 src: 1, dest: 2, contents:   1   0   1   3

At time t=12.200, rtupdate2() from node 1
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     7
dest 1|    4     1     5
     3|    8     4     2
Distance table unchanged
MAIN: rcv event, t=12.598, at 0 src: 1, dest: 0, contents:   1   0   1   3

At time t=12.598, rtupdate0() called, received packet from node 1
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    10
dest 2|    2     3     9
     3|    4     5     7
Distance table unchanged
MAIN: rcv event, t=12.979, at 1 src: 2, dest: 1, contents:   2   1   0   2

At time t=12.979, rtupdate1() from node 2
             via
   D1 |    0     2
  ----|-----------
     0|    1     3
dest 2|    3     1
     3|    5     3
MAIN: rcv event, t=13.343, at 3 src: 2, dest: 3, contents:   2   1   0   2

At time t=13.343, rtupdate3() from node 2
             via
   D3 |    0     2
  ----|-----------
     0|    7     4
dest 1|    8     3
     2|    9     2
Distance table unchanged
MAIN: rcv event, t=13.477, at 2 src: 0, dest: 2, contents:   0   1   2   4

At time t=13.477, rtupdate2() from node 0
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     7
dest 1|    4     1     5
     3|    7     4     2
Node 2 sends update to neighbors 0,1,3
MAIN: rcv event, t=13.727, at 0 src: 2, dest: 0, contents:   2   1   0   2

At time t=13.727, rtupdate0() called, received packet from node 2
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    10
dest 2|    2     3     9
     3|    4     5     7
Distance table unchanged
MAIN: rcv event, t=13.810, at 1 src: 2, dest: 1, contents:   2   1   0   2

At time t=13.810, rtupdate1() from node 2
             via
   D1 |    0     2
  ----|-----------
     0|    1     3
dest 2|    3     1
     3|    5     3
MAIN: rcv event, t=14.233, at 3 src: 0, dest: 3, contents:   0   1   2   4

At time t=14.233, rtupdate3() from node 0
             via
   D3 |    0     2
  ----|-----------
     0|    7     4
dest 1|    8     3
     2|    9     2
Distance table unchanged
MAIN: rcv event, t=14.272, at 2 src: 3, dest: 2, contents:   5   3   2   0

At time t=14.272, rtupdate2() from node 3
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     7
dest 1|    4     1     5
     3|    7     4     2
Distance table unchanged
MAIN: rcv event, t=14.389, at 2 src: 0, dest: 2, contents:   0   1   2   4

At time t=14.389, rtupdate2() from node 0
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     7
dest 1|    4     1     5
     3|    7     4     2
Distance table unchanged
MAIN: rcv event, t=14.516, at 0 src: 2, dest: 0, contents:   2   1   0   2

At time t=14.516, rtupdate0() called, received packet from node 2
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    10
dest 2|    2     3     9
     3|    4     5     7
Distance table unchanged
MAIN: rcv event, t=15.252, at 3 src: 2, dest: 3, contents:   2   1   0   2

At time t=15.252, rtupdate3() from node 2
             via
   D3 |    0     2
  ----|-----------
     0|    7     4
dest 1|    8     3
     2|    9     2
Distance table unchanged
MAIN: rcv event, t=15.509, at 1 src: 2, dest: 1, contents:   2   1   0   2

At time t=15.509, rtupdate1() from node 2
             via
   D1 |    0     2
  ----|-----------
     0|    1     3
dest 2|    3     1
     3|    5     3
MAIN: rcv event, t=15.549, at 3 src: 2, dest: 3, contents:   2   1   0   2

At time t=15.549, rtupdate3() from node 2
             via
   D3 |    0     2
  ----|-----------
     0|    7     4
dest 1|    8     3
     2|    9     2
Distance table unchanged
MAIN: rcv event, t=15.701, at 0 src: 1, dest: 0, contents:   1   0   1   3

At time t=15.701, rtupdate0() called, received packet from node 1
Current distance table at node 0:
                via     
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    10
dest 2|    2     3     9
     3|    4     5     7
Distance table unchanged
MAIN: rcv event, t=15.880, at 0 src: 3, dest: 0, contents:   4   3   2   0

At time t=15.880, rtupdate0() called, received packet from node 3
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    10
dest 2|    2     3     9
     3|    4     5     7
Distance table unchanged
MAIN: rcv event, t=16.308, at 2 src: 1, dest: 2, contents:   1   0   1   3

At time t=16.308, rtupdate2() from node 1
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     7
dest 1|    4     1     5
     3|    7     4     2
Distance table unchanged
MAIN: rcv event, t=16.391, at 1 src: 2, dest: 1, contents:   2   1   0   2

At time t=16.391, rtupdate1() from node 2
             via
   D1 |    0     2
  ----|-----------
     0|    1     3
dest 2|    3     1
     3|    5     3
MAIN: rcv event, t=17.072, at 3 src: 2, dest: 3, contents:   2   1   0   2

At time t=17.072, rtupdate3() from node 2
             via
   D3 |    0     2
  ----|-----------
     0|    7     4
dest 1|    8     3
     2|    9     2
Distance table unchanged
MAIN: rcv event, t=17.411, at 3 src: 2, dest: 3, contents:   2   1   0   2

At time t=17.411, rtupdate3() from node 2
             via
   D3 |    0     2
  ----|-----------
     0|    7     4
dest 1|    8     3
     2|    9     2
Distance table unchanged
MAIN: rcv event, t=17.642, at 3 src: 2, dest: 3, contents:   2   1   0   2

At time t=17.642, rtupdate3() from node 2
             via
   D3 |    0     2
  ----|-----------
     0|    7     4
dest 1|    8     3
     2|    9     2
Distance table unchanged
MAIN: rcv event, t=17.751, at 0 src: 1, dest: 0, contents:   1   0   1   3

At time t=17.751, rtupdate0() called, received packet from node 1
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    10
dest 2|    2     3     9
     3|    4     5     7
Distance table unchanged
MAIN: rcv event, t=17.895, at 2 src: 0, dest: 2, contents:   0   1   2   4

At time t=17.895, rtupdate2() from node 0
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     7
dest 1|    4     1     5
     3|    7     4     2
Distance table unchanged
MAIN: rcv event, t=18.286, at 1 src: 2, dest: 1, contents:   2   1   0   2

At time t=18.286, rtupdate1() from node 2
             via
   D1 |    0     2
  ----|-----------
     0|    1     3
dest 2|    3     1
     3|    5     3
MAIN: rcv event, t=19.386, at 2 src: 1, dest: 2, contents:   1   0   1   3

At time t=19.386, rtupdate2() from node 1
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     7
dest 1|    4     1     5
     3|    7     4     2
Distance table unchanged
MAIN: rcv event, t=19.552, at 0 src: 2, dest: 0, contents:   2   1   0   2

At time t=19.552, rtupdate0() called, received packet from node 2
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    10
dest 2|    2     3     9
     3|    4     5     7
Distance table unchanged
MAIN: rcv event, t=19.966, at 0 src: 2, dest: 0, contents:   2   1   0   2

At time t=19.966, rtupdate0() called, received packet from node 2
Current distance table at node 0:
                via     
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    10
dest 2|    2     3     9
     3|    4     5     7
Distance table unchanged
MAIN: rcv event, t=20.123, at 2 src: 3, dest: 2, contents:   4   3   2   0

At time t=20.123, rtupdate2() from node 3
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     6
dest 1|    4     1     5
     3|    7     4     2
Node 2 sends update to neighbors 0,1,3
MAIN: rcv event, t=20.348, at 3 src: 2, dest: 3, contents:   2   1   0   2

At time t=20.348, rtupdate3() from node 2
             via
   D3 |    0     2
  ----|-----------
     0|    7     4
dest 1|    8     3
     2|    9     2
Distance table unchanged
MAIN: rcv event, t=20.362, at 1 src: 2, dest: 1, contents:   2   1   0   2

At time t=20.362, rtupdate1() from node 2
             via
   D1 |    0     2
  ----|-----------
     0|    1     3
dest 2|    3     1
     3|    5     3
MAIN: rcv event, t=21.166, at 2 src: 1, dest: 2, contents:   1   0   1   3

At time t=21.166, rtupdate2() from node 1
                via
   D2 |    0     1    3
  ----|-----------------
     0|    3     2     6
dest 1|    4     1     5
     3|    7     4     2
Distance table unchanged
MAIN: rcv event, t=21.491, at 0 src: 2, dest: 0, contents:   2   1   0   2

At time t=21.491, rtupdate0() called, received packet from node 2
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    10
dest 2|    2     3     9
     3|    4     5     7
Distance table unchanged
MAIN: rcv event, t=21.713, at 0 src: 2, dest: 0, contents:   2   1   0   2

At time t=21.713, rtupdate0() called, received packet from node 2
Current distance table at node 0:
                via
   D0 |    1     2    3
  ----|-----------------
     1|    1     4    10
dest 2|    2     3     9
     3|    4     5     7
Distance table unchanged

Simulator terminated at t=21.713491, no packets in medium
```


### 节点0的最终距离表
```
   D0 |    1     2    3
  ----|-----------------
     1|    1     3     7    
dest 2|    2     2     6    
     3|    4     4     4    
```
节点0的最小开销值:
- 到节点1: 1 (通过直接链路)
- 到节点2: 2 (通过节点1或2)
- 到节点3: 4 (通过任意邻居)

### 节点1的最终距离表
```
   D1 |    0     2
  ----|-----------
     0|    1     3
dest 2|    3     1
     3|    5     3
```
节点1的最小开销值:
- 到节点0: 1 (通过直接链路)
- 到节点2: 1 (通过直接链路)
- 到节点3: 3 (通过节点2)

### 节点2的最终距离表
```
   D2 |    0     1    3
  ----|-----------------
     0|    2     2     6
dest 1|    3     1     5
     3|    6     4     2
```
节点2的最小开销值:
- 到节点0: 2 (通过节点0或1)
- 到节点1: 1 (通过直接链路)
- 到节点3: 2 (通过直接链路)

### 节点3的最终距离表
```
   D3 |    0     2
  ----|-----------
     0|    4     4
dest 1|    5     3
     2|    6     2
```
节点3的最小开销值:
- 到节点0: 4 (通过节点0或2)
- 到节点1: 3 (通过节点2)  
- 到节点2: 2 (通过直接链路)

