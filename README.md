# <center>Wang's Algorithm in Python</center>

使用了王浩算法完成了对公式的自动证明

两两检查输入的公式中的项，使用王浩算法中的10条推理规则逐步化简，直至推理出公理或不能推理出公理。程序将在控制台输出所有的推理步骤，不论输入的公式是否正确。

## 使用方法

在控制台中克隆并进入本仓库：

```bash
git clone git@github.com:QDKStorm/Wangs-Algorithm.git
cd Wangs-Algorithm
```

创建适合本项目的环境：

```bash
conda create -n wang python=3.11
conda activate wang
```

