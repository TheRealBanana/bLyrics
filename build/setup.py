from distutils.core import setup
import py2exe, sys

sys.argv.append('py2exe')

setup(
	scripts = ["../bLyrics2.pyw"],
	windows = 
		[{
			"script": "../bLyrics_COM.pyw",
			"icon_resources": [(1, "../icon/bLyrics.ico")]
		}],
	data_files=[('imageformats',[r'C:\Python26\Lib\site-packages\PyQt4\plugins\imageformats\qico4.dll'])],
	options = 
		{
			"py2exe": {
				"dll_excludes": ["MSVCP90.dll", "w9xpopen.exe"],
				"compressed": True, 
				"includes":["sip", "PyQt4.QtCore", "PyQt4.QtGui", "PyQt4.QtNetwork"],
				"optimize": 2,
				"bundle_files": 3,
				"dist_dir": "bLyrics_Multifiles_Compiled",
			}
		},
	zipfile = None,
) 