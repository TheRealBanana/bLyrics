First off you may be asking yourself, "Why would I want multiple files when I can have a single EXE"? 
Well Jorge, the single EXE has to first extract itself into a temporary directory before it can run which
is slower than the multifile compile. Both the single EXE and the collection of files are 100% portable and
can be moved between windows computers without issue. In most cases the only difference you will notice 
is that the single EXE version will take a few extra seconds to load up and may use slightly more memory.

How to compile:

All you have to do to compile is run the following from the command line in the same folder as the setup.py:

	python setup.py

Thats it. It will do the rest. You will find your compiled program in the folder 'bLyrics_Multifiles_Compiled'.