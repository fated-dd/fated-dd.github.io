def func():
    def func2():
        return 'fuck you'
    fuck = func2()
    return fuck

print(func())