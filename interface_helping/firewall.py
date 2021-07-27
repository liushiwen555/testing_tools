from Crypto.Cipher import AES
import random
import requests

CHARSET = [chr(i) for i in range(256)]


class PasswordCipher(object):
    def __init__(self, key):
        self.cipher = AES.new(key, AES.MODE_ECB)

    def encrypt(self, password):
        """
        加密密码组成为: 8位密码 + 8位盐 + 剩余密码 + 随机填充 + 2位密码长度(十进制字符串)
        加密后总位数是32
        :param password:
        :return:
        """
        password_length = len(password)
        if password_length < 8 or password_length > 16:
            raise ValueError('Invalid password.')
        salt = ''.join(random.sample(CHARSET, 8))
        padding_len = 22 - password_length
        padding = ''.join(random.sample(CHARSET, padding_len))
        with_salt = password[:8] + salt + password[8:]
        with_padding = with_salt + padding + '{:02d}'.format(password_length)
        return self.cipher.encrypt(with_padding.encode('latin')).hex()

    def decrypt(self, text):
        with_padding = self.cipher.decrypt(bytes.fromhex(text))
        if len(with_padding) != 32:
            raise ValueError('Invalid password!')
        password_length = int(with_padding[-2:])
        if password_length < 8 or password_length > 16:
            raise ValueError('Invalid password!')
        password = with_padding[:8] + with_padding[16:8+password_length]
        salt = with_padding[8:16]
        return password.decode('latin'), salt


def gbk2312() -> str:
    head = random.randint(0xb0, 0xf7)
    body = random.randint(0xa1, 0xf9)
    val = f'{head:x}{body:x}'
    hans_character = bytes.fromhex(val).decode('gb2312')
    return hans_character


def get_random_rule_name(length: int, **format_case: dict) -> str:
    rule_name = ''
    for i in range(length):
        rule_name += gbk2312()
    return rule_name


def get_random_ip_address_with_mask() -> str:
    ip = ''
    mask = str(random.randint(0, 32))
    for i in range(4):
        ip += str(random.randint(0, 255)) + '.' if i != 3 else str(random.randint(0, 255))
    return ip + '/' + mask


def get_random_ip_address_without_mask() -> str:
    ip = ''
    for i in range(4):
        ip += str(random.randint(0, 255)) + '.' if i != 3 else str(random.randint(0, 255))
    return ip


def get_random_mac_address() -> str:
    mac = ''
    dec_num_list = [str(random.randint(0, 9)) for i in range(10)]
    hex_num_list = [chr(random.randint(65, 70)) for i in range(6)]
    index_list = dec_num_list + hex_num_list
    for i in range(6):
        mac += ''.join(random.choices(index_list, k=2)) + ':' if i != 5 else ''.join(random.choices(index_list, k=2))
    return mac


def login(ss: object) -> object:
    cipher = PasswordCipher('Bl666666666666lB')
    password = cipher.encrypt('theworld!!!')
    login_info = {
        'username': 'test666',
        'password': password
    }
    resp = ss.post('https://{}/v1/user/login/'.format(host), json=login_info, verify=False)
    token_id = resp.json()['token']
    headers = {
        'Authorization': 'Token {}'.format(token_id.upper())
    }
    # ss.add_header('Authorization', 'Token {}'.format(token_id.upper()))
    return ss, headers


def add_basic(ss: object, headers) -> object:
    basic_info = {
        "name": get_random_rule_name(length=random.randint(1, 20)),
        "sip": get_random_ip_address_with_mask(),
        "dip": get_random_ip_address_with_mask(),
        "smac": get_random_mac_address(),
        "sport": str(random.randint(1, 65535)),
        "dport": str(random.randint(1, 65535)),
        "protocol": "TCP",
        "action": "alert",
        "active": 'true'
    }
    resp = ss.post('https://{}/v1/policy/basic/'.format(host), json=basic_info, headers=headers, verify=False)
    return resp


