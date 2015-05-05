# -*- mode: python -*-
from os import getcwd
_CURDIR = getcwd()

a = Analysis(['bLyrics_COM.pyw'],
             pathex=[_CURDIR],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='bLyrics_COM.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon='icon/bLyrics.ico')
