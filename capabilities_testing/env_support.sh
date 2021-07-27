#!/bin/bash
if [ $EUID != 0 ]; then
    echo "This script must be run as root, use sudo $0 instead" 1>&2
    exit 1
fi

set -ex

# Python 3.6.9安装
# 可能影响python3编译结果的库
apt install gcc make zlib1g-dev
# 某些第三方库需要的库
apt install libbz2-dev
apt install libsqlite3-dev
apt install python3-dev libxml2-dev libffi-dev libssl-dev libxslt1-dev
# 开始安装
wget https://www.python.org/ftp/python/3.6.9/Python-3.6.9.tgz
tar -zxvf Python-3.6.9.tgz
cd Python-3.6.9
# 开始编译
./configure --with-ssl
make
make install
# 与python3有关的支持
apt install -y python3-venv python3-dev build-essential

# postgresql 10.1安装
wget https://ftp.postgresql.org/pub/source/v10.1/postgresql-10.1.tar.gz
tar -zxvf postgresql-10.1.tar.gz
cd postgresql-10.1

# sysbench源码安装
apt install -y make automake libtool pkg-config libaio-dev
# # mysql support
# apt install -y libmysqlclient-dev libssl-dev
# # postgres support
# apt install -y libpq-dev