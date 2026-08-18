"""Lightweight zh/en translation (Qt Linguist migration planned as strings grow)."""

from __future__ import annotations

ZH = "zh"
EN = "en"

_current = ZH

STRINGS: dict[str, dict[str, str]] = {
    "app.title": {"zh": "NanoMD Designer", "en": "NanoMD Designer"},
    "menu.file": {"zh": "文件(&F)", "en": "&File"},
    "menu.language": {"zh": "语言 / Language", "en": "语言 / Language"},
    "menu.theme": {"zh": "主题 / Theme", "en": "主题 / Theme"},
    "menu.help": {"zh": "帮助(&H)", "en": "&Help"},
    "action.export": {"zh": "生成 LAMMPS 脚本…", "en": "Generate LAMMPS scripts…"},
    "action.quit": {"zh": "退出", "en": "Quit"},
    "action.about": {"zh": "关于", "en": "About"},
    "design.title": {"zh": "体系设计", "en": "System Design"},
    "design.box": {"zh": "盒子尺寸（Å）", "en": "Box size (Å)"},
    "design.lx": {"zh": "Lx（流动方向）", "en": "Lx (flow)"},
    "design.ly": {"zh": "Ly（宽度）", "en": "Ly (width)"},
    "design.lz": {"zh": "Lz（高度）", "en": "Lz (height)"},
    "design.walls": {"zh": "通道壁（z，Å）", "en": "Channel walls (z, Å)"},
    "design.lower": {"zh": "下壁内表面", "en": "Lower wall (inner)"},
    "design.upper": {"zh": "上壁内表面", "en": "Upper wall (inner)"},
    "design.height": {"zh": "通道高度", "en": "Channel height"},
    "design.water": {"zh": "水模型", "en": "Water model"},
    "design.salt": {"zh": "盐", "en": "Salt"},
    "design.conc": {"zh": "浓度（mol/L）", "en": "Concentration (mol/L)"},
    "design.temp": {"zh": "温度（K）", "en": "Temperature (K)"},
    "design.seed": {"zh": "随机种子", "en": "Random seed"},
    "design.oxidation": {"zh": "氧化度（M2）", "en": "Oxidation (M2)"},
    "design.advanced": {"zh": "高级", "en": "Advanced"},
    "design.velocity": {"zh": "目标流速（Å/ps）", "en": "Target velocity (Å/ps)"},
    "design.force": {"zh": "驱动体力（kcal/mol/Å）", "en": "Drive force (kcal/mol/Å)"},
    "design.build": {"zh": "构建并预览", "en": "Build & preview"},
    "output.title": {"zh": "输出", "en": "Output"},
    "output.open": {"zh": "打开输出目录", "en": "Open output folder"},
    "output.preview": {"zh": "in 文件预览", "en": "in-file preview"},
    "build.error": {"zh": "构建失败", "en": "Build failed"},
    "export.notbuilt": {"zh": "请先构建体系。", "en": "Build the system first."},
    "export.ok": {"zh": "已生成：", "en": "Generated:"},
    "about.text": {
        "zh": "NanoMD Designer {} - 开源图形化 LAMMPS 纳米通道建模工具\n\n"
        "在 Windows 里设计纳米通道体系（石墨烯 / GO + TIP3P 水 + 离子），"
        "一键生成 LAMMPS data / in 脚本。\n\nMIT License · 欢迎贡献",
        "en": "NanoMD Designer {} - open-source GUI for LAMMPS nanochannel design\n\n"
        "Design nanochannel systems on Windows (graphene/GO + TIP3P water + ions)\n"
        "and generate LAMMPS data/in scripts with one click.\n\n"
        "MIT License · contributions welcome",
    },
}


def tr(key: str) -> str:
    return STRINGS.get(key, {}).get(_current, key)


def set_language(lang: str) -> None:
    global _current
    if lang not in (ZH, EN):
        raise ValueError(f"unsupported language: {lang!r}")
    _current = lang


def current_language() -> str:
    return _current
