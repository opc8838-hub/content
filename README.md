# 我的内容工作台

基于开源 [Easel](https://github.com/ZJU-REAL/Easel) 的 Codex 原生集成，持续维护公众号、小红书、视频号等内容工作流。当前优先跑通公众号：热点、选题、写作、配图、排版和发布。

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/opc8838-hub/content?ref=main)

## 从哪里打开

| 使用方式 | 入口 | 运行条件 |
|---|---|---|
| 本机工作台 | 双击 `启动内容工作台.cmd`，打开 <http://127.0.0.1:7862/> | 本机依赖已安装，电脑开机 |
| 在线按需启动 | 上方 Codespaces 按钮；以后从 [Codespaces 列表](https://github.com/codespaces) 恢复同一个环境 | 首次安装依赖并连接 Codex；端口保持私有 |
| 固定网址长期在线 | 见 [在线使用说明](docs/在线使用.md) | 还需服务器、登录保护、持久化与进程管理，尚未部署 |

Git 仓库保存可运行代码。工作台同时需要 Python 后端和 Codex CLI，GitHub Pages 的静态页面托管不能运行完整工作台。

## 功能

- **热点雷达**：多平台榜单；数据源可用性取决于第三方接口。
- **选题与策划**：收藏、角度分析、标题、大纲和选题评估。
- **内容制作**：Codex 编排写作、图片、文章排版和其他制作工具。
- **运营管理**：用户画像、可恢复运营任务、内容日历、内容库、发布记录与复盘。
- **113 项能力库**：保留能力规范及脚本，外部凭证和可选依赖按需接入。

## Windows 本机使用

已有运行环境时，双击根目录 [`启动内容工作台.cmd`](启动内容工作台.cmd)。启动器检查工作台服务；未启动时后台启动，等待就绪后打开网页。启动日志位于集成 `runtime/outputs/_service/workbench.log`。

新电脑先准备 Python 3.10+、Node.js 22+、FFmpeg/FFprobe 和 Codex CLI，按安装脚本安装：

```powershell
powershell -ExecutionPolicy Bypass -File .\integrations\codex\seal-private-operations-v3\scripts\install-windows.ps1
```

如果系统缺少 winget 或 PowerShell 不能运行，需要先处理这些安装前置条件。浏览器登录需要 Playwright Chromium，音视频制作需要相应依赖。账号认证、平台权限及真实发布需要分别接通和确认。

## 首次在线使用

创建 Codespace 后等待安装，在 Ports 中打开 7862 的私有访问地址。在终端执行：

```bash
codex login --device-auth
```

根据官方提示连接自己的 Codex。然后在工作台填写账号画像，再接入公众号。详细步骤、能力范围、数据备份和长期在线部署见 [在线使用说明](docs/在线使用.md)。

## 数据与凭证

本仓库只上传源代码、通用能力、模板与前端构建产物。`.env`、公众号凭证、token 缓存、Codex 认证、浏览器登录态、个人画像和文章素材被 Git 忽略，保存在各自运行环境。迁移代码不会自动迁移账号登录或个人内容。

## 来源与许可证

- 上游项目：[ZJU-REAL/Easel](https://github.com/ZJU-REAL/Easel)
- 导入范围：Easel 的 `integrations/codex/` 独立工作台集成。
- 适配来源：[上游 PR #28](https://github.com/ZJU-REAL/Easel/pull/28)
- 导入版本：`5c375e1fcaff470907af975d794b229d1ab350ea`
- 许可证：[Apache License 2.0](LICENSE)，保留集成目录中的 [NOTICE](integrations/codex/seal-private-operations-v3/NOTICE)。
- 第三方来源及各自许可说明：[上游致谢](docs/ACKNOWLEDGMENTS.md)。

本仓库包含个人工作台品牌、Windows 启动与在线启动配置等后续调整，不依赖 OpenClaw。
