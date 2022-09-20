from os.path import dirname, basename, isfile, split
import glob

# add simple modules
modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not basename(f).startswith('__')] # exclude __init__.py

# add complex modules
modules = glob.glob(dirname(__file__)+"/*/__init__.py")
__all__ += [ split(dirname(f))[1] for f in modules ]

__all__.sort()
