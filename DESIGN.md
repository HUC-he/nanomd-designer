# NanoMD Designer — 开源图形化 LAMMPS 设计工具：功能方案（v0.2 草案）

> 状态：待评审。评审通过后按里程碑 M0→M3 实施。
> 运行形态（v0.2 关键变更）：**Windows 原生 GUI + WSL 计算后端桥接**，服务"不会编程、不懂 Linux"的材料方向用户；界面中英双语。
> 关联研究项目：《碳基水伏 MD-技术规格手册》（本工具为该项目服务，功能范围以该手册为准）。

---

## 1. 项目定位

**一句话**：一个面向纳米流体 / 电化学界面 MD 研究的开源桌面工具——在 **Windows 图形界面里完成建模、设参数、生成 LAMMPS 输入，一键丢进 WSL 跑，跑完自动把结果和图表拿回 Windows**。全程不需要用户打开终端、不需要懂 Linux。

- 目标用户：材料 / 化学方向研究生，会用 Windows 软件但不会编程、不会 Linux
- 核心卖点：
  - 3D 建模（石墨烯 / GO 狭缝通道 + TIP3P 水 + 离子）→ 自动生成 data / in
  - 一键在 WSL 里运行（自动检测环境、自动同步文件、实时进度图表）
  - 一键分析（滑移长度 / 流致电流 / 电势）并出论文图
  - 中英双语界面，新手向导式操作
- 非目标（v0.1 不做）：反应性 MD、蛋白质 / 生物体系、通用分子编辑器、云端服务、商业化

---

## 2. 运行架构（Windows ↔ WSL 桥接）

```
Windows 原生 GUI (PySide6，中英双语)
   │ ① 建模 + 力场 + 校验
   │ ② 生成工程文件（data / in / run.sh）
   ▼
Windows 项目目录（用户可见，如 文档/NanoMD 工程/<工程>/jobs/<job>）
   │ ③ 自动同步：wsl cp → ~/nanomd-jobs/<job>（避开 NTFS/中文路径坑）
   ▼
WSL 后端：bash run.sh → lmp -sf gpu -pk gpu 1
   │ ④ stdout 经 tee 实时写回 Windows 可见的 console.log
   ▼
GUI 实时尾部解析 console.log → 进度 / ns-day / thermo 曲线
   │ ⑤ 运行结束，结果（log / dump / csv）自动拷回 Windows 输出目录
   ▼
Windows 侧分析面板出图；一键用 OVITO 打开轨迹；打开输出文件夹
```

要点：
- **一键模式**：点"生成并运行"，上面 ③④⑤ 全自动；小白零命令行。
- **手动模式**（进阶 / 服务器用户）：保留"仅生成脚本"按钮，导出 data / in / run.sh，自己拷到任何 Linux 机器跑。
- **环境向导**：首次使用自动检测 WSL / 发行版 / LAMMPS / GPU / packmol / OVITO，缺什么按向导装（详见 3.6）。

---

## 3. 核心用户流程

1. 打开软件 → 环境向导检测（全绿后进入）
2. 新建工程 → 选模板（如"石墨烯狭缝 1 nm + TIP3P 水 + 0.6 M NaCl"）
3. 3D 里调通道尺寸、材料、官能团
4. 检查力场与物理约束（通俗提示，如"通道太窄，双电层会重叠"）
5. 预览 data / in → 点"生成并运行"
6. 实时看进度和 thermo 曲线
7. 跑完自动分析出图（λ / I / V / σ），一键 OVITO 看轨迹
8. 保存工程 / 加入扫描矩阵

---

## 4. 功能规格

### 4.0 界面与交互（新手向，贯穿全部模块）

