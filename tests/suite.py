from unittest import TestLoader, TextTestRunner
from unittest.suite import TestSuite

suite: TestSuite = TestLoader().discover('.')
runner: TextTestRunner = TextTestRunner()
runner.run(suite)
