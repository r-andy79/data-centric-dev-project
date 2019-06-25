import unittest
from app import parse_string

class TestParse(unittest.TestCase):
  def test_parse(self):
    params = " test , abcd"
    output = ["test", "abcd"]
    self.assertEqual(parse_string(params),output, "Should be parsed array")

if __name__ == '__main__':
  unittest.main()