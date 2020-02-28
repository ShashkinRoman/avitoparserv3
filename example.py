
def test_func(a: list = None, b: int = 0) -> (list, int):
    """
    jhjhjk
    :param a:
    :param b:
    :return:
    """
    if type(a) is not list:
        a = []
    return a, b

# TODO: sdfasdfasdf
#  sfgdsfgdsf
#  erwerwerqwer
# sdfsdfs

a = {1,2}
b = {2,3}
a ^ b
Out[4]: {1, 3}
a = [1,2,2,2,3]
set(a)
Out[6]: {1, 2, 3}
b = [2,2,3,3,2,2]
set(a) ^ set(b)
Out[8]: {1}