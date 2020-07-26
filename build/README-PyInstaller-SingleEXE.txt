How to compile:

You must first have the following packages installed:

1) Python 2.7 (CANNOT BE THE 3.x BRANCH OR ANYTHING LOWER THAN 2.7)
2) PyQt4, latest version in the 4 branch if you can
4) PyWin32 (for the win32com package)
5) PyInstaller (to compile to exe)


After you have that all installed, all you have to do to compile is do
the following command in the directory you unzipped this to:

pyinstaller bLyrics.spec
...
Or you can just run the file named: MakeSingleEXE.bat


That will take a minute or two depending on the speed of your computer and
will eventually spit out two folders called build and dist. You can delete
the build folder as it contains files left over from the build process. In
the dist folder is your bLyrics.exe file, ready to use.
