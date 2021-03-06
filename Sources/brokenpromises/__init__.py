#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : GNU General Public License
# -----------------------------------------------------------------------------
# Creation : 28-Oct-2013
# Last mod : 12-Nov-2013
# -----------------------------------------------------------------------------
# This file is part of Broken Promises.
# 
#     Broken Promises is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     Broken Promises is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with Broken Promises.  If not, see <http://www.gnu.org/licenses/>.

from models import Article
import os
import importlib

ENVIRONMENT_VARIABLE = "BP_SETTINGS"

class Settings:

	def __init__(self):
			try:
				settings_module = os.environ[ENVIRONMENT_VARIABLE]
			except KeyError or not settings_module:
				raise Exception("Settings are not configured. You must define the environment variable '%s'" % (ENVIRONMENT_VARIABLE))
			mod = importlib.import_module(settings_module)
			for setting in dir(mod):
				if setting == setting.upper():
					setattr(self, setting, getattr(mod, setting))

	def __getitem__(self, name): return getattr(self, name)

settings = Settings()

# EOF
