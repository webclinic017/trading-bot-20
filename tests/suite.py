import unittest

suite = unittest.TestLoader().discover('.')
runner = unittest.TextTestRunner()
runner.run(suite)
