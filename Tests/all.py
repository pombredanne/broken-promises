#!/usr/bin/env python
# Encoding: utf-8
# -----------------------------------------------------------------------------
# Project : OKF - Spending Stories
# -----------------------------------------------------------------------------
# Author : Edouard Richard                                  <edou4rd@gmail.com>
# -----------------------------------------------------------------------------
# License : proprietary journalism++
# -----------------------------------------------------------------------------
# Creation : 29-Oct-2013
# Last mod : 29-Oct-2013
# -----------------------------------------------------------------------------

import unittest

if __name__ == "__main__":
	tests = unittest.TestLoader().discover("collector", "*.py")
	unittest.TextTestRunner(verbosity=2).run(tests)

# EOF
