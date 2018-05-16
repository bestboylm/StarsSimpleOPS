#!/usr/bin/env python
# -*-encoding:utf-8-*-
# Author: Aaron
# Email: 1121914451@qq.com
# Time: 2018/5/16 14:28
# Description: Stars SimpleOps initializtion script
import subprocess, sys, os, shutil

#subprocess.CalledProcessError
django_version = '1.11.7'
py_version = '3.6.1'
web_dir = '/data/wwwroot/'

django_project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
django_project_name = django_project_dir.split('/')[-1]
django_web_dir = os.path.join(web_dir,django_project_name)

if not os.path.isdir(web_dir):
    os.makedirs(web_dir)

if __name__ == "__main__":
    try:
        subprocess.check_call('/bin/bash install_pyenv.sh',shell=True)
    except subprocess.CalledProcessError:
        print('\033[31mError: 执行 pyenv 安装脚本报错，请检查.\n{}\033[0m')
        sys.exit(1)
    except Exception as e:
        print('\033[31mError: 安装pyenv 失败\n{}\033[0m'.format(str(e)))
        sys.exit(1)

    # 拷贝项目目录到规定的web目录
    os.chdir(web_dir)
    if os.path.exists(django_web_dir):
        shutil.move(django_web_dir,django_web_dir+'_backup')
    shutil.move(django_project_dir, web_dir)

    # pyenv安装其他版本python
    os.chdir(django_web_dir)
    subprocess.check_call('source /etc/profile; pyenv install {}'.format(py_version), shell=True)
    subprocess.check_call('pyenv local {}'.format(py_version), shell=True)

    # 安装django
    if django_version:
        subprocess.check_call('pip install django=={}'.format(django_version), shell=True)
    else:
        subprocess.check_call('pip install django', shell=True)

    # 安装启动uwsgi
    subprocess.check_call('pip install uwsgi', shell=True)
    subprocess.check_call('uwsgi --ini  {}/init/etc/uwsgi.ini '.format(django_web_dir, py_version), shell=True)

    # 启动nginx
    shutil.copyfile('./etc/nginx.conf', '/etc/nginx/')
    subprocess.check_call('service nginx restart', shell=True)
    print("""
        初始化完成,请通过IP访问
    """)