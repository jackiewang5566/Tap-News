""" mongodb test service """
import mongodb_client as client

def test_basic():
    """ test basic function of mongodb  """
    db = client.get_db('test')
    db.testCollection.drop()
    assert db.testCollection.count() == 0
    db.testCollection.insert({'test': 1, 'hello': 'world'})
    assert db.testCollection.count() == 1
    db.testCollection.drop()
    assert db.testCollection.count() == 0
    print 'test_basic passed.'

"""
    If this script is run directly through python mongodb_client_test.py, 
__name__(enviromnent variable) will be interpreted as __main__; however, 
if there are other script import mongodb_client_test.py, __name__ will be 
the entry point of the script that import this script, it will not execute 
test_basic() in this case.

"""

if __name__ == "__main__":
    test_basic()
