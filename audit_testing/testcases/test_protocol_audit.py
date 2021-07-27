'''
 # @ Author: zzsuki
 # @ Create Time: 2020-08-12 09:33:56
 # @ Modified by: zzsuki
 # @ Modified time: 2020-08-13 01:33:08
 # @ Description:
'''

from utils.send_packet import Sender
from utils.session_setup import get_valid_session
from setting import SERVER_LOCATION, URLs
# import pytest

class TestProtocolAudit:
    sender = Sender()

    def setup_class(self):
        self.ss = get_valid_session()
        self.result = ''

    def test_s7comm_audit(self):
        # send the packet
        try:
            self.sender.send_specific_protocol('s7comm')
        except Exception as e:
            print(e)
        else:
            print('s7comm sent over..')
        # 查询网络接口检查是否记录
        data = {
            'page': 1,
            'ip': '',
            'mac': '',
            'port': '',
            'l4_protocol': '',
            'protocol': '',
            'ordering': '',
            'start_time': '',
            'end_time': '',
            'page_size': 20
        }
        resp = self.ss.get(url=SERVER_LOCATION + URLs['protocol_audit'], params=data, verify=False)
        print(resp.text)

    # @pytest.fixture(scope='class')
    def teardown_class(self):
        self.ss.close()
