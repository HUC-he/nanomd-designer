# NanoMD Designer

[![CI](https://github.com/HUC-he/nanomd-designer/actions/workflows/ci.yml/badge.svg)](https://github.com/HUC-he/nanomd-designer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)

**在 Windows 里设计纳米通道 MD 体系、一键丢进 WSL 跑、再把结果拿回 Windows——全程不用碰终端。**

NanoMD Designer 是一个开源的、中英双界面桌面 GUI，面向使用 [LAMMPS](https://www.lammps.org) 做纳米流体 / 电化学界面分子动力学模拟的材料与化学方向研究者，尤其是"不会编程、不懂 Linux"的 Windows 用户。

## 功能

- **3D 通道建模**：狭缝石墨烯 / GO 通道，氧化度与官能团（-OH / -COOH / -NH₂）可调
- **水与离子**：TIP3P（默认）与 SPC/E 水模型；NaCl / KCl / CaCl₂ 与浓度控制
- **一键生成输入**：LAMMPS `data` + `in` 文件，内建重力法（streaming NEMD）模板——y/z 定向控温、`fix addforce`、SHAKE、PPPM
- **物理校验器**：通道高度、离子统计、电中性、流速区间等新手友好提示
- **WSL 桥接**：自动检测 WSL / LAMMPS / GPU，同步任务文件、运行、日志实时回传、结果拷回 Windows 输出目录
- **一键分析**：速度剖面 → 滑移长度 λ、离子通量 → 流致电流 I、密度剖面 → 表面电荷 σ、泊松积分 → 流致电势 V
- **批量扫描**：参数矩阵（5 ns 筛选 → 20 ns 生产）、断点续跑、灵敏度排序图
- **中英双语界面**，深色 / 浅色主题

## 架构

```
Windows GUI (PySide6)  --生成-->  工程文件
     |  wsl.exe 自动同步               |
     +--------------------------------+
WSL 后端: run_job.sh -> lmp（可选 GPU）
     |  stdout 经 tee 实时回传
Windows GUI: 实时进度 / thermo 图 / 分析 / OVITO
```

用户全程不需要打开命令行；同时保留"仅导出脚本"模式，供进阶用户拷到远程集群运行。

## 环境要求

- Windows 10/11 + WSL2 + Linux 发行版（推荐 Ubuntu 24.04）
- WSL 内装有 LAMMPS——内置**环境向导**可一键安装 conda CPU 版（检测到 CUDA 时引导 GPU 编译版）
- 可选：NVIDIA 独显 + CUDA（GPU 加速）、packmol（更优的水填充）、OVITO（轨迹查看）

## 安装（开发模式）

```bash
pip install -e ".[gui,analysis,dev]"
```

运行：

```bash
nanomd       # 命令行（headless）
nanomd-gui   # 图形界面
```

正式用户的 Windows 一键安装包将在后续版本提供。

## 快速上手

1. 启动 `nanomd-gui`，环境向导检查 WSL / LAMMPS / GPU；
2. 新建工程，选模板（如"石墨烯狭缝 1 nm + TIP3P + 0.6 M NaCl"）；
3. 3D 里调好几何，点**生成并运行**；
4. 实时看 thermo 曲线，跑完一键分析导出论文图。

## 文档

- [用户手册（中文）](docs/zh/README.md) / [User manual (EN)](docs/en/README.md)
- [界面配色规范](docs/design/theme.md)
- [设计与路线图](DESIGN.md)

## 许可证

[MIT](LICENSE)

## 联系

shiyuhe1@163.com

## 引用

如果在研究中使用本软件，请按 [CITATION.cff](CITATION.cff) 引用。
