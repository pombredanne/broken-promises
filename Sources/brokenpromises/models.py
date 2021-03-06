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
# Last mod : 11-Nov-2013
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

import datetime

# -----------------------------------------------------------------------------
#
#    Article
#
# -----------------------------------------------------------------------------
class Article:

	def __init__(self, channel, title=None, url=None, source=None, body=None, 
				 pub_date=None, ref_dates=[], images=[], headline=None, created=None, 
				 *args, **kwargs):
		self.title     = title
		self.url       = url
		self.source    = source
		self.body      = body
		self.pub_date  = pub_date
		self.ref_dates = ref_dates
		self.images    = images
		self.headline  = headline
		self.channel   = channel
		self.created   = created or datetime.datetime.now()

	def __unicode__(self):
		return u"\"%s - %s...\"" % (self.source, self.title[:20])
	def __repr__(self):
		return self.__unicode__()
	def __str__(self):
		return self.__unicode__()

# EOF
