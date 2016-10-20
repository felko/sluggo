sluggo
======

sluggo is a shell that handles multiple REPLs.

It provides a few REPLs implementations, including
a git REPL, a Python REPL, and a general command
REPL.

sluggo features a few basic commands that allow you
to switch between REPLs:

* ``!quit [repl]``: closes the specified REPL or the
    current one if no argument is given.
* ``!go [repl]``: switch to the specified REPL
* ``@[repl] [cmd]``: executes the command from the
    specified REPL
* ``$[cmd]``: executes a system command
* ``!exit``: exits sluggo

sluggo is extensible. That means you can define your
own REPLs easily:

.. code:: python3

    class parrot(sluggo.REPL):
        def eval(self, input):
            print(input)

And that is all you need to start your parrot REPL
from sluggo:

.. code:: bash

    $ !go parrot
    > hey
    hey
    > it's annoying
    it's annoying

