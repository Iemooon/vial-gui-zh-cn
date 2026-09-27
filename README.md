# vial-gui — 简体中文分支

本仓库是 [vial-gui](https://github.com/vial-kb/vial-gui) 的**简体中文界面分支**（fork），
在官方代码之上加了一层运行期翻译，不修改任何上游文件。

- 上游仓库：https://github.com/vial-kb/vial-gui
- 本分支仓库：https://github.com/Iemooon/vial-gui-zh-cn
- 默认分支：`zh-cn`（汉化在此分支上维护）
- 官方使用说明与固件：https://get.vial.today/

Vial 是跨平台（Windows / Linux / macOS）的开源图形界面，配合 QMK 分支，
用于实时配置键盘的键位、层、宏等设置。

---

## 关于本分支

### 分支结构

| 分支 | 用途 |
| --- | --- |
| `main` | 镜像上游 `upstream/main`，不做任何本地改动，只用于同步 |
| `zh-cn` | 承载汉化，默认分支 |

同步上游的方式（在 `zh-cn` 上）：

```
git fetch upstream
git merge upstream/main
```

因为汉化集中在新增目录与两个入口文件的一行调用上，正常情况下合并不会冲突。

### 汉化范围

**已汉化：**

- 主窗口菜单、标签页与各编辑器页面的标题
- 各配置页的字段标签（含 QMK 设置页的设置项标题与其二级选项卡名）
- 各类按钮、提示、确认框与状态文字

**保持英文（有意为之，不是漏翻）：**

- 键位名称与说明文字（如 `KC_A`、`MO(1)`、`LT(2, KC_SPC)` 等），以及键位托盘的分类标签
- 键盘布局名、主题名
- `ISO` / `JIS` 等标准名，以及 `▲ ▼ ×` 一类符号
- QMK 设置项中的**取值内容**（数字、开关的数值部分）

保留键名不译的原因是：键盘布局与固件文档都以这些符号为准，译成中文反而无法对照。

### 实现方式

翻译不写进上游文件，而是：

- 新增 `src/main/python/i18n/`，内含翻译层 `__init__.py` 与词表 `zh_cn.py`
- 在 `main.py`、`webmain.py` 各加一处 `i18n.install()` 调用

翻译层子类化 `QTranslator` 接管项目既有的 `tr = QCoreApplication.translate` 链路。
QMK 设置页的设置项标题由上游以 `QLabel(option["title"])` 直接构造、不经过 `tr()`，
因此改为在载入 `resources/base/qmk_settings.json` 时就地替换。

词表按 Qt context 分组，想调整措辞直接改 `src/main/python/i18n/zh_cn.py` 即可。

---

## 获取可执行文件

本仓库已配置 GitHub Actions，每次推送到任意分支都会自动构建三平台产物。

打开仓库页面的 **Actions** → 选择最近一次 **CI** 运行 → 在页面底部 **Artifacts** 区下载：

| 产物 | 平台 | 说明 |
| --- | --- | --- |
| `vial-win.zip` | Windows | 解压即用，双击其中的 `Vial.exe` |
| `vial-win-installer` | Windows | `VialSetup.exe` 安装包 |
| `vial-mac` | macOS | `.dmg` |
| `vial-linux` | Linux | `AppImage` |

CI 使用 Python 3.6 与 `fbs` 构建（`fbs` 官方支持的最高版本即 3.6），
与官方发布方式一致。

---

## 本地运行（开发用）

需要本地 Python 3.6 环境（`fbs` 的要求）：

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
fbs run
```

如果只是想改动词表后立刻看效果，不必等 CI 构建，直接用源码启动即可。
词表位于 `src/main/python/i18n/zh_cn.py`，改动后重启应用生效。

> 注意：`fbs` 免费版只支持 Python 3.5 / 3.6，因此**本地打包**需要 3.6 环境；
> 更新的 Python 版本可以运行源码，但无法用 `fbs freeze` 打包。
> 需要安装包时，请使用上面 Actions 的产物。

---

## 许可

本分支遵循上游许可，见 [COPYING](COPYING)。原始项目版权归 Vial 及
[vial-gui 贡献者](https://github.com/vial-kb/vial-gui/graphs/contributors) 所有。
汉化部分同样以上游许可发布。
