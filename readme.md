# wengui

配合 went 项目使用的 GUI

## 项目地址

<https://github.com/ctmakro/wengui>

## 特性

- 启动/关停 `went` 主程序以及 `v2ray`
- 由 `v2ray` 提供http/https/socks4/socks4a/socks5代理服务
- 自动设置/重置系统代理设置

## 需要放在CWD下的文件

- v2ray/v2ctl主程序
- v2ray的config.json, geoxxx.dat
- went主程序（名称因OS而异）

## Python3下直接运行

```bash
$ python main.py
```

## 打包

使用PyInstaller 3.3: `pip install pyinstaller`

- Windows

  ```bash
  cd wengui
  pyinstaller main.spec
  cd dist/wengui
  ```
  在Windows下没有特别方便的命令行zip压缩工具，我是徒手压的。

- OSX

  ```bash
  cd wengui
  pyinstaller main.spec
  cd dist/wengui
  tar -czf wengui_darwin.tar.gz *
  ```

- Linux

  没有时间搞Linux的版本。
