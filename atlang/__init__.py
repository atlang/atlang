"""atlang: An extensible static type system inside Python."""
import ast # Python standard library's abstract syntax module
import inspect # for accessing source code for functions

import cypy # helper functions
import six # Python 2-3 compatibility, e.g. metaclasses
# TODO: semver

class TypeError(Exception):
  def __init__(self, message, location):
    Exception.__init__(message)
    self.location = location
  # TODO: error pretty-printing

class TypeFormationError(Exception):
  pass

class _TypeMetaclass(type): # here, type is Python's "type" 
  def __getitem__(self, idx):
    if _contains_ellipsis(idx):
      return IncompleteType(self, idx)
    else:
      self.validate_idx(idx)
      return self(idx, True)

def _contains_ellipsis(idx):
  # TODO: implement this
  return False

@six.add_metaclass(_TypeMetaclass)
class Type(object):
  """Base class for atlang types.

  An atlang type is an instance of atlang.Type.
  An atlang tycon is a subclass of atlang.Type.
  """
  def __init__(self, idx, ok=False):
    if not ok:
      raise TypeFormationError(
        "Types should not be constructed directly. Use tycon[idx].")
    self.idx = idx

  @classmethod
  def validate_idx(cls, idx):
    pass

  def __eq__(self, other):
    return tycon(self) is tycon(other) and self.idx == other.idx

  def __ne__(self, other):
    return not self.__eq__(other)

def tycon(ty):
  """Returns the tycon of the provided type (does not check whether ty is a type)."""
  return ty.__class__

def is_tycon(x):
  """Indicates that the provided object is a tycon."""
  return issubclass(x, Type)

class IncompleteType(object):
  """Represents an incomplete type, used for literal forms.

  An incomplete type is constructed by providing an index 
  containing one or more ellipses (so the constructor need 
  not typically be called directly):
    tycon[a, ..., b]
  """
  def __init__(self, tycon, inc_idx):
    self.tycon = tycon
    self.inc_idx = inc_idx

class FnType(Type):
  """Base class for atlang function types."""
  def __call__(self, *args):
     # TODO: figure this out
    pass

class Fn(object):
  """All atlang functions are instances of Fn."""
  def __init__(self, ty, ast, static_env):
    # TODO: figure this out
    pass

  #class _Visitor(ast.Visitor):
    # TODO: 
    #pass
