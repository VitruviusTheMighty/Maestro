class simple:

    def __init__(self):
        self.x = 1
        self.y = 2
        self.z = [3, 4]

class s:
    x = 1
    y = 2
    z = [3, 4]



a = simple()
b = simple()


a.z.append(10)
print(a.z)
print(b.z)

c = s()
d = s()
c.z.append(10)
print(c.z)
print(d.z)