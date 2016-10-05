"""
Test Runner will receive command line test specifications and component names to execute against
pre-defined py.test.
"""
from config.configmanager import ConfigManager


class TestRunner(ConfigManager):
    def __init__(self):
        super().__init__()
