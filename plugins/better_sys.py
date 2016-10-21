#!/usr/bin/env python3.4
# coding: utf-8

import re
import os
import subprocess
from colorama import *
import sluggo

init()


class sys(sluggo.REPL):
    def __init__(self):
        pass

    @property
    def prompt(self):
        pwd = os.getcwd()

        if re.match(r'/home/(\w+)', pwd):
            hierarchy = re.sub(r'/home/(\w+)', '~', pwd).split(os.sep)
        else:
            hierarchy = list(filter(bool, pwd.split(os.sep)))

        p = '\033[48;5;236m '

        if len(hierarchy) <= 5:
            for directory in hierarchy:
                p += directory + ' ' + chr(0xE0B1) + ' '
        else:
            for directory in hierarchy[:3]:
                p += directory + ' ' + chr(0xE0B1) + ' '

            p += '… ' + chr(0xE0B1) + ' '

            for directory in hierarchy[-2:]:
                p += directory + ' ' + chr(0xE0B1) + ' '

        p += ' $ \033[0;38;5;236m' + chr(0xE0B0) + ' \033[0m'
        return p

    @sluggo.on(r'cd\s+(.*)')
    def eval_cd(self, path):
        os.chdir(path)

    def eval(self, input):
        subprocess.call(input, shell=True)
