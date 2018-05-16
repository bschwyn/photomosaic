
#fastest way to find closest point to a given point in data array

#repeated search for nearest neighbor for a lot of points



class binary_search_tree():
    def __init__(self):
        pass

    def search(self, root, key):
        if root == None or root.key == key:
            return root
        elif root.key < key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)


class CubeNode():
    #properties: children 0..7, origin,

    def __init__(self, origin, size):
        self.children = [None,None, None, None, None,None, None,None]
        self.origin = origin
        self.size = size
        self.points = []
        #has range
        #has 8 children <x<y<z, <x<y>z.... how about 0 to 7 in binary

class Octree():

    def __init__(self, size):
        #bitmask to indicate which nodes are actively used
        #min size --- how many framse
        self.origin = ((size-1)//2, (size-1)//2, (size-1)//2)
        self.root = CubeNode(self.origin, size)
        self.size

    def search(self, root, point):
        if point[0] == root.origin[0] or point[1] == root.origin[1] or point[2] == root.origin[2] or root.size <=1:
            #find nearest point


            mindist = 255 ** 2 + 255 ** 2 + 255 ** 2
            for (x2,y2,z2) in root.points:
                x,y,z = point
                dist = (x2 - x) ** 2 + (y2 - y) ** 2 + (z2 - z) ** 2
                if dist < mindist:
                    mindist = dist
            return mindist

        else:
            quandrant_number = self.find_cubic_quadrant(root, point)
            if not quandrant_number:
                return None
            child = root.children[quandrant_number]
            return self.search(child, point)

    def find_quadrant_number(self,root, point):
        x_0, y_0, z_0 = root.origin
        x,y,z = point
        if x < x_0:
            ones =0
        else:
            ones = 1
        if y < y_0:
            twos = 0
        else:
            twos = 1
        if z < z_0:
            threes = 0
        else:
            threes = 1
        quadrant = ones*1 + twos*2 + threes*4
        return quadrant

        #if nochildren / is leaf

    def insert(self, root, point):
        #error if point larger than
        if root.size <= 1:
            root.points.append(point)
        #collision detection
        elif point[0] == root.origin[0] or point[1] == root.origin[1] or point[2] == root.origin[2]:
            root.points.append(point)
        else:
            quadrant_number = self.find_quadrant_number(root, point)
            if root.children[quadrant_number]:
                self.insert(root.children[quadrant_number], point)
            else:
                #create new node
                #find out whether x is < or >, #find out whether y is < or >
                new_origin = self.find_new_origin(root, quadrant_number,  root.size//2,point)
                new_node = CubeNode(new_origin, root.size//2)
                root.children[quadrant_number] = new_node
                self.insert(root.children[quadrant_number], point)

    def find_new_origin(self,root, quadrant_number, size, point):

        x,y,z = root.origin
        morex = quadrant_number & 1
        morey = quadrant_number & 2
        morez = quadrant_number & 4
        if morex:
            newx = x + size//2
        else:
            newx = x - size//2
        if morey:
            newy = y + size//2
        else:
            newy = y - size//2
        if morez:
            newz = z + size//2
        else:
            newz = z - size//2

        if point[0] == x:
            newx = x
        if point[1] == y:
            newy = y
        if point[2] == z:
            newz = z

        return (newx, newy, newz)

#tests

def octree_insert_test():
    x = Octree(16)
    x.insert(x.root, (5,6,7))
    x.insert(x.root, (4,14,11))
    x.insert(x.root, (15,15,15))
    x.insert(x.root, (0,0,0))

#octree_insert_test()



#kd tree
#supports orthogonal range searching
#O(n^(1-1/3) + k0 worst case query time,
