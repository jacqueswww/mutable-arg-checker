# mutable-arg-checker
Linter for checking your codebase for potentially dangerous mutable default arguments.

```sh

python3 mac.py

/home/jacques/projects/mutable-arg-checker/bad.py:
line 2: Mutable dict parameter
def test1(a={}):
------------^
/home/jacques/projects/mutable-arg-checker/bad.py:
line 6: Mutable list parameter
def test2(b=[]):
------------^
/home/jacques/projects/mutable-arg-checker/bad.py:
line 10: Mutable dict parameter
def test2(b=dict()):
------------^
/home/jacques/projects/mutable-arg-checker/bad.py:
line 13: Mutable list parameter
def test2(b=list()):
------------^
```
