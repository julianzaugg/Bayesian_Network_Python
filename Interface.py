'''
Created on Jan 10, 2012

JUST TESTING!!

@author: julianzaugg
'''
#!/usr/bin/env python
import sys, os
import BNet
import CPT

class Command(object):
    args = []
    def execute(self, args):
        raise NotImplementedError()

def arg(*args, **kw):
    # sugar for arg declaration
    return (args, kw)

class CPT(Command):
    args = [
        arg('-n', dest= 'name',
             nargs = '*', help = "Set name of node, no argument will\
                                        return node name"),
        arg('-p', dest= 'parents',
             nargs = '*', help = "Set parents of node, no argument\
                                        will return parents") ]

    def execute(self, args):
        print args.name, args.parents
        new = CPT(args.name, args.parents)

#****************************************************************************
def commands():
    mod = sys.modules[__name__]
    classes = []
    for attr in [getattr(mod, name) for name in dir(mod)]:
        if Command in getattr(attr, '__bases__', []):
            classes.append(attr)
    print classes
    return classes

def register_commands(arg_parser):  
    cmd_parsers = arg_parser.add_subparsers()
    for cmd in commands():
        # use first line of docstring as help
        help = (cmd.__doc__ or 'no help').strip().splitlines()[0]
        cmd_parser = cmd_parsers.add_parser(cmd.__name__, help=help)
        # add optional command-specific arguments
        for (args, kw) in cmd.args:
            cmd_parser.add_argument(*args, **kw)
        # This is really, really important!
        # Without it we won't know which command to execute.
        cmd_parser.set_defaults(command_class=cmd)
#****************************************************************************

if __name__ == '__main__':
    import argparse
    arg_parser = argparse.ArgumentParser(description = 'Interface to create a Bayesian network')
    arg_parser.add_argument('-v', '--verbose',
        action='store_true', help = 'example global option')
    # register commands
    register_commands(arg_parser)
    # parse args including which command to run
    args = arg_parser.parse_args(sys.argv[1:])
    # create instance of command
    command = args.command_class()
    if args.verbose:
        print 'running', command
    # run it
    command.execute(args)
    