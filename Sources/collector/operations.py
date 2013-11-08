#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : Broken Promises
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 05-Nov-2013
# Last mod : 08-Nov-2013
# -----------------------------------------------------------------------------
import collector.channels
import collector.utils
import nltk
import os
import dateparser

class Collector:

	@classmethod
	def retrieve_referenced_dates(cls, text):
		references = []
		dates = dateparser.find_dates(text)
		for date in dates:
			date_obj, date_row, date_position = date
			reference = {
				"date"           : date_obj,
				"extract"        : cls.get_sentence(text, date_row),
				"extracted_date" : date_row
			}
			references.append(reference)
		return references

	@classmethod
	def get_sentence(cls, text, search):
		# TODO : DIY
		tokenizer = nltk.data.load(
			"file:%s" % (
				os.path.join(os.path.dirname(__file__), "nltk_data/tokenizers/punkt/english.pickle")))
		for sentence in tokenizer.sentences_from_text(text):
			if search in sentence:
				break
			sentence = None
		return sentence

	def pre_filter(self, results):
		# articles with no body
		results = filter(lambda _: _.body, results)
		return results

# -----------------------------------------------------------------------------
#
#    Collect Articles
#
# -----------------------------------------------------------------------------
class CollectArticles(Collector):

	def __init__(self, channels, year, month=None, day=None):
		self.channels = [channel() for channel in collector.channels.perform_channels_import(channels)]
		self.date     = (year, month, day)

	def run(self):
		articles = []
		# retrieve articles from channels
		for channel in self.channels:
			articles += channel.get_articles(*self.date)
		# filters
		articles = self.pre_filter(articles)
		# search dates in the body articles
		for result in articles:
			result.ref_dates = self.retrieve_referenced_dates(result.body)
		return articles

class RefreshArticles(Collector):

	def __init__(self, articles):
		self.articles = articles

	def run(self):
		articles = self.articles
		# filter
		self.pre_filter(articles)
		# parsing date
		for article in articles:
			article.ref_dates = self.retrieve_referenced_dates(article.body)
		return articles

# -----------------------------------------------------------------------------
#
# TESTS
#
# -----------------------------------------------------------------------------
import unittest

class TestOperations(unittest.TestCase):
	'''Test Class'''

	def test_get_articles(self):
		channels = (
			"collector.channels.nytimes",
			# "collector.channels.guardian",
		)
		# channels  = collector.utils.get_available_channels()

		collector = CollectArticles(channels, "2014", "1")
		results   = collector.run()
		print 
		print "results:", len(results)
		assert len(results) > 0
		for result in results:
			assert result.ref_dates, "%s : %s" % (result, result.url)

	def test_retrieve_referenced_dates(self):
		dates = (
			("10 October 2013"       , (2013, 10, 10)),
			("10 october, 2013"      , (2013, 10, 10)),
			("10 by October 2013"    , (2013, 10, 10)),
			("10 by October, 2013"   , (2013, 10, 10)),
			("Jan 2014"              , (2014, 1, None)),
			("10 in October 2013"    , (2013, 10, 10)),
			("10 in October, 2013"   , (2013, 10, 10)),
			("10 of October 2013"    , (2013, 10, 10)),
			("10 of October, 2013"   , (2013, 10, 10)),
			("10th October 2013"     , (2013, 10, 10)),
			("10th by October 2013"  , (2013, 10, 10)),
			("10th by October, 2013" , (2013, 10, 10)),
			("10th in october 2013"  , (2013, 10, 10)),
			("10th in October, 2013" , (2013, 10, 10)),
			("10th of October 2013"  , (2013, 10, 10)),
			("10th of October, 2013" , (2013, 10, 10)),
			("2013-10-10"            , (2013, 10, 10)),
			("2013/10/10"            , (2013, 10, 10)),
			("August, 2013"          , (2013, 8, None)),
			("2013"                  , (2013, None, None)),
		)

		text  = " bla bli 123. Bu \n pouet12 \n 12432 ".join([_[0] for _ in dates])
		refs  = CollectArticles.retrieve_referenced_dates(text)
		date_found = [_['extracted_date'] for _ in refs]
		for searched_date in dates:
			try:
				ref = filter(lambda _: _["extracted_date"] == searched_date[0], refs)[0]
			except:
				raise Exception("\"%s\" not found in document" % searched_date[0])
			assert ref['extracted_date'] in searched_date[0]
			assert ref['date']           == searched_date[1]
			date_found.remove(ref['extracted_date'])
		assert len(refs) == len(dates), "%s != %s\nToo much : %s" % (len(refs), len(dates), date_found)

if __name__ == "__main__":
	# unittest.main()
	suite = unittest.TestLoader().loadTestsFromTestCase(TestOperations)
	unittest.TextTestRunner(verbosity=2).run(suite)
