
from app.helpers import foo

if __name__ == '__main__':
    
    result = foo()
    print("\nfunction foo with default arguments returned a count of ", result)
    result = foo(1,20)
    print("\nfunction foo with arguments start=1, end=20 returned a count of ", result)
    