| 功能 | 说明 |
|---|---|
| 中英双语 | 跟随 Windows 系统语言，可在设置里随时切换；Qt i18n（.ts/.qm）标准实现 |
| 向导式步骤条 | 主界面顶部步骤：建体系 → 配力场 → 生成 → 运行 → 分析，未完成步骤给红色提示 |
| 模板预设 | 一键模板：基准石墨烯 / GO-10% / GO-30% / 不同孔径等；小白直接选 |
| 通俗错误提示 | 校验不通过用大白话解释（"离子太少，算出来电流噪声会很大"）+ 建议操作 |
| 环境状态栏 | 底部常驻显示 WSL / LAMMPS / GPU 状态灯，缺啥一目了然 |

### 4.1 建模（Modeling）

| 功能 | 说明 | 里程碑 |
|---|---|---|
| 狭缝通道几何 | Lx×Ly×h 参数化，3D 实时预览，膜厚 / 膜位可调 | M1 |
| 石墨烯 / GO 膜 | 氧化度滑块（0/10/30%…）、官能团（-OH/-COOH/-NH₂）、随机或指定分布、单双面修饰 | M2 |
| 水填充 | TIP3P（主）/ SPC/E（备）；按目标密度或分子数填充；内置格子填充 + 可选 packmol 优化 | M1 |
| 离子 | NaCl 默认 + KCl / CaCl₂ 可选；浓度输入；随机分布 + 最小间距检查 + 电中性自动处理 | M1 |
| 组分树 | 左栏列出 壁 / 水 / 离子 / 官能团，可显隐、配色、改参数 | M1 |
| 交互编辑 | 框选、拖拽原子 / 官能团位置（进阶） | M3 |

### 4.2 力场库（Force Field Library）

| 功能 | 说明 |
|---|---|
| 预置参数 | TIP3P、SPC/E、石墨烯 C、GO 官能团（-OH/-COOH/-NH₂）、离子（Na/K/Ca/Cl），参数带出处注释 |
| 多套并存 | 离子参数可多套切换（Aqvist / Dang / 用户自定义），切换时提示混合规则一致性 |
| 可编辑 | 每个原子类型参数可改、可新增自定义力场；改动标"未保存" |
| 一致性校验 | 电中性、混合规则（geometric）、水模型联动（换水模型自动换 O/H 电荷与 σ/ε）、缺失 pair_coeff 高亮 |

> 手册 §3.3 的"待查参数"（K⁺/Ca²⁺/-COOH/-NH₂）已在调研阶段补齐并记录出处，直接入库。

### 4.3 输入生成（Input Generation）

| 功能 | 说明 |
|---|---|
| data 文件 | atom types / masses / charges / bonds（SHAKE 用）/ box 自动生成 |
| in 文件模板 | 内置"平衡 + 生产"两阶段模板：minimize → NVT(y/z 控温) → addforce 驱动生产 |
| 重力法模板 | `compute temp/partial 0 1 1` + `fix_modify`、`fix addforce` 按目标流速自动换算、膜 `fix setforce`、SHAKE、PPPM，全部内建 |
| 模板可改 | 高级用户可编辑模板文本（保存为项目级模板） |
| 生成预览 | 写盘前预览 data / in 全文；工程目录结构用户可见 |
| 导出脚本 | "仅生成脚本"模式：打包 data / in / run.sh，供手动拷到任意 Linux |

### 4.4 校验器（Validator）

| 功能 | 说明 |
|---|---|
| 物理约束检查 | h≥6 Å、离子 ≥20 对、目标流速 0.1~1.0 Å/ps（据此换算 addforce）、体系电中性、边界设置正确；提示用大白话 |
| 力场检查 | 参数完整性、混合规则、水模型与 SHAKE 匹配 |
| 运行错误定位 | 捕获 LAMMPS 报错，高亮出错行 / 参数，并附通俗解释 |

### 4.5 WSL 运行中心（Runner Bridge）

