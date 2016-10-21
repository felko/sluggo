#!/usr/bin/env python3.4
# coding: utf-8

import code
import sluggo


class py(sluggo.REPL):
    def __init__(self):
        self.prompt = '>>> '
        self.console = code.InteractiveConsole()

    def eval(self, input):
        self.console.push(input)

    def interpret_multi(self, lines):
        src = '\n'.join(lines)
        self.console.runsource(src)
