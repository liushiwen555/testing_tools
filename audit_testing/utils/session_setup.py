from requests import session
from setting import URLs, SERVER_LOCATION
from Crypto.Cipher import AES
import random

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


def get_valid_session():
    cipher = PasswordCipher('Bl666666666666lB')
    ss = session()
    # headers = {
    #     'Content-Type': 'application/json'
    # }
    data = {
        'username': 'test666',
        'password': cipher.encrypt('theworld!!!')
    }
    ss.post(url=SERVER_LOCATION + URLs['login'], json=data, verify=False)
    return ss
