# -*- mode: python -*-
from os import getcwd
from os.path import abspath
_CURDIR = getcwd()

a = Analysis(['../src/bLyrics2.pyw'],
             pathex=[_CURDIR],
             hookspath=None,
             runtime_hooks=None, datas=[("../src/dialogs/logic/lyricsProviders", "lyricsProviders")])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='bLyrics2.exe',
          debug=False,
          strip=None,
          upx=False,
          console=False,
          icon='../src/icon/bLyrics.ico')
