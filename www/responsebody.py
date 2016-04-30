# coding=utf-8
from flask import jsonify


class ResponseBody(object):
    def __init__(self,status,body):
        self.content = {'status':status, 'body':body}

    def getContent(self):
        return jsonify(self.content)

    def __str__(self):
        return jsonify(self.content)

    def __call__(self, *args, **kwargs):
        return jsonify(self.content)

    __repr__ = __str__

