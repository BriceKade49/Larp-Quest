# Brice Kade
# ETGG 1803
# 2/25/19

import math

class Vector(object):
    """ A basic vector class """
    
    def __init__(self, *args):
        """ Initialize vector instance of vector(1, 2, 3) """
        self.data = []            
        for value in args:
            self.data.append(float(value))
        self.dim = len(args)
        if self.dim == 2:
            self.__class__=Vector2
        elif self.dim == 3:
            self.__class__=Vector3

    def __len__(self):
        """ DO not access directly use len(v)
Returns an interger dimension"""
        return self.dim

    def __getitem__(self, index):
        """ Returns float value at this postition """
        return self.data[index]

    def __str__(self):
        """ Returns a string representation of the vector """
        s = "<vector" + str(self.dim) + ": "
        for i in range(self.dim):
            s += str(self[i])
            if i < self.dim - 1:
                s += ", "
        s += ">"
        return s

    def __setitem__(self, index, newval):
        """ Needs index as int
New val must be able to convert to float
Changes value"""
        self.data[index]=float(newval)

    def __eq__(self, other):
        """ :param other: any value
:return: a boolean
True if other is a vector of the same dimension and value """
        if isinstance(other, Vector) and self.dim == other.dim:
            for i in range(self.dim):
                if self[i] != other[i]:
                    return False
            return True
        return False

    def copy(self):
        """ Create a deep copy of the vector """
        v = Vector(*self.data)
        v.__class__ = self.__class__
        return v

    def __mul__(self, scalar):
        """ Multiplies vector by a scalar, with the scalar on the right: v * x
scalar is int or float
returns a copy of the vector with all values multiplied"""
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            n = "Vector" + str(self.dim)
            raise TypeError("You can only multiply this " + n + " and a scalar. You attempted to multiply by " + str(scalar) + ".")
        r = self.copy()
        for i in range(self.dim):
            r[i] *= scalar
        return r

    def __rmul__(self, scalar):
        """ Like mul but multiplies it on the left """
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            n = "Vector" + str(self.dim)
            raise TypeError("You can only multiply this " + n + " and a scalar. You attempted to multiply by " + str(scalar) + ".")
        r = self.copy()
        for i in range(self.dim):
            r[i] *= scalar
        return r

    def __add__(self, other_vec):
        """ This takes 2 vectors and adds them together"""
        if isinstance(other_vec, Vector) and self.dim == other_vec.dim:
            r = self.copy()
            for i in range(self.dim):
                r[i]+=other_vec[i]
            return r

    def __sub__(self, other_vec):
        """ This takes 2 vectors and subtracts them"""
        if isinstance(other_vec, Vector) and self.dim == other_vec.dim:
            r = self.copy()
            for i in range(self.dim):
                r[i]-=other_vec[i]
            return r
    def __neg__(self):
        """this each value in the vector negative"""
        for i in range(self.dim):
            self.data[i]*= -1
        return self.copy()

    def __truediv__(self, scalar):
        """this divides each value of vector by a scalar or number"""
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            n = "Vector" + str(self.dim)
            raise TypeError("You can only divide this " + n + " and a scalar. You attempted to divide by " + str(scalar) + ".")
        r = self.copy()
        for i in range(self.dim):
            r[i] /= scalar
        return r
    
    @property
    def is_zero(self):
        """Returns True if this Vector is identically the zero Vector of the appropriate dimension, False otherwise"""
        for value in self:
            if value != 0.0:
                return False
            return True

    @property
    def mag(self):
        """returns the lenth of the vector with a 2-norm"""
        dim = 0
        for i in range(self.dim):
            dim = dim + (abs(self.data[i])**2)
        return dim ** .5
    
    @property
    def mag_squared (self):
        """returner the mag without squaring the final value so the value is more a whole number"""
        dim = 0
        for i in range(self.dim):
            dim = dim + (abs(v[i]))**2
        return dim

    @property
    def normalize(self):
        """Returns a unit Vector in the same direction as the given vector"""
        return self* (1/self.mag)

    @property
    def i(self):
        """Returns a tuple of the coordinates of the Vector given converted to integers"""
        Tuple = []
        for i in self:
            Tuple.append(int(i))
        return tuple(Tuple)
        
