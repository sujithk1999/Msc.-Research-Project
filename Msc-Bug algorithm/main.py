# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 12:01:10 2022

@author: Admin
"""

from Base import *
from ImprovedBug import *
import argparse
import sys

def create_parser():
    parser = argparse.ArgumentParser(prog="main.py",
                                     description='''Implementation of Bug algorithms for V-REP simulator with the sataic obstacle''',
                                     epilog=''' sk ''')

    parser.add_argument('-a', '--algorithm', choices=['ImprovedBug'], help=" Execute the ImprovedBug algorithm ", default='ImprovedBug')
    parser.add_argument('-s', '--speed', type=int, help=" The Speed of roobot wheels ", default=1.0)
    parser.add_argument('-t', '--targetname', type=str, help=" Name of target on scene ", default='target')
    parser.add_argument('-b', '--botname', type=str, help=" Name of bot on scene ", default='Bot')

    return parser


if __name__ == '__main__':

    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    bug = None

    if namespace.algorithm == "ImprovedBug":
        bug = ImprovedBug(target_name=namespace.targetname, bot_name=namespace.botname, wheel_speed=namespace.speed)
    else:
        print("Something goes wrong!")
        exit(-2)

    bug.loop()

