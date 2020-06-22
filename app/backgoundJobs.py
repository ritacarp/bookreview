
def foo(start=0, end=10):
    i=0
    for x in range(start, end):
        i += 1
        print("In test worker:  x = ", x)
    return(i)


if __name__ == '__main__':
    
    result = foo()
    print("\nfunction foo with default arguments returned a count of ", result)
    result = foo(1,20)
    print("\nfunction foo with arguments start=1, end=20 returned a count of ", result)
    