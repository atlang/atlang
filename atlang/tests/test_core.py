"""py.test based unit tests for atlang core"""
import pytest

from .. import Type, TypeFormationError, tycon, is_tycon

class unit_(Type):
  @classmethod
  def validate_idx(cls, idx):
    if idx != ():
      raise TypeFormationError("Index of unit type must be ().")

unit = unit_[()]

def test_unit_construction(): 
  assert isinstance(unit, Type)

def test_unit_idx():
  assert unit.idx == ()

def test_unit_construction_bad_idx():
  with pytest.raises(TypeFormationError):
    unit_[0]

def test_unit_construction_direct():
  with pytest.raises(TypeFormationError):
    unit_(())

def test_unit_eq():
  assert unit == unit

class ty2_(Type):
  pass

ty2 = ty2_[()]

def test_ty2_eq():
  assert ty2 == ty2
  assert not (ty2 != ty2)

def test_ty2_neq():
  assert ty2 != unit
  assert not (ty2 == unit)

def test_is_tycon():
  assert is_tycon(ty2_) and is_tycon(unit_)

def test_tycon():
  assert tycon(ty2) is ty2_ and tycon(unit) is unit_

