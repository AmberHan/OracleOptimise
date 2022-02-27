## test
- 4bit_test:存放实验生成的线路,tfc文件,bmp图片
- nbit_test:存放100个随机数据集
## oracleOptimise.py
主函数入口，n-bit Oracle的优化
## oracle4bitOptimise.py
4bit实验
## mode1.py
模板1优化
## mode2.py
模板2优化
## tfc.py
生成tfc文件
## readWriteTxt.py
读取数据集


### 注意:
因为开花算法只在步骤1中优化效果明显,步骤2之后优化能力降低;大量测试表明能够优化1/8的数据
- jbBlossom.py:使用局部最优，调用开花算法
- qjBlossom.py:使用全局最优，调用开花算法
- qjBlossom.dll:C++生成的开花算法静态文件