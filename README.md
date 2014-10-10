
This is a set of Python scripts I personally use to interactively perform
routine tasks on my company's AWS resources.


Requirements
------------

All script are written in Python using the [`boto`][boto] interface to Amazon Web Services.
The [`colorama`][colorama] module is used to provide colored terminal text.

	sudo apt-get install python python-pip
	sudo pip install boto
	sudo pip install colorama

[boto]: http://boto.readthedocs.org/en/latest/index.html
[colorama]: https://pypi.python.org/pypi/colorama/


Getting started
---------------

Every single script has a configuration variable called `PROFILE_NAME`: this
is the name of the profile used to get API credentials to access your AWS resources
(if you are not familiar with AWS named profiles, look [here][aws-profiles]).

[aws-profiles]: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-multiple-profiles

So, for each script you intend to use, you have to check (or edit) its `PROFILE_NAME`
variabile, and then place your API credentials for that profile in `~/.aws/credentials`.
For example:

	[VolumeBackupper]
	aws_access_key_id = QWERTYXXXXXXXXXXXXXX
	aws_secret_access_key = XXXxxxXXXxxxXXXxxxXXXxxxXXXxxxXXXxxxXXXx
	[InstanceLister]
	aws_access_key_id = ASDFGXXXXXXXXXXXXXXX
	aws_secret_access_key = XXXxxxXXXxxxXXXxxxXXXxxxXXXxxxXXXxxxXXXx


Usage and customization
-----------------------

Before using any script, look at its configuration variables at beginning
of the code: you likely have to edit some of them, such as `REGION`,
`SSH_CERTIFICATE`, and so on. Then you can simply run a specific utility 
with the Python interpreter, for example the one which backups volumes:

	python backup_volumes.py

Or you can run the `index.py` script, which lists all available
scripts (also your custom and private ones) and interactively asks you 
which to run:

	python index.py

I shared these utilities mainly because you can use as a starting point
to write your own scripts. Remember that, for this exact reason, all Python
scripts you place in that folder will be listed and can be run by `index.py`.


Contribute
----------

If you think your script can be useful to all of us, feel free to share them
[**forking this repo**][forking] and making a pull request. If you want to
keep a script private, just prepend the filename with an underscore `_`,
and it will be excluded from the repo (because of the `.gitignore` file).

[forking]: https://github.com/lorenzos/AWSInteractiveUtils/fork

Considering I'm a Python newbie (I used it just because `boto` is great and 
the languge itself looks really suitable for command-line stuff), I will gladly
accept contributions also if they are just fixes or refinements.

