'''
 # @ Author: zzsuki
 # @ Create Time: 2020-08-12 06:57:32
 # @ Modified by: zzsuki
 # @ Modified time: 2020-08-12 07:00:19
 # @ Description:
'''
import os
import argparse
from setting import SUPPORT_COMMON_PROTOCOL, SUPPORT_INDUSTRIAL_PROTOCOL, PACKETS_ROOT_PATH

BASH_PATH = os.path.dirname(__file__)


def run_bash(cmd: str, sudo_flags: bool = True, output: bool = False):
    if sudo_flags:
        os.system('sudo {} {}'.format(cmd, '' if output else '>/dev/null 2>&1'))
    else:
        os.system('{} {}'.format(cmd, '' if output else '>/dev/null 2>&1'))


def send_packet():
    parser = argparse.ArgumentParser(description='send specific protocol')
    # group = parser.add_mutually_exclusive_group()
    parser.add_argument('-i', '--interface', type=str, help='网口名称', required=True)
    parser.add_argument('-p', '--pps', type=int, default=10, help='每秒发包')
    parser.add_argument('-P', '--protocol', default='all', type=str, help='协议类型')
    parser.add_argument('-L', '--loop', type=int, default=5, help='文件循环次数')
    parser.add_argument('-l', '--limit', type=int, default=50, help='帧数量限制')
    args = parser.parse_args()
    print('[+]:', args)
    if args.protocol != 'all':
        pcap_path = '{}/ics/{}/{}.pcap'.format(PACKETS_ROOT_PATH, args.protocol, args.protocol) if args.protocol in SUPPORT_INDUSTRIAL_PROTOCOL else '{}/{}/{}.pcap'.format(PACKETS_ROOT_PATH, args.protocol, args.protocol)
        cmd = '/bin/bash {}/bash/send_packet.sh {} {} {} {} {}'.format(BASH_PATH, args.interface, args.pps, args.loop, args.limit, pcap_path)
        run_bash(cmd)
    else:
        try:
            for industrial_protocol in SUPPORT_INDUSTRIAL_PROTOCOL:
                print('\n[+]: Current Sending {}'.format(industrial_protocol))
                pcap_path = '{}/ics/{}/{}.pcap'.format(PACKETS_ROOT_PATH, industrial_protocol, industrial_protocol)
                cmd = '/bin/bash {}/bash/send_packet.sh {} {} {} {} {}'.format(BASH_PATH, args.interface, args.pps, args.loop, args.limit, pcap_path)
                run_bash(cmd)
                print('[+]: {} Sending Finished'.format(industrial_protocol))
            for common_protocol in SUPPORT_COMMON_PROTOCOL:
                print('\n[+]: Current Sending {}'.format(common_protocol))
                pcap_path = '{}/{}/{}.pcap'.format(PACKETS_ROOT_PATH, common_protocol, common_protocol)
                cmd = '/bin/bash {}/bash/send_packet.sh {} {} {} {} {}'.format(BASH_PATH, args.interface, args.pps, args.loop, args.limit, pcap_path)
                run_bash(cmd)
                print('[+]: {} Sending Finished'.format(common_protocol))
        except Exception as e:
            print(e)
    print('\n[+]: Finished')
