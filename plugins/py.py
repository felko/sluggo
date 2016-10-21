#!/usr/bin/env python3.4
# coding: utf-8

import os
import code
from importlib.machinery import SourceFileLoader
import sluggo


class py(sluggo.REPL):
    def __init__(self, path=None):
        self.path = path
        self.prompt = '>>> '

        if path is not None:
            self.console = code.InteractiveConsole(filename=os.path.basename(path))

            with open(path) as file:
                src = file.read()
                c = compile(src, path, 'exec')
                self.console.runcode(c)
        else:
            self.console = code.InteractiveConsole()

    def init(self):
        print('Python 3 sluggo console')
        print('Type "help", "copyright", "credits" or "license" for more information.')

    def eval(self, input):
        self.console.push(input)

    def interpret_multi(self, lines):
        src = '\n'.join(lines)
        self.console.runsource(src)
