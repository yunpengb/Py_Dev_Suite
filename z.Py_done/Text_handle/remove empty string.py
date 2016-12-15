#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# @version               v1
# @date                  2015-10-10
# @author                Yunpeng
#
# @Copyright 2015 Nokia Networks. All rights reserved.
################################################################################

import sys
import os

a1 = " haha\n"
a2 = " what "

print "type1:remove head empty"
print "[%s]" % a1.lstrip()

print "type2:remove End empty"
print "[%s]" % a1.rstrip()

print "type3:remove both head and End empty str"
print "[%s]" % a1.strip()
