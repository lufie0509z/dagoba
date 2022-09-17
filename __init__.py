from unicodedata import name
import unittest

from .test import DbModelTest
from .test_primary_key import PrimaryKeyTest
from .test_eager_query import EagerQueryTest
from .test_lazy_query import LazyQueryTest

def main():
    unittest.main(__name__)


if __name__ == '__main__':
    main()
