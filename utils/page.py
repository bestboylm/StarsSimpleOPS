#!/usr/bin/env python
# -*-encoding:utf-8-*-
# Author: Aaron
# Email: 1121914451@qq.com
# Time: 2018/5/11 19:25

def userList(request, LIST):
    data_dict = {}
    max_data_count = int(request.GET.get('limit'))  #每页最多展示记录条数，可由客户端传值过来
    pg_pagination_number = 11  #页面默认显示的页码个数
    current_page = request.GET.get('page',1)  #获取当前页页码
    current_page = int(current_page)
    start = (current_page-1) * max_data_count
    end = current_page * max_data_count

    data_dict['data'] = LIST[start:end]

    data_dict['count'] = len(LIST) #获取数据记录总个数
    return data_dict