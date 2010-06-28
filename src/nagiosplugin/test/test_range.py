# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

import unittest
import nagiosplugin.test
from nagiosplugin import range

nagiosplugin.test.path_setup()


class RangeParseTest(unittest.TestCase):

    def test_empty_range_is_zero_to_infinity(self):
        r = range.Range('')
        self.failIf(r.match(-0.1))
        self.failUnless(r.match(0))
        self.failUnless(r.match(1000000))

    def test_explicit_start_end(self):
        r = range.Range('0.5:4')
        self.failIf(r.match(0.4))
        self.failUnless(r.match(0.5))
        self.failUnless(r.match(4))
        self.failIf(r.match(5))

    def test_fail_if_start_gt_end(self):
        self.assertRaises(ValueError, range.Range, u'4:3')

    def test_omit_start(self):
        r = range.Range(u'5')
        self.failIf(r.match(-0.1))
        self.failUnless(r.match(0))
        self.failUnless(r.match(5))
        self.failIf(r.match(5.1))

    def test_omit_end(self):
        r = range.Range(u'7.7:')
        self.failIf(r.match(7.6))
        self.failUnless(r.match(7.7))
        self.failUnless(r.match(1000000))

    def test_start_is_neg_infinity(self):
        r = range.Range(u'~:5.5')
        self.failUnless(r.match(-1000000))
        self.failUnless(r.match(5.5))
        self.failIf(r.match(5.6))

    def test_invert(self):
        r = range.Range(u'@-9.1:2.6')
        self.failUnless(r.match(-9.2))
        self.failIf(r.match(-9.1))
        self.failIf(r.match(2.6))
        self.failUnless(r.match(2.7))


class RangeStrTest(unittest.TestCase):

    def setUp(self):
        self.r = range.Range()

    def test_empty(self):
        self.assertEqual(u'', str(self.r))

    def test_explicit_start_stop(self):
        (self.r.start, self.r.end) = (1.5, 5)
        self.assertEqual(u'1.5:5', str(self.r))

    def test_omit_start(self):
        self.r.end = 6.7
        self.assertEqual(u'6.7', str(self.r))

    def test_omit_end(self):
        self.r.start = -6.5
        self.assertEqual(u'-6.5:', str(self.r))

    def test_neg_infinity(self):
        (self.r.start, self.r.end) = (None, -3.7)
        self.assertEqual(u'~:-3.7', str(self.r))

    def test_invert(self):
        (self.r.invert, self.r.start, self.r.end) = (True, 3, 7)
        self.assertEqual(u'@3:7', str(self.r))


def suite():
    suite = unittest.TestLoader()
    suite.loadTestsFromTestCase(RangeParseTest)
    suite.loadTestsFromTestCase(RangeStrTest)
    return suite

if __name__ == '__main__':
    unittest.main()