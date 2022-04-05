## test文件
Deutsch
- 4bit_deu_test:存放实验生成的线路,tfc文件,bmp图片
- nbit_deu_test:存放100个随机数据集（例11001010表示平衡函数f(0,1,4,6)=1），优化后的线路（tfc格式）

Grover
- nbit_gro_test:存放100个随机数据集（例10001010表示f(0,4,6)=1为目标元素），优化后的线路（tfc格式）
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
## Blossom:
- jbBlossom.py:调用开花算法
