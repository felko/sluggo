#!/usr/bin/env python3.4
# coding: utf-8

import sluggo
from cmd import cmd

import os
import git as git_
from colorama import Fore, Back, Style, init

init()

class git(cmd):
    def __init__(self):
        self.cmd = 'git'
        try:
            self.repo = git_.Repo('.')
        except git_.exc.InvalidGitRepositoryError:
            self.repo = None

    @property
    def prompt(self):
        if self.repo is not None:
            branch = self.repo.active_branch.name
            repo_name = os.path.basename(self.repo.working_dir)

            if self.repo.is_dirty():
                return Back.WHITE + Fore.BLACK + ' ' + repo_name + ' '\
                    + Back.RED + Fore.WHITE + chr(0xE0B0)\
                    + Fore.BLACK + ' ' + chr(0xE0A0) + ' ' + branch + ' '\
                    + Fore.RED + Back.RESET + chr(0xE0B0) + ' '\
                    + Style.RESET_ALL
            else:
                return Back.WHITE + Fore.BLACK + ' ' + repo_name + ' '\
                    + Back.GREEN + Fore.WHITE + chr(0xE0B0)\
                    + Fore.BLACK + ' ' + chr(0xE0A0) + ' ' + branch + ' '\
                    + Fore.GREEN + Back.RESET + chr(0xE0B0) + ' '\
                    + Style.RESET_ALL
        else:
            return 'git> '

    def update(self):
        try:
            self.repo = git_.Repo('.')
        except git_.exc.InvalidGitRepositoryError:
            self.repo = None
