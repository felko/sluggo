#!/usr/bin/env python3.4
# coding: utf-8

__all__ = (
    'REPL',
    'REPLError',
    'sys',
    'on',
    'CONF_DIR',
    'HIST_DIR',
    'PLUGIN_DIR',
    'CONF_FILE'
)

import re
import os
import readline
import atexit
import subprocess
import code
import functools
from collections import OrderedDict

CONF_DIR = os.path.expanduser('~/.sluggo')
HIST_DIR = os.path.expanduser('~/.sluggo/history')
PLUGIN_DIR = os.path.expanduser('~/.sluggo/plugins')
CONF_FILE = os.path.expanduser('~/.sluggorc')


class REPLError(Exception):
    pass


class _REPLHook:
    def __init__(self, fn, patterns):
        self.fn = fn
        self.patterns = []

        for pat in patterns:
            self.patterns.append(re.compile('^' + pat + '$'))

    def process(self, string):
        for pat in self.patterns:
            m = pat.match(string)

            if m:
                def _wrapper_func(obj):
                    return self.fn(obj, *m.groups(), **m.groupdict())
                return _wrapper_func
        else:
            raise REPLError("Couldn't parse {!r}".format(string))


def on(*patterns):
    return functools.partial(_REPLHook, patterns=patterns)


class REPLMeta(type):
    instances = {}

    def __prepare__(mcs, cls):
        return OrderedDict()

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        REPLMeta.instances[name] = cls

        cls.hooks = []

        for _, val in attrs.items():
            if isinstance(val, _REPLHook):
                cls.hooks.append(val)


    def get_repl_with_name(cls, name):
        try:
            return REPLMeta.instances[name]
        except KeyError:
            raise REPLError('No REPL named {}'.format(name))


class REPL(metaclass=REPLMeta):
    def __init__(self, register_history=True):
        self.prompt = self.name + '> '

        if register_history:
            if not os.path.exists(HIST_DIR):
                os.makedirs(HIST_DIR)

            hist_file_path = os.path.join(HIST_DIR, self.name)

            try:
                readline.read_history_file(hist_file_path)
            except IOError:
                pass

            atexit.register(readline.write_history_file, hist_file_path)

            readline.parse_and_bind('tab: complete')
            readline.set_completer_delims(' \t\n')
            readline.set_completer(self.completer)

    @property
    def name(self):
        return self.__class__.__name__

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

    def interpret(self, input):
        for hook in self.hooks:
            try:
                f = hook.process(input)
            except REPLError:
                continue
            else:
                return f(self)

        self.eval(input)

    def interpret_multi(self, lines):
        multi = []

        for line in lines:
            if multi:
                if line == '!}':
                    self.interpret_multi(multi)
                    multi.clear()
                else:
                    multi.append(line)
            elif line == '!{':
                multi.append(line)
            else:
                self.interpret(line)

    def eval(self, input):
        raise REPLError("Couldn't interpret the command {!r}".format(input))

    def init(self):
        pass

    def update(self):
        pass


class sys(REPL):
    def __init__(self):
        self.prompt = '$ '

    @on(r'cd\s+(.*)')
    def eval_cd(self, path):
        os.chdir(os.path.expanduser(path))

    def eval(self, input):
        subprocess.call(input, shell=True)
