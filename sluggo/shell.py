#!/usr/bin/env python3.4
# coding: utf-8

__all__ = (
    'Shell',
)

import os
import glob
from importlib.machinery import SourceFileLoader
from collections import OrderedDict

from sluggo.repl import *


class Shell(REPL):
    def __init__(self, base_repl=None):
        base_repl = system() or base_repl
        self.repls = OrderedDict()
        self.repls[base_repl.name] = base_repl

        self.prompt = ''
        self.current_repl_name = base_repl.name
        self.running = False

        if os.path.exists(os.path.expanduser(CONF_FILE)):
            with open(CONF_FILE) as conf:
                self.interpret_multi(map(str.strip, conf.readlines()))

        for plugin_path in glob.glob(os.path.join(CONF_DIR, 'plugins', '*.py')):
            src = SourceFileLoader(os.path.basename(plugin_path), plugin_path)
            src.load_module()

    @property
    def repl(self):
        return self.repls[self.current_repl_name]

    @on(r'!exit')
    def eval_exit(self):
        self.running = False

    @on(r'!quit', r'!q')
    def eval_quit(self):
        del self.repls[self.current_repl_name]

        if not self.repls:
            self.running = False
        else:
            self.current_repl_name = list(self.repls.values())[-1].name

    @on(r'!{')
    def eval_enter_multi(self):
        lines = []
        inp = input('... ')

        while inp != '!}':
            lines.append(inp)
            inp = input('... ')

        self.repl.interpret_multi(lines)

    @on(r'!go\s+(\w+)\s*(.*)')
    def eval_go(self, repl_name, args):
        if repl_name not in self.repls:
            self.start_repl(repl_name, args.split())

        self.current_repl_name = repl_name

    @on(r'!close\s+(\w+)')
    def eval_close(self, repl_name):
        del self.repls[repl_name]

    @on(r'!open\s+(\w+)')
    def eval_open(self, repl_name):
        if repl_name not in self.repls:
            self.start_repl(repl_name, args)

    @on(r'@(\w+)\s*(.*)')
    def eval_at(self, repl_name, *cmd):
        cur_repl = self.current_repl_name

        if repl_name not in self.repls:
            self.start_repl(repl_name)
            self.repls[repl_name].interpret(' '.join(cmd))
            del self.repls[repl_name]
        else:
            self.repls[repl_name].interpret(' '.join(cmd))

    @on(r'\$(.)')
    def eval_system(self, cmd):
        self.interpret('@system ' + cmd)

    def eval(self, inp):
        try:
            self.repl.interpret(inp)
        except Exception as e:
            print(e)
            raise e

    # def eval(self, inp):
    #     unknown = False
    #
    #     if inp.startswith('!'):
    #         cmd = inp[1:].split()
    #
    #         if len(cmd) == 1:
    #             if cmd[0] == 'exit':
    #                 self.running = False
    #             elif cmd[0] in ('q', 'quit'):
    #                 del self.repls[self.current_repl_name]
    #
    #                 if not self.repls:
    #                     self.running = False
    #                 else:
    #                     self.current_repl_name = list(self.repls.values())[-1].name
    #             elif cmd[0] == '{':
    #                 lines = []
    #                 inp = input('... ')
    #
    #                 while inp != '!}':
    #                     lines.append(inp)
    #                     inp = input('... ')
    #
    #                 self.repl.interpret_multi(lines)
    #             else:
    #                 unknown = True
    #         elif len(cmd) >= 2:
    #             if cmd[0] == 'go':
    #                 if cmd[1] not in self.repls:
    #                     self.start_repl(cmd[1], cmd[2:])
    #
    #                 self.current_repl_name = cmd[1]
    #             elif cmd[0] in ('q', 'close'):
    #                 del self.repls[cmd[1]]
    #             else:
    #                 unknown = True
    #         else:
    #             unknown = True
    #
    #         if unknown:
    #             print('Unknown command: {!r}'.format(inp))
    #
    #     elif inp.startswith('@'):
    #         cur_repl = self.current_repl_name
    #         repl, *args = inp[1:].split()
    #
    #         if repl not in self.repls:
    #             self.start_repl(repl)
    #             self.repls[repl].interpret(' '.join(args))
    #             del self.repls[repl]
    #         else:
    #             self.repls[repl].interpret(' '.join(args))
    #     elif inp.startswith('$'):
    #         self.interpret('@system ' + inp[1:])
    #     else:
    #         try:
    #             self.repl.interpret(inp)
    #         except Exception as e:
    #             print(e)


    def start_repl(self, repl_name, args=()):
        repl = REPL.get_repl_with_name(repl_name)(*args)
        self.repls[repl.name] = repl

    def run(self):
        self.running = True

        while self.running:
            self.interpret(input(self.repl.prompt))
