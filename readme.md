# wengui

配合 went 项目使用的 GUI

## 需要放在CWD下的文件

- v2ray主程序
- v2ray的config.json
- went主程序（名称因OS而异）

## 运行

```bash
$ python main.py
```

## 打包

- OSX

  ```bash
  $ pyinstaller main.spec
  $ cd ./dist/wengui
  $ tar -czf wengui_darwin.tar.gz *
  ```
