"""
run `setup.py` by `python setup.py build_ext --inplace`
"""

from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy as np

build_name = "pygkdtree_v9"

setup(ext_modules=cythonize(
    Extension(
        build_name, 
        sources=["{}.pyx".format(build_name)], 
        language="c++", 
        include_dirs=[np.get_include()], 
        library_dirs=[], 
        libraries=[], 
        extra_compile_args=[], 
        extra_link_args=[]
    ), 
    compiler_directives={"language_level": 3}, 
))