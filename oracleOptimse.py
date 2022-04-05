# !-*- coding:utf-8 -*-
# !@Time   : 2022/1/25 17:03
# !@Author : DongHan Yang
# !@File   : OracleOptimse.py
import random
from Blossom.jbBlossom import jb_blossom
from Blossom.qjBlossom import qj_blossom
from tfc import *
from mode1 import mode1
from mode2 import mode2
import copy
import math
import time
from readWriteTxt import *


class Oracle:
    def __init__(self, n, fx, choose, gates=None):
        self.n = n
        self.fx2 = []
        if gates is None:
            self.oldGates = self.init(fx)
        else:
            self.oldGates = gates
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
                    vc = 12 * (cNums + 1) - 34
            elif self.n - cNums >= 1:
                if cNums <= 9:
                    vc = cost1[cNums]
                else:
                    vc = 24 * (cNums + 1) - 88
            else:
                if cNums <= 9:
                    vc = cost0[cNums]
                else:
                    vc = 2 ** (cNums + 1) - 3
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
                if bin(a ^ b).count('1') >= 10:  # xg
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
        # print(f'fx：{fx}')
        # print(f'初始化的门：{gates[key]}')
        self.fx2 = gates[key]
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


phase1Gc = 0
phase1Qc = 0
phase2Gc = 0
phase2Qc = 0
OldGc, OldQc, RG, RQ = 0, 0, 0, 0


def myOracle(n, fx, deu_gro, index):
    global phase1Gc, phase1Qc, phase2Gc, phase2Qc
    global OldGc, OldQc
    if deu_gro == 0:
        choose = 0
        pathName = "nbit_deu_test/" + str(n) + '/' + str(index)
    else:
        choose = 2
        pathName = "nbit_gro_test/" + str(n) + '/' + str(index)
    gate = Oracle(n, fx, choose)
    # Tfc(n, gate.oldGates, "init")
    g = gate.retGates
    # Tfc(n, g, "phase1")
    # print(f'阶段一局部后：', g)
    # print(gate.qc, gate.gc)
    phase1Gc += gate.gc
    phase1Qc += gate.qc
    while True:
        gg = copy.deepcopy(g)
        g1 = mode1(g)
        g2 = mode2(g1)
        gate = Oracle(n, 1, choose, g2)
        g = gate.retGates
        if dictEqu(gg, g) and dictEqu(g, gg):
            break
    gate.setNot()
    # Tfc(n, g, "phase2")  # Tfc(n, g, "phase2") #
    # print(f'阶段二局部后：', g)
    # print(gate.qc, gate.gc)
    # Tfc(n, g, pathName) #生成存储的文件
    phase2Gc += gate.gc
    phase2Qc += gate.qc


def Old(n, fx, choose):
    global OldGc, OldQc, RG, RQ
    gate = Oracle(n, fx, choose)
    OldGc += gate.oldgc  # 计算初始化线路代价
    OldQc += gate.oldqc
    RG += gate.gc
    RQ += gate.qc
    # print(OldGc // 100, RG // 100, OldQc // 100, RQ // 100)
    # OldGc, RG, OldQc, RQ = 0, 0, 0, 0


# DJ生成测试集
def deu_generateData(n):
    times = 100
    fxs = []
    while times > 0:
        fx = [0] * (2 ** (n - 1)) + [1] * (2 ** (n - 1))
        random.shuffle(fx)
        if fx not in fxs:
            fxs.append(fx)
        else:
            continue
        # myOracle(n, fx, 0)
        times -= 1
    print(fxs)
    t = txt(str(n) + ".txt")
    t.writeTxt(fxs)


# Grover生成测试集
def gro_generateData(n):
    times = 100
    fxs = []
    while times > 0:
        solutNum = random.randint(2, 2 ** (n - 2))
        otherNum = 2 ** n - solutNum
        fx = [0] * otherNum + [1] * solutNum
        random.shuffle(fx)
        if fx not in fxs:
            fxs.append(fx)
        else:
            continue
        times -= 1
    print(fxs)
    t = txt(str(n) + ".txt")
    t.writeTxt(fxs)


# 生成测试数据
def generateData(deu_gro):
    for i in range(4, 11):
        if deu_gro == 0:
            deu_generateData(i)
        else:
            gro_generateData(i)


if __name__ == '__main__':
    deu_gro = int(input("deut优化（0） or Grover优化(1):"))
    # generateData(deu_gro)  # 生成100组数据
    if deu_gro == 0:
        txtPath = "nbit_deu_test\\"
    else:
        txtPath = "nbit_gro_test\\"
    for n in range(4, 11):
        # 读取数据
        start = time.time()
        t = txt(txtPath + str(n) + ".txt")
        fxs = t.readTxt()
        for index in range(len(fxs)):
            fx = fxs[index]
            myOracle(n, fx, deu_gro, index)
        end = time.time()
        print(str(n) + ":100个测试集平均代价：")
        print(phase1Gc // 100, phase1Qc // 100, phase2Gc // 100, phase2Qc // 100)
        phase1Gc, phase1Qc, phase2Gc, phase2Qc = 0, 0, 0, 0
        useTime = end - start
        print("ET耗时为：%s" % useTime)
        print("*" * 100)
