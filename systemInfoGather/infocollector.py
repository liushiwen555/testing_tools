from utils import run_bash_with_return, format_result_to_dict
from scapy.all import rdpcap
from setting import PCAP_PATH, STRCMP_PATH
from logger import get_logger
import time
import os
import locale
import re


LOGGER = get_logger(__file__)


class InfoCollector():
    def __init__(self):
        self.LANG = locale.getdefaultlocale()[0]

    def collect_cpu_info(self) -> dict:
        cpu_dict: dict = {}
        # static信息
        cpu_static_result = run_bash_with_return('lscpu')
        cpu_static_reg = re.compile(r'(\S+.*)[:|：]\s+(.*)')
        cpu_static_list = re.findall(cpu_static_reg, cpu_static_result)
        try:
            cpu_static_keys = [i[0] for i in cpu_static_list]
            cpu_static_values = [i[1] for i in cpu_static_list]
            cpu_static_dict = dict(zip(cpu_static_keys, cpu_static_values)) if len(cpu_static_keys) == len(cpu_static_values) else None
        except Exception:
            LOGGER.error('collect_cpu_info [slices or dict] error:', exc_info=True)
        cpu_dict['static'] = cpu_static_dict
        # runtime、dynamic信息
        cpu_dynamic_result = run_bash_with_return(r"cat /proc/cpuinfo").split('\n\n')[0]
        cpu_dynamic_reg = re.compile(r'(\S+.*)\t*[:|：]\s*(.*)')
        cpu_dynamic_list = re.findall(cpu_dynamic_reg, cpu_dynamic_result)
        try:
            cpu_dynamic_keys = [i[0].strip('\t') for i in cpu_dynamic_list]
            cpu_dynamic_values = [i[1] for i in cpu_dynamic_list]
            cpu_dynamic_dict = dict(zip(cpu_dynamic_keys, cpu_dynamic_values)) if len(cpu_dynamic_keys) == len(cpu_dynamic_values) else None
        except Exception:
            LOGGER.error('collect_cpu_info [slices or dict] error:', exc_info=True)
        cpu_dict['dynamic'] = cpu_dynamic_dict
        LOGGER.info(cpu_dict)
        return cpu_dict

    def collect_mem_info(self) -> dict:
        mem_dict: dict = {}
        mem_result = run_bash_with_return('cat /proc/meminfo')
        mem_reg = re.compile(r'(\S+)[:|：]\s+(.*)')
        mem_list = re.findall(mem_reg, mem_result)
        LOGGER.info(mem_list)
        try:
            mem_keys = [i[0] for i in mem_list]
            mem_values = [i[1] for i in mem_list]
        except Exception:
            LOGGER.error('collect_mem_info [slices] error:', exc_info=True)
            return None
        if len(mem_keys) == len(mem_values):
            mem_dict = dict(zip(mem_keys, mem_values))
        LOGGER.info(mem_dict)
        return mem_dict

    def collect_pci_info(self) -> dict:
        pci_dict: dict = {}
        pci_result = run_bash_with_return('lspci')
        pci_reg = re.compile(r'(.*)[:|：]\s{1}(.*)')
        pci_list = re.findall(pci_reg, pci_result)
        LOGGER.info(pci_list)
        try:
            pci_address = [i[0] for i in pci_list]
            pci_des = [i[1] for i in pci_list]
        except Exception:
            LOGGER.error('collect_pci_info [slices] error:', exc_info=True)
            return None
        if len(pci_address) == len(pci_des):
            pci_dict = dict(zip(pci_address, pci_des))
        LOGGER.info(pci_dict)
        return pci_dict

    def collect_disk_info(self) -> dict:
        disk_dict: dict = {}
        disk_result = run_bash_with_return(r"sudo fdisk -s -l|grep '.\{1\}/dev/'")
        size_reg = re.compile(r'(\d+)\s{1}bytes')
        size_of_sector = re.findall(size_reg, disk_result)
        try:
            total_size_bytes = sum([int(i) for i in size_of_sector])
        except Exception:
            LOGGER.error('collect_disk_info [sum function] error:', exc_info=True)
            return None
        total_size_Gb = float('%0.2f' % (total_size_bytes / 1024 / 1024 / 1024))
        disk_dict['TotalSize'] = str(total_size_Gb) + ' GiB'
        LOGGER.info(disk_dict)
        return disk_dict

    def collect_cpu_bench(self):
        cpu_bench_dict: dict = {}
        threads_nums = [1, 4, 8, 16, 32]
        events_nums = [10000, 30000]
        cpu_max_prime_nums = [40000, 80000]
        for i in range(10):
            bench_item_dict: dict = {}
            threads_num = threads_nums[i // 2]
            events_num = events_nums[i % 2]
            cpu_max_prime_num = cpu_max_prime_nums[i % 2]
            sysbench_cpu_result = run_bash_with_return(f"sysbench --threads={threads_num} --events={events_num} --time=3000 --cpu-max-prime={cpu_max_prime_num} cpu run")
            cpu_speed_reg = re.compile(r'(events per second)[:|：]\s+(\d+\.\d+)')
            general_statistics_reg = re.compile(r'(total\s+.*)[:|：]\s+(\d+\.?\d+s?)')
            latency_reg = re.compile(r'(min|avg|max|95th\s{1}.*|sum)[:|：]\s+(\d+\.\d+)')
            threads_fairness_reg = re.compile(r'(events.*|execution.*)[:|：]\s+(\d+\.\d+\/\d+\.\d+)')
            cpu_speed_result = re.findall(cpu_speed_reg, sysbench_cpu_result)
            general_statistics_result = re.findall(general_statistics_reg, sysbench_cpu_result)
            latency_result = re.findall(latency_reg, sysbench_cpu_result)
            threads_fairness_result = re.findall(threads_fairness_reg, sysbench_cpu_result)
            try:
                cpu_speed_dict = dict(cpu_speed_result)
                general_statistics_dict = dict(general_statistics_result)
                latency_dict = dict(latency_result)
                threads_fairness_dict = dict(threads_fairness_result)
            except Exception:
                LOGGER.error('collect_cpu_bench [dict pack] error:', exc_info=True)
                return None
            bench_item_dict['CPU speed'] = cpu_speed_dict
            bench_item_dict['General statistics'] = general_statistics_dict
            bench_item_dict['Latency (ms)'] = latency_dict
            bench_item_dict['Threads fairness'] = threads_fairness_dict
            cpu_bench_dict[f'Threads({threads_num}) * Events({events_num}) * MaxPrime({cpu_max_prime_num})'] = bench_item_dict
            LOGGER.info(bench_item_dict)
        return cpu_bench_dict

    def collect_mem_bench(self):
        mem_bench_dict: dict = {}
        operations = ["read", 'write']
        modes = ['seq', 'rnd']
        for i in range(4):
            operation = operations[i // 2]
            mode = modes[i % 2]
            bench_item_dict: dict = {}
            sysbench_mem_result = run_bash_with_return(f"sysbench --memory-total-size=200G --memory-oper={operation} --memory-access-mode={mode} --time=3000 memory run")
            mem_speed_reg = re.compile(r'(\d+\.\d+\s+MiB/sec)')
            general_statistics_reg = re.compile(r'(total\s+(?:time|number).*)[:|：]\s+(\d+\.?\d+s?)')
            latency_reg = re.compile(r'(min|avg|max|95th\s{1}.*|sum)[:|：]\s+(\d+\.\d+)')
            threads_fairness_reg = re.compile(r'(events.*|execution.*)[:|：]\s+(\d+\.\d+\/\d+\.\d+)')
            try:
                mem_speed_result = re.findall(mem_speed_reg, sysbench_mem_result)[0]
            except Exception:
                LOGGER.error('collect_mem_bench [speed extract] error:', exc_info=True)
                return None
            general_statistics_result = re.findall(general_statistics_reg, sysbench_mem_result)
            latency_result = re.findall(latency_reg, sysbench_mem_result)
            threads_fairness_result = re.findall(threads_fairness_reg, sysbench_mem_result)
            try:
                general_statistics_dict = dict(general_statistics_result)
                latency_dict = dict(latency_result)
                threads_fairness_dict = dict(threads_fairness_result)
            except Exception:
                LOGGER.error('collect_mem_bench [dict pack] error:', exc_info=True)
                return None
            bench_item_dict['Memory speed'] = mem_speed_result
            bench_item_dict['General statistics'] = general_statistics_dict
            bench_item_dict['Latency (ms)'] = latency_dict
            bench_item_dict['Threads fairness'] = threads_fairness_dict
            mem_bench_dict[f'Mode({mode}) * Operation({operation})'] = bench_item_dict
            LOGGER.info(bench_item_dict)
        return mem_bench_dict

    def collect_strcmp_info(self):
        strcmp_dict: dict = {}
        strcmp_result = run_bash_with_return(f'gcc strcmp_test.c -o strcmp_test && {STRCMP_PATH}')
        try:
            strcmp_dict = format_result_to_dict(strcmp_result)
        except Exception:
            LOGGER.error(f'collect_strcmp_bench [dict pack] error: bash returns \"{strcmp_result}\"\n', exc_info=True)
            return None
        LOGGER.info(strcmp_result)
        return strcmp_dict

    def collect_scapy_read_info(self):
        start_time = time.time()
        rdpcap(PCAP_PATH)
        end_time = time.time()
        time_cost = end_time - start_time
        fsize_bytes = os.path.getsize(PCAP_PATH)
        fsize_Gb = fsize_bytes / (1024 * 1024 * 1024)
        return {str(round(fsize_Gb, 2)) + ' Gb': str(round(time_cost, 2)) + 's'}


if __name__ == "__main__":
    print(InfoCollector().collect_strcmp_info())
    # InfoCollector().collect_cpu_info()
