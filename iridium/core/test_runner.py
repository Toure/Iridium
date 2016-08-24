"""
Test Runner will receive command line test specifications and component names to execute against
pre-defined py.test.
"""
from iridium.config.config import Config


class TestRunner(Config):
    def __init__(self):
        super().__init__()