| 功能 | 说明 |
|---|---|
| WSL 自动检测 | `wsl -l -v` 枚举发行版；探测 lmp（常见路径 + 用户自定义），记住到设置 |
| 路径映射 | Windows ↔ WSL 路径自动互转（`C:\...` ↔ `/mnt/c/...`，含空格 / 中文路径处理） |
| 一键同步运行 | 项目 → `~/nanomd-jobs/<job>` 同步 → 执行 → 日志实时回传 → 结果拷回 Windows |
| 实时监控 | 当前步 / 进度 / 性能（ns/day）/ 剩余时间估算；thermo 曲线（温度 / 能量 / 压力 / 流速） |
| 稳态提示 | 检测速度剖面 / 离子通量漂移，提示是否进入生产阶段 |
| 进程控制 | 启动 / 停止 / 继续；断线重连（关软件重开可看到进行中任务） |
| 输出管理 | 运行结束自动打开 Windows 输出目录；一键 OVITO 打开轨迹（优先 Windows 侧 OVITO，无则 WSL 侧） |

### 4.6 环境向导（Environment Wizard，小白刚需）

| 检测项 | 缺了怎么办 |
|---|---|
| WSL 是否启用 | 显示官方启用命令与文档链接（需管理员，无法全自动） |
| 发行版 | `wsl --install -d Ubuntu-24.04` 指引 |
| LAMMPS | 标准模式：一键在 WSL 内跑随仓库发布的 `setup_wsl_env.sh`（conda 装 CPU 版，全自动）；GPU 模式：检测 CUDA / nvcc，走源码编译向导（给出步骤 + 自动执行） |
| GPU 加速 | 检测 `libcuda` / `nvidia-smi`（WSL 内），提示"显卡加速可用 / 仅 CPU" |
| packmol | 可选；缺则用内置格子填充 |
| OVITO | Windows 侧优先，未装则提示下载；或回退 WSL 侧 OVITO / 内置渲染 |

向导输出一个"环境体检报告"（绿 / 黄 / 红），存到设置；每次启动自动复查。

### 4.7 分析（Analysis）

| 功能 | 说明 |
|---|---|
| 速度剖面 → λ | 沿 z 分 bin 平均 v_x(z)，线性外推得滑移长度 |
| 离子通量 → I | 统计单位时间过 x 截面净电荷 → 流致电流 |
| 密度剖面 → σ | 离子 / 水密度剖面、Stern 层峰位与强度、表面电荷 |
| 电荷密度 → V | 泊松积分（方法可插拔：一维泊松 / 补偿电场法，研究方案定稿后锁定默认） |
| 结果输出 | 图表导出 PNG / SVG / CSV；双击打开输出目录；一键 OVITO 看轨迹 |

### 4.8 批量扫描（Scan）

| 功能 | 说明 |
|---|---|
| 矩阵编辑器 | 行 = 体系，列 = 变量（材料 / 氧化度 / 官能团 / 孔径 / 离子 / 浓度 / 温度） |
| 两阶段调度 | 先 5 ns 筛选趋势 → 锁定体系 20 ns 生产 |
| 断点续跑 | 已完成体系跳过；失败体系单独重跑 |
| 结果汇总 | 汇总表 + 灵敏度排序图（各因素对 I / V / λ 的贡献） |

### 4.9 工程文件（Project）

| 功能 | 说明 |
|---|---|
| 工程格式 | JSON（默认）/ YAML 可选：全部设置 + 力场 + 矩阵 + 结果引用 |
| 可复现 | 随机种子、版本号、LAMMPS 版本记录在工程内 |
| 模板 | 工程可存为模板，导入导出 |

---

## 5. 技术栈

