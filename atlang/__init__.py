"""atlang: An extensible static type system inside Python."""
import ast # Python standard library's abstract syntax module
import inspect # for accessing source code for functions

import cypy # helper functions
import six # Python 2-3 compatibility, e.g. metaclasses
# TODO: semver

class TypeError(Exception):
  def __init__(self, message, location):
    pass # TODO: figure this out

class TypeFormationError(Exception):
  def __init__(self, message):
    pass # TODO: figure this out

class Type(object):
  """Base class for atlang types.

  An atlang type is an instance of atlang.Type.
  An atlang tycon is a subclass of atlang.Type.
  """
  def __init__(self, idx):
    self.idx = idx

  def __eq__(self, other):
    # TODO: Is this all I have to implement for equality?
    return self.idx == other.idx

# TODO: set this up as the metaclass
class _TypeMetaclass(object):
  def __getitem__(self, idx):
    # TODO: get this working
    pass

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

  class _Visitor(ast.Visitor):
    # TODO: 
    pass
