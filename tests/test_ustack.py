import unittest
from copy import copy

from ufpy import UStack


class UStackTestCase(unittest.TestCase):
    def test_init(self):
        s = UStack(1, 1, 2, 3, 5, 8)
        s2 = UStack(*s.elements)
        s3 = UStack(iterable=s2.elements)

        self.assertEqual(s, s2)
        self.assertEqual(s, s3)
        self.assertEqual(s2, s3)

    def test_elements(self):
        s = UStack(1, 1, 2, 3, 5, 8)
        self.assertEqual(s.elements, [1, 1, 2, 3, 5, 8])

        s.elements = 1, 2
        self.assertEqual(s, UStack(1, 2))

        del s.elements
        self.assertEqual(s, UStack())

    def test_top(self):
        s = UStack(1, 1, 2, 3, 5, 8)
        self.assertEqual(s.top, 8)

        s.top = 10
        self.assertEqual(s, UStack(1, 1, 2, 3, 5, 10))

        del s.top
        self.assertEqual(s, UStack(1, 1, 2, 3, 5))

    def test_pop(self):
        s = UStack(1, 1, 2, 3, 5, 8)
        self.assertEqual(s.pop(), 8)
        self.assertEqual(s, UStack(1, 1, 2, 3, 5))

    def test_push(self):
        s = UStack(1, 1, 2, 3, 5, 8)
        self.assertEqual(s.push(2, 1), UStack(1, 1, 2, 3, 5, 8, 2, 1))
        self.assertEqual(s, UStack(1, 1, 2, 3, 5, 8, 2, 1))

    def test_remove(self):
        s = UStack(1, 1, 2, 3, 5, 8)
        self.assertEqual(s.remove(1), UStack(1, 2, 3, 5, 8))
        self.assertEqual(s, UStack(1, 2, 3, 5, 8))

    def test_clear(self):
        s = UStack(1, 1, 2, 3, 5, 8)
        s2 = UStack(1, 1, 2, 3, 5, 8)

        del s2.elements

        self.assertEqual(s.clear(), UStack())
        self.assertEqual(s, s2)

    def test_copy(self):
        # with copy
        s = UStack(1, 1, 2, 3, 5, 8)
        s2 = s.copy()
        s3 = copy(s2)

        self.assertEqual(s, s2)
        self.assertEqual(s, s3)
        self.assertEqual(s2, s3)

        self.assertNotEqual(id(s), id(s2))
        self.assertNotEqual(id(s), id(s3))
        self.assertNotEqual(id(s2), id(s3))

        # without copy
        s4 = s
        s5 = s4

        self.assertEqual(id(s4), id(s5))

    def test_call(self):
        s = UStack(1, 1, 2, 3, 5, 8)

        def f(i, v):
            return v * i

        self.assertEqual(s(f), UStack(0, 1, 4, 9, 20, 40))

    def test_math_operations(self):
        s = UStack(1, 1, 2, 3, 5, 8)
        self.assertEqual(s + 1, UStack(1, 1, 2, 3, 5, 8, 1))
        self.assertEqual(s - 1, UStack(1, 2, 3, 5, 8))
        self.assertEqual(s * 2, UStack(2, 2, 4, 6, 10, 16))
        self.assertEqual(s / 2, UStack(0.5, 0.5, 1, 1.5, 2.5, 4))

    def test_len_and_empty(self):
        s = UStack(1, 1, 2, 3, 5, 8)
        self.assertEqual(len(s), 6)
        self.assertFalse(s.is_empty())
        self.assertTrue(bool(s))

    def test_repr(self):
        s = UStack(1, 1, 2, 3, 5, 8)
        self.assertEqual(repr(s), 's[1, 1, 2, 3, 5, 8]')


if __name__ == '__main__':
    unittest.main()