| 层 | 选型 | 理由 |
|---|---|---|
| GUI 框架 | PySide6（Windows 原生运行） | 成熟、跨平台；不依赖 WSLg |
| 3D 渲染 | pyvista + pyvistaqt（VTK），备选 pyqtgraph GLViewWidget | 分子渲染成熟；备选更轻量 |
| 图表 | pyqtgraph（实时）+ matplotlib（论文图） | 各司其职 |
| 核心引擎 | numpy / scipy / ase | 几何、晶格、写入 data 文件 |
| 轨迹分析 | MDAnalysis（或 OVITO python 模块） | 读 dump、算剖面 |
| WSL 桥接 | `wsl.exe` subprocess + UNC / tee 日志流 | 零额外服务依赖；stdout 经 tee 实时写回 Windows 可见日志 |
| 填水 | 内置格子填充（必选）+ packmol（可选增强，WSL 侧） | 无外部依赖也能用 |
| i18n | Qt Linguist（.ts / .qm，pyside6-lrelease） | 标准、可扩展其他语言 |
| 配置 / 工程 | JSON / YAML | 可读可 diff |
| 测试 / 质量 | pytest + ruff | CI 标准 |
| 分发（后期） | PyInstaller 打包 Windows 安装包 | 小白不用碰命令行 |

> 开发环境：Windows 上 Python 3.11 + pip 安装以上依赖；WSL 侧需要 LAMMPS（环境向导负责）。本项目开发机（用户机器）已具备 WSL + GPU LAMMPS，可直接联调。

---

## 6. 架构与目录

核心原则：**core 层零 GUI 依赖**（headless 可测）；**WSL 桥接只通过 `wsl.exe` 子进程 + 文件交换**，不依赖任何 WSL 侧服务。

```
nanomd-designer/
├── src/nanomd/
│   ├── core/
│   │   ├── models/       # 体系数据结构（System/Wall/Water/Ions）
│   │   ├── forcefields/  # 参数库（含出处注释）
│   │   ├── builders/     # 石墨烯/GO、水、离子生成
│   │   ├── writers/      # data + in 文件生成
│   │   ├── validator/    # 物理约束检查（通俗提示）
│   │   ├── wsl_bridge/   # 环境检测/路径映射/同步/进程/日志流
│   │   ├── analysis/     # 速度剖面/通量/密度/泊松
│   │   ├── scan/         # 扫描矩阵引擎
│   │   └── project/      # 工程文件读写
│   ├── gui/
│   │   ├── main_window.py
│   │   ├── scene3d.py    # 3D 场景
│   │   ├── wizard/       # 环境向导
│   │   ├── panels/       # 建模/力场/运行/分析/扫描面板
│   │   └── widgets/
│   ├── locales/          # zh_CN.ts / en.ts（Qt i18n）
│   └── cli.py            # 命令行入口（headless 模式）
├── scripts/wsl/          # WSL 侧脚本（随仓库发布）
│   ├── setup_wsl_env.sh  # 环境向导调用：conda + CPU LAMMPS 自动安装
│   ├── run_job.sh        # 运行器调用：同步后执行
│   └── env_check.sh      # 环境检测
├── tests/                # core 单测 + GUI 冒烟（无显示自动跳过）
├── docs/
│   ├── zh/               # 中文文档（用户手册/架构/开发）
│   └── en/
├── examples/             # 基准体系示例工程
├── assets/               # 图标/模板
├── README.md             # 英文
├── README.zh-CN.md       # 中文（顶部互链）
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── CITATION.cff
├── CHANGELOG.md
├── pyproject.toml
└── .github/
    ├── workflows/ci.yml
    └── ISSUE_TEMPLATE/
```

## 7. UI 布局草案

```
┌────────────────────────────────────────────────────────────┐
│ 菜单栏: 文件  编辑  工程  运行  分析  帮助        语言: EN/中  │
├────────────────────────────────────────────────────────────┤
│ 步骤条: ① 建体系 → ② 配力场 → ③ 生成 → ④ 运行 → ⑤ 分析      │
├────────────┬───────────────────────────────────────────────┤
│            │  右侧属性面板:                                 │
│  3D 场景    │    通道尺寸 | 材料 | 官能团 |                  │
│  (壁/水/    │    水模型 | 离子 | 运行配置                   │
│   离子/     ├───────────────────────────────────────────────┤
│   官能团)   │  底部标签页:                                  │
│            │  生成预览 | 运行日志/Thermo图 | 分析结果 | 扫描矩阵 │
│ 左栏: 组分树│                                               │
├────────────┴───────────────────────────────────────────────┤
│ 状态栏: ● WSL 就绪  ● LAMMPS GPU 就绪  ● packmol 可选  环境体检 │
└────────────────────────────────────────────────────────────┘
```

