from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("cBoolTable", ["cBoolTable.pyx"]),
				Extension("cBNet", ["cBNet.pyx"]),
				Extension("cTable_Utils", ["cTable_Utils.pyx"])]

setup(
  name = 'Bayesian network stuff',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
