# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/2/26 18:29
# !@Author : DongHan Yang
# !@File   : oracle4bitOptimise.py
# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/1/25 17:03
# !@Author : DongHan Yang
# !@File   : Oracle-4qbit.py
import random
from Blossom.jbBlossom import jb_blossom
from Blossom.qjBlossom import qj_blossom
from tfc import *
from mode1 import mode1
from mode2 import mode2
import copy
import math
from readWriteTxt import *


class Oracle:
    def __init__(self, n, fx, choose, gates=None):
        self.n = n
        if gates is None:
            self.oldGates = self.init(fx)
        else:
            self.oldGates = gates
            # choose = 0
        self.oldgc, self.oldqc = self.calCost(self.oldGates)
        self.midGates = self.oldGates
        self.retGates = {}
        self.optimize1(choose)
        self.gc, self.qc = self.calCost(self.retGates)

    # 设置NOT
    def setNot(self):
        gates = copy.deepcopy(self.retGates)
        for key, values in gates.items():
            if bin(key).count('1') != 1:
                continue
            elif values[0] == 0:
                self.retGates[key][0] = 1
                self.putGates(0, [0], self.retGates)
        self.gc, self.qc = self.calCost(self.retGates)

    # 计算代价
    def calCost(self, gates):
        gc = 0
        qc = 0
        notsnum = 0
        cost0 = [1, 1, 5, 13, 29, 61, 125, 253, 509, 1021]
        cost1 = [1, 1, 5, 13, 29, 52, 80, 100, 128, 152]
        cost2 = [1, 1, 5, 13, 26, 38, 50, 62, 74, 86]
        for key, values in gates.items():
            cNums = bin(key).count('1')
            if self.n - cNums >= cNums - 2:
                if cNums <= 9:
                    vc = cost2[cNums]
                else:
                    vc = 2 ** (cNums + 1) - 3
            elif self.n - cNums >= 1:
                if cNums <= 9:
                    vc = cost1[cNums]
                else:
                    vc = 24 * (cNums + 1) - 88
            else:
                if cNums <= 9:
                    vc = cost0[cNums]
                else:
                    vc = 12 * (cNums + 1) - 34
            for value in values:
                gc += 1
                qc += vc
                if value == 0 and cNums != 0:
                    qc += 1
                    notsnum += 1
        if notsnum == 1:
            qc += 1
        return gc, qc

    # 如01(1)010, 010 对应倒数第2个1取反 -> 01(0)010
    # key:  1100 0101
    # valu1:01    0 1
    # valu2:11    1 1
    # count:10    1 0
    # index:00    1 0
    # outpu:1100 0001
    def get_key(self, key, index):
        c_key = key
        # 找到第2个1
        while index != 1:  # 清除1
            c_key &= (c_key - 1)
            index >>= 1
        new_key = (c_key & (-c_key)) ^ key
        return new_key

    # key: 得到1的数目
    # value:  1010
    # reomve: 0010 移除对应1的
    # output: 10 0
    def get_value(self, key, vaule, romove_value_index):
        count = bin(key).count('1')
        last_index = romove_value_index
        xor_value = (1 << count) - 1
        low = (last_index - 1) & vaule
        high = (vaule >> 1) & (xor_value ^ (last_index - 1))
        return low + high

    # 将key中的x1和x2合并，存入gates
    def merge(self, key, x1, x2):
        gates = self.retGates
        count = x1 ^ x2  # 获取1数目,是对应value的
        # 生成count个门
        while count:
            last_index = count & (-count)  # 获取最后一位1
            # value:二进制中间去掉一个值，得到新的二进制
            y1 = self.get_value(key, x1, last_index)
            # key:对应key的第last_index个1变成0
            new_key = self.get_key(key, last_index)
            # y2 = ((x1 >> 1) & (0b11111111 ^ (last_index - 1))) + ((last_index - 1) & x1)  # 保留last_index前后值，前面右移
            # new_key1 = getValueKey(key, ((1 << bin(key).count('1')) - 1) ^ last_index)
            # print(y1 == y2)
            # print(new_key == new_key1)
            self.putGates(new_key, [y1], gates)
            x1 ^= last_index  # 中间门态
            count &= (count - 1)  # 最后一位1清0

    # 存放门
    def putGates(self, key, valueList, gates):
        for value in valueList:
            if key in gates:
                # 偶数抵消
                if gates[key].count(value):
                    gates[key].remove(value)
                    if len(gates[key]) == 0:
                        del gates[key]
                else:
                    gates[key].append(value)
            else:
                gates[key] = [value]

    # 递归优化
    def optimize1(self, choose):
        gates = self.midGates
        # 最近邻排序
        self.set_choose(choose)
        # 存放新的new_gates
        self.retGates = {}
        is_ret = True
        for key, value in gates.items():
            if len(value) % 2 == 1:  # 奇数最后一位不好处理
                self.putGates(key, [value[-1]], self.retGates)
            # 偶数个
            for i in range(len(value) // 2):
                a, b = value[i * 2], value[2 * i + 1]
                # 超过分解代价高
                if bin(a ^ b).count('1') >= 10:
                    lenv = len(value) if len(value) % 2 == 0 else len(value) - 1
                    self.putGates(key, value[i * 2: lenv], self.retGates)
                    break
                else:
                    is_ret = False
                    self.merge(key, a, b)  # 两两合并
        # print(f'中间生成态',self.retGates)
        if is_ret:
            return
        self.midGates = copy.deepcopy(self.retGates)
        self.optimize1(choose)

    # 初始化，根据fx生成门序列
    def init(self, fx):
        n = self.n
        key = 2 ** n - 1  # 选取的线路
        # print(f"当前长度", len(fx) // 2)
        gates = {key: []}
        for i in range(2 ** n):
            if fx[i] == 1:
                gates[key].append(i)
        # gates = self.my_set()
        print(f'fx：{fx}')
        print(f'初始化的门：{gates[key]}')
        return gates

    def set_choose(self, choose):
        if choose == 1:
            jb_blossom(self.midGates)
        elif choose == 2:
            qj_blossom(self.midGates)

    # 测试，自定义门
    def my_set(self):
        n_gates = {15: [4, 7, 8, 9, 10, 11, 12, 15]}
        self.n = int(math.log2(list(n_gates.keys())[0]))
        return n_gates


def dictEqu(g1, g2):
    for key, value in g1.items():
        if key not in g2:
            return False
        else:
            for v in value:
                if v not in g2[key]:
                    return False
    return True


def myOracle(n, fx, choose):
    gate = Oracle(n, fx, choose)
    Tfc(n, gate.oldGates, "init")
    g = gate.retGates
    # print(gate.oldgc, gate.oldqc)
    Tfc(n, g, "phase1")
    print(f'阶段一局部后：', g)
    print(gate.qc, gate.gc)
    while True:
        gg = copy.deepcopy(g)
        g1 = mode1(g)
        g2 = mode2(g1)
        gate = Oracle(n, 1, choose, g2)
        g = gate.retGates
        if dictEqu(gg, g) and dictEqu(g, gg):
            break
    gate.setNot()
    Tfc(n, g, "phase2")  # Tfc(n, g, "phase2") #
    print(f'阶段二局部后：', g)
    print(gate.qc, gate.gc)


if __name__ == '__main__':
    n = 4
    # 初始化,随机
    fx = [0] * (2 ** (n - 1)) + [1] * (2 ** (n - 1))
    random.shuffle(fx)
    myOracle(n, fx, 0)
    print("*" * 100)
    # t = txt("4bit_test\\" + str(n) + ".txt")
    # fxs = t.readTxt()
    # for fx in fxs:
    #     myOracle(n, fx, 0)
