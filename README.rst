sluggo
======

sluggo is a shell that can handle multiple REPLs.

It provides a few REPLs implementations, including
a git REPL, a Python REPL, and a general command
REPL.


Demo
----

`demo <https://asciinema.org/a/8i56cd2twd96r9xpxwp4m6saf>`_

Features
--------

sluggo features a few basic commands that allow you
to switch between REPLs:

* ``!go [repl]``: switch to the specified REPL
* ``@[repl] [cmd]``: executes the command from the specified REPL
* ``$[cmd]``: executes a system command
* ``!open [repl]``: opens a REPL session without switching
* ``!close [repl]``: closes the specified REPL
* ``!alias [name] [cmd]``: Creates an alias to a command that can be called with ``![name]``
* ``!quit``: closes the current one if no argument is given
* ``!exit``: exits sluggo
* ``!cls``: clears the console
* ``!reload``: reloads the configuration file and the plugins

sluggo is extensible. That means you can define your
own REPLs easily:

.. code:: python

    import sluggo

    class parrot(sluggo.REPL):
        def eval(self, input):
            print(input)

You just need to put this in your ~/.sluggo/plugins directory for it to be
loaded automatically:

.. code:: bash

    $ !go parrot
    parrot> hey
    hey
    parrot> it's annoying
    it's annoying
