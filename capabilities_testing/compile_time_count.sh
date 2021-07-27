#!/bin/bash
start_time = date "+%Y-%m-%d %H:%M:%S"
# 考虑到实际的很多设备核心可能不多，所以采用4线程竞争做
# make -j 4
end_time = date "+%Y-%m-%d %H:%M:%S"
time_cost = end_time - start_time