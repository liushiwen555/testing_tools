#!/usr/bin/python3
from infocollector import InfoCollector
from setting import ROOT_PATH
import json
import time


def test_all(*_except):
    result_dict: dict = {}
    methods = [i for i in dir(InfoCollector) if i.startswith('collect') and i not in _except]
    ic = InfoCollector()
    for i in methods:
        _method = getattr(ic, i)
        result = _method()
        result_dict[i] = result
    
    current_time = time.strftime("%Y_%m_%d-%H-%M-%S", time.localtime(time.time()))

    with open(ROOT_PATH + f'/{current_time}_result.json', mode='w+') as f:
        json.dump(result_dict, f, indent=4)
    f.close()


if __name__ == "__main__":
    test_all('collect_scapy_read_info')
