#!/usr/bin/env python3.4
# coding: utf-8

import subprocess
import sluggo


class cmd(sluggo.REPL):
    def __init__(self, cmd):
        self.prompt = cmd + '> '
        self.cmd = cmd

    def eval(self, input):
        subprocess.call(self.cmd + ' ' + input, shell=True)
