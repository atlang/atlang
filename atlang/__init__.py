"""atlang: An extensible static type system inside Python."""
import ast # Python standard library's abstract syntax module
import inspect # for accessing source code for functions
import textwrap # for stripping leading spaces

import cypy # helper functions
import six # Python 2-3 compatibility, e.g. metaclasses
# TODO: semver

class UsageError(Exception):
  pass 

class TypeError(Exception):
  def __init__(self, message, location):
    Exception.__init__(message)
    self.location = location
  # TODO: error pretty-printing

class TypeFormationError(Exception):
  pass

class _TypeMetaclass(type): # here, type is Python's "type" builtin
  def __getitem__(self, idx):
    if _contains_ellipsis(idx): return _construct_incty(self, idx)
    else: return _construct_ty(self, idx)

def _contains_ellipsis(idx):
  if idx is Ellipsis: return True
  elif isinstance(idx, tuple):
    for item in idx:
      if item is Ellipsis: return True
  return False 

def _construct_incty(tycon, inc_idx):
  tycon.validate_inc_idx(inc_idx)
  return IncompleteType(tycon, inc_idx)

def _construct_ty(tycon, idx):
  tycon.validate_idx(idx)
  return tycon(idx, True)

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

  @classmethod
  def validate_inc_idx(cls, inc_idx):
    pass 

  def __eq__(self, other):
    return tycon(self) is tycon(other) and self.idx == other.idx

  def __ne__(self, other):
    return not self.__eq__(other)

  def ana_FunctionDef_TopLevel(self, tree, static_env):
    raise NotImplementedError("ana_FunctionDef_TopLevel not implemented.")

  @classmethod
  def syn_idx_FunctionDef_TopLevel(self, tree, static_env):
    raise NotImplementedError("syn_idx_FunctionDef_TopLevel not implemented.")

  def __call__(self, f):
    raise TypeError("Non-FnType used as a top-level function decorator.")

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

  def __call__(self, f):
    if issubclass(self.tycon, FnType):
      (ast, static_env) = _reflect_func(f)
      idx = self.tycon.syn_idx_FunctionDef_TopLevel(ast, static_env)
      return Fn(ast, static_env, _construct_ty(self.tycon, idx))
    else:
      raise TypeError("Incomplete non-FnType used as a top-level function decorator.")

def tycon(ty):
  """Returns the tycon of the provided type or incomplete type ."""
  if isinstance(ty, Type):
    return ty.__class__
  elif isinstance(ty, IncompleteType):
    return ty.tycon
  else:
    raise UsageError("Argument to tycon is not a type or incomplete type.")

def is_tycon(x):
  """Indicates whether the provided value is a tycon."""
  return issubclass(x, Type)

class FnType(Type):
  """Base class for atlang function types."""
  def __call__(self, f):
    (tree, static_env) = _reflect_func(f)
    self.ana_FunctionDef_TopLevel(tree, static_env)
    return Fn(tree, static_env, self)

class Fn(object):
  """All atlang functions are instances of Fn."""
  def __init__(self, tree, static_env, ty):
    self.tree = tree
    self.static_env = static_env
    self.ty = ty

def _reflect_func(f):
  source = textwrap.dedent(inspect.getsource(f))
  tree = ast.parse(source).body[0] # ast.parse produces a Module initially
  return (tree, StaticEnv.from_func(f))

class StaticEnv(object):
  def __init__(self, closure, globals):
    self.closure = closure
    self.globals = globals

  def __getitem__(self, item):
    try: return self.closure[item]
    except KeyError: return self.globals[item]

  @classmethod
  def from_func(cls, f):
    closure = _func_closure(f)
    globals = f.func_globals
    return cls(closure, globals)

def _func_closure(f):
  closure = f.func_closure
  if closure is None: return {}
  else: return dict(zip(f.func_code.co_freevars, (c.cell_contents for c in closure)))

