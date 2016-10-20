#!/usr/bin/env python3.4
# coding: utf-8

__all__ = (
    'REPL',
    'REPLError',
    'system'
)

import os
import readline
import atexit
import subprocess
import shlex
import code

CONF_DIR = os.path.expanduser('~/.sluggo/')


class REPLError(Exception):
    pass


class REPL:
    def __init__(self):
        self.prompt = self.name

    @classmethod
    def get_repl_with_name(cls, name):
        for subcls in cls.__subclasses__():
            if subcls.__name__ == name:
                return subcls
            else:
                try:
                    return subcls.get_repl_with_name(name)
                except REPLError:
                    continue

        raise REPLError('No REPL named {}'.format(name))

    @property
    def name(self):
        return self.__class__.__name__

    def __init__(self, register_history=True):
        if register_history:
            if not os.path.exists(CONF_DIR):
                os.makedirs(CONF_DIR)

            hist_file_path = os.path.join(CONF_DIR, self.name)

            try:
                readline.read_history_file(hist_file_path)
            except IOError:
                pass

            atexit.register(readline.write_history_file, hist_file_path)

            readline.parse_and_bind('tab: complete')
            readline.set_completer_delims(' \t\n')
            readline.set_completer(self.completer)

    def completer(self, text, state):
        text = os.path.expanduser(text)
        head, tail = os.path.split(text)

        search_dir = os.path.join('.', head)
        candidates = [s for s in os.listdir(search_dir) if s.startswith(tail)]

        if state >= len(candidates):
            return None

        if len(candidates) == 1:
            fn = os.path.join(head, candidates[0])
            if not os.path.isdir(fn):
                return fn + ' '
            return fn + '/'

        return os.path.join(head, candidates[state])

    def eval(self, input):
        raise NotImplementedError('{}.eval is not defined.'.format(self.__class__.__qualname__))


class system(REPL):
    def __init__(self):
        self.prompt = '$ '

    def eval(self, input):
        cmd = shlex.split(input)
        subprocess.call(cmd)


class cmd(REPL):
    def __init__(self, cmd):
        self.prompt = cmd + '> '
        self.cmd = cmd

    def eval(self, input):
        cmd = shlex.split(input)
        cmd.insert(0, self.cmd)
        subprocess.call(cmd)

class git(cmd):
    def __init__(self):
        super().__init__('git')

class py(REPL):
    def __init__(self):
        self.prompt = '>>> '
        self.console = code.InteractiveConsole()

    def eval(self, input):
        self.console.push(input)
