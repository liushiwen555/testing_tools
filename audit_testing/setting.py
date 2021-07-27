import os


SUPPORT_INDUSTRIAL_PROTOCOL = [
    's7comm',
    's7comm-plus',
    'modbus',
    'ams',
    'mms',
    'sv',
    'goose',
    'ge_srtp',
    'fins',
    'dnp3',
    'enip',
    'fox',
    'hart',
    'opcae',
    'opcda',
    'opcua',
    'profinet',
    'umas',
    'iec104',
    'bacnet',
    'cip',
    'egd'
]
SUPPORT_COMMON_PROTOCOL = [
    'arp',
    'ftp',
    'http',
    'icmp',
    'smtp',
    'pop',
    'snmp',
    'telnet'
]
PACKETS_ROOT_PATH = os.path.dirname(__file__) + '/pcaps'

SERVER_LOCATION = 'https://192.168.166.30'

URLs = {
    'login': '/v2/user/login/',
    'protocol_audit': '/v2/packet/'
}
