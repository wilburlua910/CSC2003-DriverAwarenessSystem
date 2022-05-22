from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext = Extension(
    name = "pyblink",
    sources = ["pyblink.pyx"],
    libraries = [
        "blink",
        "wiringPi"
        ],
    library_dirs = ["lib"],
    include_dirs = ["lib"]
)

setup(
    name = "pyblink",
    ext_modules = cythonize([ext])
)