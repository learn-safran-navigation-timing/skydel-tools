#!/usr/bin/python3

import sys

class SnmpSetException(Exception):
  def __init__(self, message):
    self.message = message
    super().__init__(self.message)

class SnmpSetNotWritable(SnmpSetException):
  def __init__(self):
    super().__init__("not-writable")

class SnmpSetWrongType(SnmpSetException):
  def __init__(self):
    super().__init__("wrong-type")

class SnmpSetWrongLength(SnmpSetException):
  def __init__(self):
    super().__init__("wrong-length")

class SnmpSetWrongValue(SnmpSetException):
  def __init__(self):
    super().__init__("wrong-value")

class SnmpSetInconsistentValue(SnmpSetException):
  def __init__(self):
    super().__init__("inconsistent-value")

class SnmpPass:
  def __init__(self, base_oid):
    self.base_oid = base_oid
    self.entries = dict() # key is sub_oid, value is a getter/setter tuple

  # getter must return a (type as string, value) tuple
  # setter must take a type as string and a value as string as argument
  def add_custom_entry(self, sub_oid, getter, setter = None):
    self.entries[sub_oid] = (getter, setter)

  def get_sub_oid(self, full_oid):
    if full_oid.startswith(self.base_oid):
      return full_oid[len(self.base_oid):]
    return None

  def get_entry(self, full_oid):
    sub_oid = self.get_sub_oid(full_oid)
    if sub_oid is None or sub_oid not in self.entries:
      return None
    return self.entries[sub_oid]

  def print_get(self, full_oid, entry):
    if entry is None or entry[0] is None:
      return False
    else:
      (t, value) = entry[0]()
      print(full_oid)
      print(t)
      print(value)
      return True    

  def get(self, full_oid):
    entry = self.get_entry(full_oid)
    return self.print_get(full_oid, entry)    

  def getnext(self, requested_oid):
    sub_oid = self.get_sub_oid(requested_oid)
    full_oid = None
    entry = None
    if sub_oid is not None:
      it = iter(sorted(self.entries.keys()))
      prev = None
      while True:
        cur = next(it, None)
        if cur is None or cur > sub_oid:
          break
        prev = cur
    elif len(self.entries) > 0:
      cur = sorted(self.entries.keys())[0]
    if cur is not None:
      full_oid = self.base_oid + cur
      entry = self.entries[cur]
    return self.print_get(full_oid, entry)

  def set(self, full_oid, t, value):
    entry = self.get_entry(full_oid)
    if entry is None or entry[1] is None:
      print("not-writable")
      return False
    try:
      entry[1](t, value)
      return True
    except SnmpSetException as e:
      print(e.message)
      return False

  def run_persist(self):
    while True:
      line = sys.stdin.readline()
      if not line:
         break
      line = line.strip()
      if line == 'PING':
        print('PONG')
      elif line == 'get':
        full_oid = sys.stdin.readline().strip()
        if not self.get(full_oid):
          print('NONE')
      elif line == 'getnext':
        requested_oid = sys.stdin.readline().strip()
        if not self.getnext(requested_oid):
          print('NONE')
      elif line == 'set':
        full_oid = sys.stdin.readline().strip()
        typevalue = sys.stdin.readline().strip().split()
        if self.set(full_oid, typevalue[0], typevalue[1]):
          print('DONE')
      sys.stdout.flush()

  def run_passthrough(self, argv):
    if argv[1] == '-g':
      self.get(argv[2])
    elif argv[1] == '-n':
      if len(argv) < 3:
        oid = ""
      else:
        oid = argv[2]
      self.getnext(oid)
    elif argv[1] == '-s':
      self.set(argv[2], argv[3], argv[4])

