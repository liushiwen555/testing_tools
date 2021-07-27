import subprocess
import itertools
import re
# import json


def run_bash_with_return(cmd: str, shell: bool = True) -> str:
    result_bytes = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE)
    result_str = bytes.decode(result_bytes.communicate()[0]).strip('\n')
    return result_str


def run_bash_without_return(cmd: str, shell: bool = True):
    subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE)


def format_result_to_dict(result: str, split_flag: str = ':', split_max: int = -1) -> dict:
    formated_result: dict = {}
    info_line = [i for i in result.split('\n')]
    # print(info_line)
    info_key = [i.split(split_flag, maxsplit=split_max)[0].strip() for i in info_line]
    info_value = [i.split(split_flag, maxsplit=split_max)[1].strip() for i in info_line]
    if len(info_key) == len(info_value):
        formated_result = dict(zip(info_key, info_value))
    return formated_result


def sysbench_cpu_runner(_threads: int, events: int, cpu_max_prime: int, _time: int = 3000):
    cpu_bench_result = run_bash_with_return("sysbench \
        --threads=%d  \
        --time=%d \
        --events=%d \
        --cpu-max-prime=%d cpu run| \
        awk -F ':' '{if(length($2)!=0) print $0}'" % (_threads, _time, events, cpu_max_prime))
    item_bench_dict = format_result_to_dict(cpu_bench_result)
    print(item_bench_dict)
    i_iter = iter(item_bench_dict.items())
    item_typical_bench_dict = {
        'Test Info': dict(itertools.islice(i_iter, 2)),
        'CPU speed': dict(itertools.islice(i_iter, 1)),
        'General statistics': dict(itertools.islice(i_iter, 2)),
        'Latency (ms)': dict(itertools.islice(i_iter, 5)),
        'Threads fairness': dict(i_iter)
    }
    return item_typical_bench_dict


def sysbench_mem_runner(memory_oper: str, memory_access_mode: str, memory_total_size: float, _time: int = 3000):
    mem_bench_result = run_bash_with_return("sysbench \
        --memory-oper={} \
        --memory-access-mode={} \
        --memory-total-size={}G \
        --time={} memory run \
        ".format(memory_oper, memory_access_mode, memory_total_size, _time))
    # 构造正则
    speed_re = re.compile(r'\d+.\d+\s?MiB/sec')
    dict_re = re.compile(r'.+:.+')
    # 提取速度与其它字典型信息
    speed_in_mib = re.findall(speed_re, mem_bench_result)
    dict_list = re.findall(dict_re, mem_bench_result)
    # 讲字典型信息转换回str以供format方法处理
    mem_bench_result = '\n'.join(dict_list)
    item_bench_dict = format_result_to_dict(mem_bench_result)
    # 将字典序列化，以供切割
    i_iter = iter(item_bench_dict.items())
    # islice是从原有中取得方法，类似与del等操作，会影响变量中实际存储的值
    item_typical_bench_dict = {
        'Test Info': dict(itertools.islice(i_iter, 5)),
        'Mem speed': dict(itertools.islice(i_iter, 1)),
        'General statistics': dict(itertools.islice(i_iter, 2)),
        'Latency (ms)': dict(itertools.islice(i_iter, 5)),
        'Threads fairness': dict(i_iter)
    }
    # MiB单位的速度不是字典形式，因此单独插入
    item_typical_bench_dict['Mem speed']['speed in MiB/s'] = speed_in_mib[0]
    return item_typical_bench_dict
