#!/usr/bin/env python3.4
# coding: utf-8

import shlex
import subprocess
import sluggo


class cmd(sluggo.REPL):
    def __init__(self, cmd):
        self.prompt = cmd + '> '
        self.cmd = cmd

    def eval(self, input):
        cmd = shlex.split(input)
        cmd.insert(0, self.cmd)
        subprocess.call(cmd)
