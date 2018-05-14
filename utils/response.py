#!/usr/bin/env python
# -*- coding:utf-8 -*-


class BaseResponse(object):
    def __init__(self):
        self.code = 0
        self.msg = None
        self.count = None
        self.data = None
        self.error = None

