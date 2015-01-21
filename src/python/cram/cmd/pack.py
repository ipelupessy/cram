##############################################################################
# Copyright (c) 2014, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Cram.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-661100
#
# For details, see https://github.com/scalability-llnl/cram.
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import argparse
from contextlib import closing

import llnl.util.tty as tty
from cram.cramfile import *

description = "Pack a command invocation into a cramfile"

def setup_parser(subparser):
    subparser.add_argument('-n', "--nprocs", type=int, dest='nprocs', required=True,
                           help="Number of processes to run with")
    subparser.add_argument('-f', "--file", dest='file', default='cram.job', required=True,
                           help="File to store command invocation in.  Default is 'cram.job'")
    subparser.add_argument('-e', "--exe", dest='exe', default=USE_APP_EXE,
                           help="Optionally specify the executable name for the cram job.")
    subparser.add_argument('arguments', nargs=argparse.REMAINDER,
                           help="Arguments to pass to executable.")


def pack(parser, args):
    if not args.arguments:
        tty.die("You must supply command line arguments to cram pack.")

    if not args.nprocs:
        tty.die("You must supply a number of processes to run with.")

    if os.path.isdir(args.file):
        tty.die("%s is a directory." % args.file)

    with closing(CramFile(args.file, 'a')) as cf:
        cf.pack(args.nprocs, os.getcwd(), args.arguments, os.environ, exe=args.exe)
