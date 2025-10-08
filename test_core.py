import unittest
from run import retrieve,calc
class Tests(unittest.TestCase):
 def test_retrieval(self): self.assertEqual(retrieve('profit margin',['unrelated','profit margin increased'])[0][0],1)
 def test_safe_math(self): self.assertAlmostEqual(calc('subtract ; 10 ; 3',[]),7)
if __name__=='__main__':unittest.main()
