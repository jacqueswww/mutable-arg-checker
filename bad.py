
def test1(a={}):
    pass


def test2(b=[]):
    pass


def test2(b=dict()):
    pass

def test2(b=list()):
    pass


mutable_dict = {}
def test2(b=mutable_dict):
    pass

