First off you may be asking yourself, "Why would I want multiple files when I can have a single EXE"? 
Well Jorge, the single EXE has to first extract itself into a temporary directory before it can run which
is slower than the multifile compile. Both the single EXE and the collection of files are 100% portable and
can be moved between windows computers without issue. In most cases the only difference you will notice 
is that the single EXE version will take a few extra seconds to load up and may use slightly more memory.

How to compile:

First have the setup.py script in hand that I already made for this app or make one using the code attached 
at the bottom. All you have to do to compile is run the following from the command line after you have assembled all 
the files you need to compile into the same folder as the setup.py:

	python setup.py

Thats it. It will do the rest. You will find your compiled program in the folder 'bLyrics_Multifiles_Compiled'.

Here's the setup.py:





from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
	scripts = ["bLyrics_COM.pyw"],
	windows = 
		[{
			"script": "bLyrics_COM.pyw",
			"icon_resources": [(1, "icon/bLyrics.ico")]
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