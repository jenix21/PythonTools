# -*- coding:utf-8 -*-

# jdkim, 2014.2.18 (print_stack.py)

# Simple script to convert address-based call stack to symbol-based call stack. 
#   - 'addr2line' have to be in $PATH.
#      ex) android-ndk-r9b/toolchains/arm-linux-androideabi-4.6/prebuilt/linux-x86_64/bin/arm-linux-androideabi-addr2line
#   - 'not stripped shared library' should be in same directory of this script.

import sys
import re
import subprocess

addr2line = 'arm-linux-androideabi-addr2line'
cmd = '{0} -e libcontent_shell_content_view.so {1}'
address_list = list()

def check_addr2line():
	p = subprocess.Popen('which %s' % addr2line, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	ret, _ = p.communicate()
	if len(ret) == 0:
		raise Exception('no addr2line exist, check your ndk toolcahin path.')

def read_log():
    global address_list
    logs = ''
    print ' >>> Paste log containing pc address of shared library, then enter new line, finally Ctrl+D to finish.'

    add_regx = re.compile('[0-9a-f]{8}')
    logs = sys.stdin.readlines()
    if len(logs) == 0:
        raise Exception('empty log')
    for log in logs:
        addr = add_regx.findall(log)
        if len(addr) == 1:
            address_list.append(addr[0])

def print_callstack():
    print ' >>> call stack'
    for addr in address_list:
        p = subprocess.Popen(cmd.format(addr2line, addr), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        ret, _ = p.communicate()
        print '%s (%s)' % (ret.strip(), addr.strip())

def main():
    check_addr2line()
    read_log()
    print_callstack()

if __name__ == '__main__':
    sys.exit(main())
