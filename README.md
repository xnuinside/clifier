### clifier

Clifier is a simple, tiny script to generate Argparse commands and subparsersfrom yaml config file.

All arguments and parameters names same like in Argparser module, 
so you do not need to know new lexic.

Whan you use clifier you don't need to create separate documentation for your users - 
you can just use config.yaml file as doc. 


#### Install

To install clifier - use pip:

    pip install clifier 
    
#### Examples

In folder clifier/examples you can find the example cli with config file. 
Just copy it to you local env and test.


Simple example of yaml config:

    parser:
      prog: 'Clifier Example'
      description: Example for Clifier
    
    commands:
       - keys: ['-v', '--version']
         help: "show Clifier Example version"
         action: show_version()
         default: True
    
    subparsers:
      play:
        - keys: ['game']
          help: Write a name of the gave, what you want to play
    
        - keys: ['-c', '--count']
          help: Put number how much times you want to play
          default: 2
    
      sleep:
        - keys: ['-t', '--time']
          help: Put how much second you want to sleep

### Sections in config file
#### "parser" section 

Used to define args equal to args of argparse.ArgumentParser() 
__init__ method, for example:
    
    - prog
    - description
    - usage
    - epilog and etc 
    
    to know more, look at official Argparse documentation:
    https://docs.python.org/3.6/library/argparse.html#argparse.ArgumentParser

#### "commands" section
    
    commands properties equal to add_argument method
    https://docs.python.org/3.6/library/argparse.html#argparse.ArgumentParser.add_argument 
    
    
    
#### "subparsers" section
    
    name of subparser section element - it's a name, what equals to 
    add_parser() argument "name" of object what returned by 
    add_subparser_method
    
    https://docs.python.org/3.6/library/argparse.html#argparse.ArgumentParser.add_subparsers
    
    it's a Subparser name and it's not showed as argument in parser
   
#### To use Clifier in your code
    
Prepare variable with path to your config file with cli:

    config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "cli.yaml")


Initialise clifier
    
    from clifier import Clifier
    
    cli = clifier.Clifier(config_path, prog_version="0.0.1")

And get parser like standart Argparse parser

    parser = cli.create_parser()
    args = parser.parse_args()
    

That's it!

#### Adding custom actions

You can add to Clifier Custom Argparser Actions with method add_actions():

    cli = clifier.Clifier(config_path)
    cli.add_actions((your_custom_action_1, your_custom_action_2)

To use those actions in Cli, define them in command line config file with "action" property, for example:

    
#### Custom actions defined from box in Clifier

##### show_version

method to create command -v, --version to show program version 
for usage: 

    1. provide arg prog_version to Clifier() or define "version" param in config

        example in config.yaml:
        
        parser:
           prog: 'your prog name'
           version: "0.0.1"
           
        or 
        
        cli = clifier.Clifier(config_path, prog_version="0.0.1")
        
    2. define -v, --version command in cli config:
    
        commands:
           - keys: ['-v', '--version']
             help: "show Clifier Example version"
             action: show_version()
             default: True
    
    
##### check_path_action

This action check exist or not file_path that was provided by user to command line.
