#!/usr/bin/env python3.4
# coding: utf-8

__all__ = (
    'Shell',
)

from collections import OrderedDict

from sluggo.repl import *


class Shell:
    def __init__(self, base_repl=None):
        base_repl = system() or base_repl
        self.repls = OrderedDict()
        self.repls[base_repl.name] = base_repl

        self.current_repl_name = base_repl.name
        self.running = False

    @property
    def repl(self):
        return self.repls[self.current_repl_name]

    def eval(self, input):
        unknown = False

        if input.startswith('!'):
            cmd = input[1:].split()

            if len(cmd) == 1:
                if cmd[0] == 'exit':
                    self.running = False
                elif cmd[0] in ('q', 'quit'):
                    del self.repls[self.current_repl_name]

                    if not self.repls:
                        self.running = False
                    else:
                        self.current_repl_name = list(self.repls.values())[-1].name
                else:
                    unknown = True
            elif len(cmd) >= 2:
                if cmd[0] == 'go':
                    if cmd[1] not in self.repls:
                        self.start_repl(cmd[1], cmd[2:])

                    self.current_repl_name = cmd[1]
                elif cmd[0] in ('q', 'close'):
                    del self.repls[cmd[1]]
                else:
                    unknown = True
            else:
                unknown = True

            if unknown:
                print('Unknown command: {!r}'.format(input))

        elif input.startswith('@'):
            cur_repl = self.current_repl_name
            repl, *args = input[1:].split()

            if repl not in self.repls:
                self.start_repl(repl)

            self.repls[repl].eval(' '.join(args))
        elif input.startswith('$'):
            self.eval('@system ' + input[1:])
        else:
            try:
                self.repl.eval(input)
            except Exception as e:
                print(e)


    def start_repl(self, repl_name, args=()):
        repl = REPL.get_repl_with_name(repl_name)(*args)
        self.repls[repl.name] = repl

    def run(self):
        self.running = True

        while self.running:
            self.eval(input(self.repl.prompt))