---

## 8. 开源仓库配置清单（M0 交付）

- [ ] **README.md（英文）+ README.zh-CN.md（中文）**：简介、截图、安装、快速上手、功能列表、许可证徽章、引用方式；两种语言顶部互链
- [ ] **LICENSE**：MIT（学术社区最通用）
- [ ] **CONTRIBUTING.md**：开发环境搭建、代码规范（ruff）、测试要求、PR 流程
- [ ] **CODE_OF_CONDUCT.md**
- [ ] **CITATION.cff**：学术引用元数据（发论文后补 DOI）
- [ ] **pyproject.toml**：包名 `nanomd-designer`、依赖、入口 `nanomd` / `nanomd-gui`、构建后端
- [ ] **GitHub Actions CI**：ruff + pytest（core 层，含 WSL 桥接的 mock 测试）+ 安装冒烟；GUI 测试无显示环境自动跳过
- [ ] **.gitignore**：Python / conda / LAMMPS 产物（data、in、log、dump、*.nmd）
- [ ] **scripts/wsl/**：环境检测 + 安装 + 运行脚本
- [ ] **docs/**：用户手册（zh + en）、架构说明、开发指南
- [ ] **examples/**：基准体系示例工程
- [ ] **Issue / PR 模板**
- [ ] **徽章**：license、CI、Python 版本；（发布后）PyPI
- [ ] **CHANGELOG.md** + 语义化版本
- [ ] （v0.1 后）PyPI 发布 + Windows 安装包（PyInstaller）+ Zenodo DOI

---

## 9. 里程碑

### M0 仓库骨架
建仓 + 双语 README / LICENSE / CI / 目录 / pyproject / scripts/wsl 占位 + core 空模块。

### M1 Windows↔WSL 单体系工作台（对应研究手册 Step 1–2）
- Windows 原生 GUI：3D 狭缝通道 + 石墨烯壁 + TIP3P 水 + NaCl
- 力场库 v1（含出处）+ 校验器（通俗提示）
- data / in 生成 + 模板预设
- WSL 桥接：环境检测、一键同步运行、实时 thermo 图、日志回传
- 分析：速度剖面 → λ、离子通量 → I
- **验收**：在一台"没装过任何东西的机器"上，按环境向导装好 WSL + LAMMPS 后，一键生成并跑通基准体系（手册 §2），出 λ / I 图

### M2 功能扩展（对应研究手册 Step 3–4）
- GO 修饰：氧化度 / -OH / -COOH / -NH₂
- 分析：密度剖面 → σ、电荷密度 → V（方法可插拔）
- 扫描矩阵 + 5 ns 筛选批量跑

### M3 生产与分析完善（对应研究手册 Step 5）
- 20 ns 生产管理、断点续跑
- 结果汇总表 + 灵敏度排序图
- OVITO 联动完善、论文出图导出
- 发布 v0.1.0（GitHub Release + PyPI + Windows 安装包）

---

## 10. 待拍板决策

1. **项目名**：默认 `NanoMD Designer`（repo: `nanomd-designer`）。可换。
2. **许可证**：MIT（推荐）。学术工具惯例。
3. **README 结构**：英文主 README.md + 中文 README.zh-CN.md（推荐，符合开源惯例）。
4. **GPU 安装策略**：环境向导"标准模式"自动装 conda CPU 版 LAMMPS（人人可用）；GPU 版走"编译向导"（检测到 CUDA 才出现）。本项目开发机直接检测到 GPU 版。

---

*注：V_stream 计算方法（一维泊松 vs 补偿电场法）由研究方案定稿，工具内做成可插拔，不阻塞开发。*
