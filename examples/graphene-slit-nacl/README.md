# Example: graphene slit channel + TIP3P water + 0.6 M NaCl

基准体系，对应《碳基水伏 MD-技术规格手册》§2：

| 项 | 值 |
|---|---|
| 盒子 | 150 × 40 × 20 Å |
| 通道高度 | 10 Å（壁内表面 z = 5 / 15 Å） |
| 膜 | 双层单层石墨烯（覆盖整个 xy） |
| 水 | TIP3P，1404 分子 |
| 离子 | NaCl 0.6 M，22 对（44 个离子） |
| 总原子数 | 8550，总电荷 0 |
| 种子 | 12345 |

文件：

- `system.data` — LAMMPS data 文件（atom_style full）
- `in.streaming.lammps` — 重力法流致模拟 in 文件（y/z 定向控温、`fix addforce`、SHAKE、PPPM、膜固定）
- `preview_3d.png` / `preview_top.png` — 离屏渲染预览（深色主题下的原子配色）

在 WSL 中运行：

```bash
lmp -sf gpu -pk gpu 1 -in in.streaming.lammps
```

重新生成本示例：

```bash
PYTHONPATH=src python scripts/generate_example.py
```
