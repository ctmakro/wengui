# -*- mode: python -*-

block_cipher = None

executable_name = 'wengui'

include_files = '''
./config.json
./geoip.dat
./geosite.dat

./readme.md
'''

include_files = include_files.split('\n')
include_files = map(lambda x:x.strip(),include_files)
include_files = filter(lambda x:len(x)>0,include_files)
include_files = list(include_files)

import sys
if sys.platform=='win32':
    include_files+=[
        './v2ray.exe',
        './v2ctl.exe',
        './went_win64.exe',
    ]
elif sys.platform=='darwin':
    include_files+=[
        './went_darwin',
        './v2ray',
        './v2ctl',
    ]
else:
    raise NotImplementedError('system not supported for pyinstalling.')

datas = [(n,'.') for n in include_files]


a = Analysis(['main.py'],
             pathex=['/Users/chia/wengui'],
             binaries=[],
             datas=datas,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name=executable_name,
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=executable_name)
