# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/2/27 15:29
# !@Author : DongHan Yang
# !@File   : readWriteTxt.py
import os.path


class txt:
    def __init__(self, name):
        self.name = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "test\\" + name

    def readTxt(self):
        data = []
        with open(self.name, 'r') as f:
            content = f.readlines()
            for c in content:
                c = c.strip('\n')
                dd = list(map(int, c.split(',')))
                data.append(dd)
        f.close()
        # print(data)
        return data

    def writeTxt(self, datas):
        with open(self.name, 'w') as f:
            for data in datas:
                for index in range(len(data)):
                    d = data[index]
                    f.write(str(d))
                    if index != len(data)-1:
                        f.write(',')
                f.write('\n')
        f.close()


if __name__ == '__main__':
    gates = {14: [0]}
    t = txt("test.txt")
    data = [[1, 2, 3], [2, 3, 4]]
    t.writeTxt(data)
    t.readTxt()
