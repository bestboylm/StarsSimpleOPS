#!/bin/bash
# Description: 安装pyenv

install_pyenv(){
    install_dir='/usr/local/pyenv'
    python_version='3.6.1'

    yum install -y epel-release git gcc zlib zlib-devel readline readline-devel readline-static \
    openssl openssl-devel openssl-static bzip2-devel bzip2-libs sqlite-devel
    [ -d ${install_dir} ] || git clone git://github.com/yyuu/pyenv.git ${install_dir}
    
    echo 'export PYENV_ROOT="/usr/local/pyenv"' > /etc/profile.d/pyenv.sh 
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> /etc/profile.d/pyenv.sh 
    echo 'eval "$(pyenv init -)"' >> /etc/profile.d/pyenv.sh 
    source  /etc/profile.d/pyenv.sh > /dev/null 2>&1
    
    pyenv versions || echo "未成功安装, 请尝试重新执行" ;exit 1
    pyenv install ${python_version} || echo "可能缺少依赖"
    pyenv rehash
    pyenv versions
    echo -e "\033[36m 安装成功. \033[0m"
}


install_pyenv
