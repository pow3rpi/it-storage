from unittest import TestSuite, TestLoader, TextTestRunner

from tests.auth import log_in, sign_up, password, update
from tests.blog import link, tutorial, post


class TestProtocol:

    def __init__(self):
        self.suite = TestSuite()
        self.loader = TestLoader()
        self.runner = TextTestRunner()

    def run_all(self):
        print('Starting all tests...')
        tests = self.loader.discover('./tests/', pattern='*.py')
        self.runner.run(tests)

    def test_auth_service(self):
        suite = self.suite
        suite.addTests([
            self.loader.loadTestsFromModule(sign_up),
            self.loader.loadTestsFromModule(log_in),
            self.loader.loadTestsFromModule(password),
            self.loader.loadTestsFromModule(update)
        ])
        self.runner.run(suite)

    def test_blog(self):
        suite = self.suite
        suite.addTests([
            self.loader.loadTestsFromModule(post),
            self.loader.loadTestsFromModule(link),
            self.loader.loadTestsFromModule(tutorial)
        ])
        self.runner.run(suite)
