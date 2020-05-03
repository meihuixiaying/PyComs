#!/usr/bin/python 
# -*- coding: utf-8 -*-

class ABC(object):

    def foo1(self):
        print("foo1", self)

    def foo2(cls):
        print("foo2", cls)

    @classmethod
    def foo3(cls):
        print("foo3", cls)

    @staticmethod
    def foo4(self):
        print('foo4', self)

    @staticmethod
    def foo5(cls):
        print('foo5', cls)


if __name__ == "__main__":
    # abc = ABC()
    # abc.foo1()
    # ABC.foo1(abc)
    # print('=========')
    # abc.foo2()
    # print('=========')
    # abc.foo3()
    # abc.foo4(abc)
    # abc.foo5(abc)
    ABC.foo4("xxxx")
    ABC.foo1()
    ABC.foo3()
