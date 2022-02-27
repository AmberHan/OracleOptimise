# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/1/26 9:13
# !@Author : DongHan Yang
# !@File   : tfc.py
class Tfc:
    def __init__(self, n, gates, name):
        control = []
        self.name = name
        for i in range(n - 1, -1, -1):
            cline = "c" + str(i)
            control.append(cline)
        control.append("t")
        self.control = control
        self.txt = self.writeTop()
        self.writeTfc(gates)

    def writeTfc(self, gates):
        end = "END"
        txt = self.writeGates(gates)
        txt += end
        self.txt += txt
        file = f"./test/{self.name}.tfc"
        fo = open(file, "w")
        fo.write(self.txt)
        fo.close()

    def writeGates(self, gates):
        txt = ""
        for key, values in gates.items():
            # 确定门，根据控制点个数
            for value in values:
                notKey = self.getNotKey(key, value)
                controlList = self.getMctList(key, notKey)
                mct = "t" + str(bin(key).count('1') + 1) + " " + ",".join(controlList) + ",t\n"
                txt = txt + mct
        return txt

    # key:   1100 0011 （所有点）
    # key1:  1000 0001 （负点）
    # out:   MCT
    def getMctList(self, key1, key2):
        index = 0
        contrList = []
        control = self.control
        ckey = key1
        while key1:
            if key1 % 2 == 1:
                if key2 % 2 == 0:  # 负
                    contrList.append(control[index])
                else:
                    contrList.append(control[index] + "'")
            index += 1
            key1 >>= 1
            key2 >>= 1
        if len(contrList) != bin(ckey).count('1'):
            print("False")
        return contrList

    def writeGates1(self, gates):
        txt = ""
        for key, values in gates.items():
            # 确定门，根据控制点个数
            controlList = self.getControlList(key)
            mct = "t" + str(bin(key).count('1') + 1) + " " + ",".join(controlList) + ",t\n"
            for value in values:
                notKey = self.getNotKey(key, value)
                notList = self.getControlList(notKey)
                notStr = self.setNot(notList)
                notTxt = "\n".join(notStr)
                txt = txt + notTxt + "\n" + mct + notTxt + "\n"
        return txt

    # key:   1010 1100
    # value: 0 1  00
    # out:   1000 1100; 1标记当前位置为负
    # 获取当前为负控制点
    def getNotKey(self, key, value):
        ckey = key
        while ckey:
            last_key_one = ckey & (-ckey)  # 获取最后一个1
            if value % 2 == 1:  # 正数
                key ^= last_key_one
            value >>= 1  # 去除最低位
            ckey &= (ckey - 1)  # 清除最后一个1
        return key

    # 输出 ["t1 x1", "t1 x2"...]
    def setNot(self, notList):
        notStrList = []
        for str in notList:
            notStrList.append("t1 " + str)
        return notStrList

    def setNotState(self):
        pass

    # 获取key对应的控制点位置
    def getControlList(self, key):
        index = 0
        contrList = []
        control = self.control
        ckey = key
        while key:
            if key % 2 == 1:
                contrList.append(control[index])
            index += 1
            key >>= 1
        if len(contrList) != bin(ckey).count('1'):
            print("False")
        return contrList

    def writeTop(self):
        str = ",".join(self.control)
        v = ".v " + str + "\n"
        i = ".i " + str + "\n"
        o = ".o " + str + "\n"
        begin = "BEGIN\n"
        top = v + i + o + begin
        return top


if __name__ == '__main__':
    gates = {14: [0]}
    t = Tfc(4, gates, "test")
    print(t.txt)