class Vector2 (Vector):
    """ This class is for 2 dimetional vectors and sets the x and y of the vectors"""
    def __init__(self,x,y):
        super().__init__(x,y)
    @property
    def x(self):
        return self[0]
    
    @x.setter
    def x(self,newVal):
        self[0]=float(newVal)

    @property
    def y(self):
        return self[1]
    
    @y.setter
    def y(self,newVal):
        self[1]=float(newVal)

    @property
    def degrees(self):
        """Returns the degree measurment of the vector"""
        val = math.degrees(math.atan2(self.y, self.x))
        return val

    @property
    def degrees_inv(self):
        """Returns the iverted oposite degree measurment of the given vector"""
        val = math.degrees(math.atan2(-self.y, self.x))
        return val

    @property
    def redians(self):
        """Returns the radian measurment of the given vector"""
        val = math.atan2(self.y, self.x)
        return val
    
    @property
    def redians_inv(self):
        """Returns the inverse or oposite radian measurment of the given vector"""
        val = math.atan2(-self.y, self.x)
        return val

    @property
    def perpendicular(self):
        """Turns the vector that is at a 90 degree angle to the given vector"""
        if self.x == 0:
            return Vector2(self.y, self.x)
        if self.y == 0:
            return Vector2(self.y, self.x)
        return Vector2(-self.y, self.x)
    
            
class Vector3 (Vector):
    """ This class is for 3 dimetional vectors and set the x, y, and z of the vector"""
    def __init__(self,x,y,z):
        super().__init__(x,y,z)
        
    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self,newVal):
        self[0]=float(newVal)

    @property
    def y(self):
        return self[1]
    
    @y.setter
    def y(self,newVal):
        self[1]=float(newVal)

    @property
    def z(self):
        return self[2]
    
    @z.setter
    def z(self,newVal):
        self[2]=float(newVal)


def dot(v1, v2):
    """ Gets the dot product bedtween vectors v1 and v2 """
    val = 0

    if v1.dim == v2.dim:
        for i in range(v1.dim):
            if i == 0:
                x= v1[i] * v2[i]
            else:     
                y = x + (v1[i] * v2[i])
                x = y
    else:
        print("vector lenths not the same")
    return x

def cross_product(v,w):
    """Returns vector3 cross Product of 2 given vectors"""
    return (v.mag*w.mag*math.sin(math.acos((dot(v,w)/ (v.mag* w.mag)))))
                                 
def polar_to_Vector2(r, rad, inv=True):
    """Returns an either iverted or non iverted vector2 polar coordinates"""
    x = r* math.cos(rad)
    y = r * math.sin(rad)
    if inv == True:
        y = -y
    return Vector2(x, y)
def pnorm(v, p=2):
    """ Returns 2-norm of vector """
    total = 0
    for i in range(v.dim):
        total += (abs(v[i])) ** p
    return total ** (1/p)

if __name__ == "__main__":
    # This test runs only when running this module directly (F5 in Idle or
    # the play button in pycharm).
    v = Vector(1, 2, 3)
    w = Vector(4, 5, 6)
    z = v + w
    print(z) # <Vector3: 5.0, 7.0, 9.0>
    #print("v + 5 =", v + 5) # TypeError: You can only add another
    # Vector3 to this Vector3 (You passed
    # '5'.)
    q = v - w
    print(q) # <Vector3: -3.0, -3.0, -3.0>
    a = v * -2
    print(a) # <Vector3: -2.0, -4.0, -6.0>
    a = -2 * v
    print(a) # <Vector3: -2.0, -4.0, -6.0>
    b = a + (v + w)
    print(b) # <Vector3: 3.0, 3.0, 3.0>
    d = v + (v + v) + w
    print(d) # <Vector3: 7.0, 11.0, 15.0>
    n = -v
    print(n) # <Vector3: -1.0, -2.0, -3.0>
    s = Vector2(3, -2)
    print(s) # <Vector2: 3.0, -2.0)
    print(s.x) # 3.0
    t = Vector(3, -2)
    print(t) # <Vector2: 3.0, -2.0>
    print(t.y) # -2.0
    print(s == t) # True
    print(isinstance(v,Vector))
    print(isinstance(v,Vector2))
    print(isinstance(v,Vector3))


