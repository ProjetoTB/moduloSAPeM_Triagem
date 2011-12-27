#!/usr/bin/env python
# -*- coding:utf-8 -*-
####
# Author: "Fernando Ferreira" <fferreira@lps.ufrj.br>
#
# Build SAPeM modules based on Base and Forks folders
#
# Usage: build_modules.py [options]
#
# Options:
#  -h, --help    show this help message and exit
#  -t, --tar     create tar files from modules
#  -u, --upload  upload to github download page
###

import sys, os
import shutil
import tarfile
import cStringIO
from distutils.dir_util import copy_tree as cp

class noOpt:
	def __init__(self):
		self.tar = False
		self.update = False

if __name__ == '__main__':
	try:
		from optparse import OptionParser
		parser = OptionParser()
		parser.add_option("-t", "--tar", 
				action='store_true', default=False,
				help="create tar files from modules")
		parser.add_option("-u", "--upload", 
				action='store_true', default=False,
				help="upload to github download page")
		(options, args) = parser.parse_args()
	except ImportError:
		print 'not possible set options'
		options = noOpt()

	modulesDir = u'modules'
	forksDir   = u'forks'
	baseDir    = u'base'
	DIR        = os.path.dirname(os.path.realpath(__file__))
	if not os.path.exists(modulesDir):
		os.makedirs(modulesDir)
	dirDict = dict([(d, os.path.join(DIR, modulesDir, 'moduloSAPeM_%s'%d))
				for d in os.listdir(forksDir) if 'Triagem' in d])

	tarfileDict={}
	for d, v in dirDict.iteritems():
		if os.path.exists(v):
			shutil.rmtree(v)
		os.makedirs(v)
		cp(baseDir, v)
		cp(os.path.join(forksDir, d), v)
		if options.tar:
			tarfilename = os.path.join(DIR, '.'.join([v,'tar','gz']))
			tar=tarfile.open(tarfilename, 'w:gz')
			tar.add(v)
			tar.close()
			tarfileDict[d] = tarfilename
