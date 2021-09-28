from unittest import TestCase, main
from ingestionpack.controller.example_table import get_example_table

class Test(TestCase):
    def test_get_example_table(self):
        result = get_example_table()
        self.assertEqual(len(result), 10)  # add assertion here

    def test_get_example_table_2(self):
        result=get_example_table()
        self.assertEqual(len(result), 8)  # add assertion here


if __name__ == '__main__':
    main()
