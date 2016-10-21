#!/usr/bin/env python3.4
# coding: utf-8

__all__ = (
    'Shell',
)

import os
import glob
import traceback
import colorama
from importlib.machinery import SourceFileLoader
from collections import OrderedDict

from sluggo.repl import *

colorama.init()


class Shell(REPL):
    def __init__(self, base_repl=None):
        base_repl = sys() or base_repl
        self.repls = OrderedDict()
        self.repls[base_repl.name] = base_repl
        self.cmds = {}

        self.prompt = ''
        self.current_repl_name = base_repl.name
        self.running = False

        self.load_conf()
        self.load_plugins()

    def load_conf(self):
        if os.path.exists(os.path.expanduser(CONF_FILE)):
            with open(CONF_FILE) as conf:
                self.interpret_multi(map(str.strip, conf.readlines()))

    def load_plugins(self):
        pwd = os.getcwd()
        os.chdir(PLUGIN_DIR)

        for plugin_path in glob.glob('*.py'):
            src = SourceFileLoader(os.path.basename(plugin_path), plugin_path)
            src.load_module()

        os.chdir(pwd)

    @property
    def repl(self):
        return self.repls[self.current_repl_name]

    @on(r'\s*')
    def eval_empty(self):
        pass

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

    @on(r'!open\s+(\w+)\s*(.*)')
    def eval_open(self, repl_name, args):
        if repl_name not in self.repls:
            self.start_repl(repl_name, args.split())

    @on(r'!reload')
    def eval_reload(self):
        self.load_conf()
        self.load_plugins()

    @on(r'!alias\s+(\w+)\s+(.*)')
    def eval_alias(self, cmd_name, cmd):
        self.cmds[cmd_name] = cmd

    @on(r'!(\w+)')
    def eval_cmd(self, cmd_name):
        try:
            cmd = self.cmds[cmd_name]
        except KeyError:
            raise REPLError('Unknown command: {!r}'.format(cmd_name))
        else:
            self.interpret(cmd)

    @on(r'@(\w+)\s*(.*)')
    def eval_at(self, repl_name, *cmd):
        cur_repl = self.current_repl_name

        if repl_name not in self.repls:
            self.start_repl(repl_name)
            self.repls[repl_name].interpret(' '.join(cmd))
            del self.repls[repl_name]
        else:
            self.repls[repl_name].interpret(' '.join(cmd))

    @on(r'\$(.+)')
    def eval_sys(self, cmd):
        self.interpret('@sys ' + cmd)

    def eval(self, inp):
        self.repl.interpret(inp)

    def start_repl(self, repl_name, args=()):
        repl_type = REPL.get_repl_with_name(repl_name)
        repl = repl_type(*args)
        self.repls[repl.name] = repl
        repl.init()

    def run(self):
        self.running = True

        while self.running:
            try:
                self.interpret(input(self.repl.prompt))
            except REPLError as e:
                print(colorama.Fore.RED + str(e) + colorama.Fore.RESET)
            except Exception:
                print(colorama.Fore.RED, end='', flush=True)
                traceback.print_exc()
                print(colorama.Style.BRIGHT + '\nIf you think this is an bug, please open an issue:')
                print('https://github.com/felko/sluggo/issues')
                print(colorama.Style.RESET_ALL, end='')

            for repl in self.repls.values():
                repl.update()
