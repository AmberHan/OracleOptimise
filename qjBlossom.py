# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/2/11 21:40
# !@Author : DongHan Yang
# !@File   : qjBlossom.py
from ctypes import *
from numpy.ctypeslib import ndpointer
import os.path


def get_compare(node, diff):
    N = len(node)
    M = len(diff)
    dllabspath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "qjBlossom.dll"
    dll = CDLL(dllabspath)
    line = c_int * 3
    data_type = line * M
    data = data_type()
    for i in range(M):
        for j in range(3):
            data[i][j] = c_int(diff[i][j])

    dll.show.restype = ndpointer(dtype=c_int, shape=(N,))
    output = dll.show(N, M, data)  # 调用 add 函数
    ret = []
    ret_0 = []
    for i in range(N):
        if output[i] != 0 and node[output[i] - 1] not in ret:
            ret.append(node[i])
            ret.append(node[output[i] - 1])
        elif output[i] == 0:
            ret_0.append(node[i])
    if len(ret_0) > 1:
        print(ret_0)
        print("多个0")
    ret.extend(ret_0)
    # print("匹配：")
    # print(output)
    # print(node)
    # print(ret)
    return ret


def all_xor(lists):
    n = len(lists)
    rets = []
    for i in range(n):
        for j in range(i + 1, n):
            cost = 10 - bin(lists[i] ^ lists[j]).count('1')
            rets.append([i + 1, j + 1, cost])
    return rets


def qj_blossom(new_gates):
    for key, value in new_gates.items():
        if len(value) <= 2:
            continue
        e = all_xor(value)
        # 所有异或为i的进行搭配邻接
        new_value = get_compare(value, e)
        if set(new_gates[key]) == set(new_value):
            # print("same")
            pass
        else:
            print("different")
            print(new_gates[key])
            print(new_value)
        new_gates[key] = new_value


if __name__ == '__main__':
    dd = [[5, 7, 9], [3, 7, 4], [3, 6, 6], [2, 5, 8], [5, 1, 9], [1, 3, 6], [6, 5, 1], [2, 7, 4], [2, 3, 5], [6, 4, 2],
          [7, 1, 5], [5, 4, 4], [4, 1, 3], [5, 3, 9], [7, 6, 4], [2, 1, 3], [4, 3, 9], [6, 2, 7], [4, 2, 8], [6, 1, 10]]

    d = [5, 7, 9, 3, 7, 4, 3, 6, 6, 2, 5, 8, 5, 1, 9, 1, 3, 6, 6, 5, 1, 2, 7, 4, 2, 3, 5, 6, 4, 2, 7, 1, 5, 5, 4, 4, 4,
         1,
         3, 5, 3, 9, 7, 6, 4, 2, 1, 3, 4, 3, 9, 6, 2, 7, 4, 2, 8, 6, 1, 10]
    # qj_km(7, 20, dd)
