import os
import yaml
import logging
import argparse

logger = logging.getLogger("laziest")


class Clifier(object):

    defaults = {
        'required': False,
        'nargs': 1
    }

    def __init__(self, config_path, use_base_defaults=False, defaults=None):
        """

        :param config_path:
        :param use_base_defaults:
        :param defaults:
        """
        self.config_path = config_path
        self.config = self.read_config()
        self.defaults = defaults if defaults \
            else self.defaults if use_base_defaults else None

    def create_parser(self):
        """ """
        parser_params = self.config.get('parser', None)
        parser = argparse.ArgumentParser(**parser_params)

        if 'commands' in self.config:
            self.create_commands(self.config['commands'], parser)

        if 'subparsers' in self.config and self.config['subparsers']:
            self.create_subparsers(parser)

        if 'commands' not in self.config and not 'subparser' not in self.config:
            logging.warning("Created cli parser without commands and subparser."
                            "Need to define sections 'commands' and 'subparser'"
                            "in {}.".format(self.config_path))
        return parser

    def apply_defaults(self, commands):
        """ apply default settings to commands """
        for command in commands:
            print(command)
            if 'action' in command and "()" in command['action']:
                command['action'] = eval("self.{}".format(command['action']))
            if command['keys'][0].startswith('-'):
                if 'required' not in command:
                    command['required'] = False

    def create_commands(self, commands, parser):
        """ add commands to parser """
        self. apply_defaults(commands)
        for command in commands:
            keys = command['keys']
            del command['keys']
            parser.add_argument(*keys, **command)

    def create_subparsers(self, parser):
        """ get config for subparser and create commands"""
        subparsers = parser.add_subparsers()
        for name in self.config['subparsers']:
            subparser = subparsers.add_parser(name)
            self.create_commands(self.config['subparsers'][name], subparser)

    def read_config(self):
        """ """
        if not os.path.isfile(self.config_path):
            raise Exception("File does not exist {}".format(
                self.config_path))
        yaml_file = open(self.config_path, 'r')
        conf = yaml.load(yaml_file)
        return conf

    def add_actions(self, actions_list):
        for action in actions_list:
            self.__setattr__(action.__name__, action)
