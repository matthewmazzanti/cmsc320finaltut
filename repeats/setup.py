from distutils.core import setup, Extension

module1 = Extension('repeats',
                    sources = ['repeatsmodule.cpp','repeats.cpp'],
                    include_dirs = ['/usr/local/Cellar/seqan/2.3.2/include'],
                    extra_compile_args=['-std=c++14',
                                        '-O3',
                                        '-DNDEBUG',
                                        '-W',
                                        '-Wall',
                                        '-pedantic'])

setup (name = 'repeats',
       version = '0.0',
       description = 'Super Maximal Pair finder',
       ext_modules = [module1])
