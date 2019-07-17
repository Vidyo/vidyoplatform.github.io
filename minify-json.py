#!/usr/bin/env python

# minify-json.py
# Created by James Ross 2013/6/26
# ------------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2013 Z2.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ------------------------------------------------------------------------------

import sys
import os
import os.path
import json


################################################################################
def parse_args(argv):
    options = {}
    if len(sys.argv) > 1:
        options['input'] = sys.argv[1]

    if len(sys.argv) > 2:
        options['output'] = sys.argv[2]

    return options


################################################################################
def validate_options(options):
    if not 'input' in options:
        raise RuntimeError("No [input] argument was provided")

    if not (os.path.isfile(options['input']) or os.path.isdir(options['input'])):
        raise TypeError("[input] '" + options['input'] + "' is not a file or directory")

    if 'output' in options and os.path.isdir(options['input']) and not os.path.isdir(options['output']):
        raise TypeError("[output] '" + options['output'] + "' must be a directory because [input] is a directory")


################################################################################
def print_help_and_exit():
    sys.stdout.write("usage: " + os.path.basename(__file__) + " [input] [output]\n")
    sys.stdout.write("Where [input]  => path to json file or directory\n")
    sys.stdout.write("      [output] => path to output file or directory\n\n")
    sys.exit(2)


################################################################################
def print_error_and_exit(message):
    sys.stderr.write(message + "\n")
    sys.exit(1)


################################################################################
def create_path(path):
    abs_path = os.path.abspath(os.path.dirname(path))
    if not os.path.exists(abs_path):
        os.makedirs(abs_path)


################################################################################
def minify_file(input_filepath, output_path):
    try:
        filepath = os.path.abspath(input_filepath)
        json_txt = open(filepath, 'r').read()
        json_mini = json.dumps(json.loads(json_txt), separators=(',', ':'))

        if len(output_path) > 0:
            out_file = os.path.abspath(output_path)
            create_path(out_file)
            open(out_file, 'w').write(json_mini)

        else:
            sys.stdout.write(json_mini)

    except Exception, e:
        sys.stderr.write(str(e) + "\n")


################################################################################
def find_json_files(input_dir):
    search_results = []
    search_root = input_dir
    for root, directories, files in os.walk(search_root):
        for filename in files:
            if os.path.splitext(filename)[1] == '.json':
                relative_path = os.path.relpath(root, search_root)
                search_results.append(os.path.join(relative_path, filename))

    return search_results


################################################################################
def minify_dir(dir_in, dir_out):
    abs_dir_in = os.path.abspath(dir_in)
    files = find_json_files(abs_dir_in)
    for relative_filepath in files:
        file_in = os.path.join(abs_dir_in, relative_filepath)
        file_out = ""
        if len(dir_out) > 0:
            file_out = os.path.join(dir_out, relative_filepath)

        minify_file(file_in, file_out)


################################################################################
options = parse_args(sys.argv)

try:
    validate_options(options)

except Exception, e:
    sys.stderr.write(str(e) + "\n")
    print_help_and_exit()

try:
    output = options['output'] if 'output' in options else ""

    if os.path.isfile(options['input']):
        minify_file(options['input'], output)

    elif os.path.isdir(options['input']):
        minify_dir(options['input'], output)

except Exception, e:
    print_error_and_exit(str(e) + "\n")
