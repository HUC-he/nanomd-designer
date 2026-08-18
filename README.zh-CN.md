# NanoMD Designer

[![CI](https://github.com/HUC-he/nanomd-designer/actions/workflows/ci.yml/badge.svg)](https://github.com/HUC-he/nanomd-designer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)

**在 Windows 里设计纳米通道分子动力学体系，一键生成可直接运行的 LAMMPS 脚本，哪里都能跑——不用写脚本、不用碰 Linux。**

> English: [README.md](README.md) · 纳米流体 / 电化学界面 / 石墨烯通道 / 流致电势 分子动力学建模工具

NanoMD Designer 是一个开源的、中英双界面桌面 GUI，用于搭建和设置 **纳米流体与电化学界面** 的 [LAMMPS](https://www.lammps.org) 分子动力学（MD）模拟。专为在 Windows 上工作、希望把精力放在科学问题而不是手写 LAMMPS 输入脚本的材料 / 化学 / 物理研究者设计。

**关键词：** 分子动力学 · LAMMPS · 纳米流体 · 石墨烯 · 氧化石墨烯 · 纳米通道 · 流致电势 · 流致电流 · 电动效应 · 电化学界面 · 双电层 · 水脱盐 · 离子输运 · 水伏发电 · MD 建模 · 科学计算 · Python GUI · 开源

## 适用领域（这个工具是给谁用的）

| 领域 | NanoMD Designer 能帮什么 |
|---|---|
| **纳米流体学** | 搭建水填充的石墨烯 / GO 狭缝通道；研究流动、滑移长度、压差驱动下的流致电流 / 流致电势 |
| **电动效应与电化学界面** | 带电碳界面处的双电层结构、离子输运、表面电荷效应 |
| **水处理与膜科学（脱盐）** | 石墨烯 / GO 纳米通道模型，研究水的透过与离子截留 |
| **能源收集（水伏发电）** | 碳纳米通道中流体流动产生的流致电势，服务于水伏发电研究 |
| **二维材料研究** | 官能团化氧化石墨烯（GO），支持 -OH / -COOH / -NH₂ 与氧化度调节 |
| **科研与教学** | 几分钟内从零搭出可运行的 LAMMPS 体系——非常适合 MD 入门的研究生和科研人员 |

## 已实现功能

- **3D 通道建模**：石墨烯 / GO 狭缝通道，氧化度可调，官能团支持 -OH / -COOH / -NH₂
- **水与离子**：TIP3P（默认）/ SPC/E 水；NaCl / KCl / CaCl₂ 浓度可控
- **一键生成 LAMMPS 脚本**：`system.data` + `in.streaming.lammps`，内建重力法（streaming NEMD）模板——y/z 定向控温、`fix addforce`、SHAKE、PPPM、膜固定
- **物理检查**：电荷中性、通道高度、离子统计提示
- **WSL 即用脚本**：生成的输入可直接在 WSL 或任意 Linux 集群运行，含 GPU 参数（`lmp -sf gpu -pk gpu 1`）
- **中英双语界面**，深色 / 浅色主题
- **完全离线、完全开源**：MIT 协议，无云端、无注册

## 路线图

- 一键分析：速度剖面 → 滑移长度 λ、离子通量 → 流致电流 I
- 批量扫描矩阵（系统化参数扫描）
- 环境向导（一键安装 WSL / LAMMPS）
- OVITO 轨迹预览联动
- Windows 一键安装包

## 架构

```
NanoMD Designer（Windows GUI，PySide6 + pyvista）
   │  3D 通道建模 → 力场 → 物理检查
   ▼
生成 system.data + in.streaming.lammps
   │
   ▼
随处可跑：
  WSL / Linux 集群：  lmp -sf gpu -pk gpu 1 -in in.streaming.lammps
```

## 环境要求

- Windows 10/11 + Python 3.10+
- 运行生成的脚本需要一个 LAMMPS 可执行文件（例如 WSL 内或集群上）
- 可选：NVIDIA 独显 + CUDA（GPU 加速运行）

## 安装

```bash
git clone https://github.com/HUC-he/nanomd-designer.git
cd nanomd-designer
python -m venv .venv
.venv\Scripts\pip install -e ".[gui]"
```

启动：

```bash
.venv\Scripts\pythonw -m nanomd.gui.main
```

或直接双击 `scripts/launch_gui.bat`。

## 快速上手

1. 启动 GUI（双击 `scripts/launch_gui.bat` 或桌面快捷方式）；
2. 调整盒子尺寸、壁位置、水模型、盐与浓度；
3. 设氧化度与官能团，构建 GO 通道；
4. 点**构建并预览**查看 3D 体系；
5. 点**生成 LAMMPS 脚本**导出 `system.data` + `in.streaming.lammps`；
6. 在 WSL 里运行：`lmp -sf gpu -pk gpu 1 -in in.streaming.lammps`

## 示例

- `examples/graphene-slit-nacl/` — 纯净石墨烯狭缝 + TIP3P 水 + 0.6 M NaCl（8550 原子）
- `examples/go-oh-10-slit/` — GO-10% 羟基修饰通道（9410 原子）

## 文档

- [用户手册（中文）](docs/zh/README.md) / [User manual (EN)](docs/en/README.md)
- [界面配色规范](docs/design/theme.md)
- [设计与路线图](DESIGN.md)

## 许可证与引用

[MIT](LICENSE) · [CITATION.cff](CITATION.cff)

## 联系

shiyuhe1@163.com
