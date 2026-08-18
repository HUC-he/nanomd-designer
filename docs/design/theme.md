# 界面配色规范（UI Theme）

> 状态：M0 定稿，M1 起在 GUI 中落地。

## 设计目标

- 现代、干净、不刺眼，以"深海 / 水流"为意象（贴合纳米流体主题）；
- 深色为主推（科学软件常用），浅色同步提供；
- 语义色严格区分（成功 / 警告 / 错误）；
- 原子颜色遵循 MD 社区惯例（参考 VMD），避免新手误解。

## 深色主题 Deep Channel（`assets/themes/dark.qss`）

| Token | Hex | 用途 |
|---|---|---|
| `bg` | `#0E1621` | 窗口背景（深海军蓝黑） |
| `surface` | `#162130` | 面板 / 选项卡 / 分组框 |
| `surface-2` | `#1D2B3D` | 悬停 / 凸起 / 按钮底 |
| `border` | `#28394E` | 边框 / 分隔线 |
| `text` | `#E8EEF5` | 主文字 |
| `text-muted` | `#93A5B8` | 次文字 / 说明 |
| `text-disabled` | `#5F7388` | 禁用 |
| `accent` | `#2DD4BF` | 主色（水青色），焦点 / 悬停描边 |
| `accent-strong` | `#0D9488` | 主按钮填充 |
| `accent-blue` | `#60A5FA` | 次强调（链接 / 信息） |
| `selection` | `#1E3A5F` | 选中行 / 列表 |
| `success` | `#34D399` | 就绪 / 成功 |
| `warning` | `#FBBF24` | 可选缺失 / 提醒 |
| `error` | `#F87171` | 必需缺失 / 报错 |

## 浅色主题 Clear Water（`assets/themes/light.qss`）

| Token | Hex | 用途 |
|---|---|---|
| `bg` | `#F4F7FA` | 窗口背景 |
| `surface` | `#FFFFFF` | 面板 |
| `surface-2` | `#EAF0F6` | 悬停 / 表头 |
| `border` | `#D5DEE8` | 边框 / 分隔线 |
| `text` | `#1E2A38` | 主文字 |
| `text-muted` | `#5B6B7E` | 次文字 |
| `text-disabled` | `#8B9AA9` | 禁用 |
| `accent` | `#0D9488` | 主色 |
| `accent-strong` | `#0F766E` | 主按钮悬停 |
| `accent-blue` | `#2563EB` | 链接 / 信息 |
| `selection` | `#DBEAFE` | 选中行 |
| `success` | `#059669` | 成功 |
| `warning` | `#D97706` | 警告 |
| `error` | `#DC2626` | 错误 |

## 原子 / 分子配色（两主题通用，参考 VMD 惯例）

| 对象 | Hex | 说明 |
|---|---|---|
| 石墨烯 / 碳 C | `#8A97A6` | 灰 |
| 氧 O（水 / 官能团） | `#E5484D` | 红 |
| 氢 H | `#F2F4F8` | 白 |
| Na⁺ | `#9D7BFF` | 紫 |
| Cl⁻ | `#35C4C0` | 青 |
| K⁺ | `#E58C4A` | 橙 |
| Ca²⁺ | `#2E8FB8` | 深青蓝 |
| 官能团标记 -OH | `#34D399` | 绿（仅选中 / 高亮） |
| 官能团标记 -COOH | `#FBBF24` | 橙 |
| 官能团标记 -NH₂ | `#60A5FA` | 蓝 |

## 排版与间距

- 字体跟随系统默认；基础字号 10 pt，标题 12–13 pt；
- 面板内边距 12 px，控件间距按 8 px 网格；
- 组件圆角 6 px，边框 1 px，主按钮用 accent-strong 填充；
- 状态灯：绿 = 就绪，黄 = 可选组件缺失，红 = 必需组件缺失。

## 文件位置

- `assets/themes/dark.qss`、`assets/themes/light.qss` —— 实际样式表
- `assets/branding/palette.html` —— 配色预览页（浏览器打开即可看效果）

## 落地约定

- 主按钮在代码里标记 `setProperty("primary", True)`，QSS 用
  `QPushButton[primary="true"]` 命中；
- 面板容器统一 `objectName = "Panel"`；
- 新增颜色先查本表，不要硬编码散落的十六进制。
