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
# Last mod : 31-Oct-2013
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


import optparse
from brokenpromises.operations import CollectArticles
import brokenpromises.channels
from bson.json_util import dumps
import sys

oparser = optparse.OptionParser(usage ="\n./%prog [options] year \n./%prog [options] year month\n./%prog [options] year month day")
oparser.add_option("-C", "--nocache", action="store_true", dest="nocache",
	help = "Prevents from using the cache", default=False)
oparser.add_option("-f", "--channelslistfile", action="store", dest="channels_file",
	help = "Use this that as channels list to use", default=None)
oparser.add_option("-c", "--channels", action="store", dest="channels_list",
	help = "channels list comma separated", default=None)
oparser.add_option("-m", "--mongodb", action="store", dest="mongodb_uri",
	help = "uri to mongodb instance to persist results", default=None)
oparser.add_option("-d", "--drop", action="store_true", dest="mongodb_drop",
	help = "drop the previous articles from database before", default=False)
oparser.add_option("-o", "--output", action="store", dest="output_file",
	help = "Specify  a file to write the export to. If you do not specify a file name, the program writes data to standard output (e.g. stdout)", default=None)

options, args = oparser.parse_args()
assert len(args) > 0 and len(args) <= 3

if options.output_file:
	sys.stdout = open(options.output_file, 'a')

channels = brokenpromises.channels.get_available_channels()
if options.channels_file:
	with open(options.channels_file) as f:
		channels = [line.replace("\n", "") for line in f.readlines()]
if options.channels_list:
	channels = options.channels_list.split(",")

results = CollectArticles(channels, *args).run()

#  MONGO
if options.mongodb_uri:
	from pymongo import MongoClient
	from urlparse import urlparse

	client     = MongoClient(options.mongodb_uri)
	db         = client[urlparse(options.mongodb_uri).path.split("/")[-1]]
	collection = db['articles']

	if options.mongodb_drop:
		collection.remove()

	for article in results:
		previous = collection.find_one({"url" : article.url})
		if not previous:
			collection.insert(article.__dict__)
		else:
			collection.update({'_id':previous['_id']}, dict(previous.items() + article.__dict__.items()))

# OUTPUT
print dumps([_.__dict__ for _ in results])
print >> sys.stderr, "%d articles collected." % (len(results))
exit()

# EOF