def add_modbus(ss: object, headers: dict) -> object:
    st_address = random.randint(0, 65535)
    ed_address = random.randint(st_address, 65535)
    modbus_info = {
        "name": get_random_rule_name(length=random.randint(1, 20)),
        "function_code": random.randint(1, 2),
        "action": random.choice(['drop', 'reject', 'alert', 'pass']),
        "active": "false",
        "args": {
            "start_address": st_address,
            "end_address": ed_address,
            "length": (ed_address - st_address) + 1,
            "function_code": 1}
    }
    resp = ss.post('https://{}/v1/policy/industry/modbus/'.format(host), json=modbus_info, headers=headers, verify=False)
    return resp


def add_whitelist(ss: object, headers: dict) -> object:
    whitelist_info = {
        "name": get_random_rule_name(length=random.randint(1, 20)),
        "sip": get_random_ip_address_without_mask(),
        "dip": get_random_ip_address_without_mask(),
        "sport": random.randint(1, 65535),
        "dport": random.randint(1, 65535),
        "protocol": random.choice(['TCP', 'UDP']),
        "active": random.choice(['false', 'true'])
    }
    resp = ss.post('https://{}/v1/policy/white/'.format(host), json=whitelist_info, headers=headers, verify=False)
    return resp


def add_session_manage(ss: object, headers: dict) -> object:
    session_rule = {
        "src": get_random_ip_address_without_mask(),
        "dst": get_random_ip_address_without_mask(),
        "speed": random.randint(1, 1000),
        "count": random.randint(0, 10000000),
        "active": random.choice(['true', 'false'])
    }
    resp = ss.post('https://{}/v1/policy/connection/'.format(host), json=session_rule, headers=headers, verify=False)
    return resp


def add_ipbond(ss: object, headers: dict) -> object:
    bond_rule = {
        "name": get_random_rule_name(length=random.randint(1, 20)),
        "ip": get_random_ip_address_without_mask(),
        "mac": get_random_mac_address(),
        "active": random.choice(['true', 'false'])
    }
    resp = ss.post('https://{}/v1/policy/device/'.format(host), json=bond_rule, headers=headers, verify=False)
    return resp


def add_snat(ss: object, headers: dict) -> object:
    snat_rule = {
        "name": get_random_rule_name(length=random.randint(1, 20)),
        "src": random.choice([get_random_ip_address_without_mask(), get_random_ip_address_with_mask()]),
        "dst": get_random_ip_address_without_mask(),
        "active": 'true'
    }
    resp = ss.post('https://{}/v1/policy/nat/snat/'.format(host), json=snat_rule, headers=headers, verify=False)
    return resp

# def get_random_protocol() -> dict:
#     protocol_poll = ['TCP', 'UDP', 'IP', 'ICMP', 'HTTP', 'FTP']
#     protocol_poll = {
#         'TCP': []
#     }


# basic_info = {
#     "name": get_random_rule_name(length=10),
#     "sip": get_random_ip_address_with_mask(),
#     "dip": get_random_ip_address_with_mask(),
#     "smac": get_random_mac_address(),
#     "sport": str(random.randint(1, 65535)),
#     "dport": str(random.randint(1, 65535)),
#     "protocol": "TCP",
#     "action": "alert",
#     "active": 'true'
# }

ss = requests.session()
host = '192.168.1.31'
# for i in range(10):
#     ss, headers = login(ss)
#     resp = add_basic(ss, headers)
#     print(resp.text)

# for i in range(10):
#     ss, headers = login(ss)
#     resp = add_basic(ss, headers)
#     print(resp.text)
# for i in range(10):
#     ss, headers = login(ss)
#     resp = add_whitelist(ss, headers)
#     print(resp.text)
# for i in range(10):
#     ss, headers = login(ss)
#     resp = add_session_manage(ss, headers)
#     print(resp.text)
# for i in range(10):
#     ss, headers = login(ss)
#     resp = add_ipbond(ss, headers)
#     print(resp.text)
for i in range(10):
    ss, headers = login(ss)
    resp = add_snat(ss, headers)
    print(resp.text)
