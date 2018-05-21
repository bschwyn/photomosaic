
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
        self.bounds = [self.origin[0] - size//2, self.origin[0] + size//2,
                       self.origin[1] - size//2, self.origin[1] + size//2,
                       self.origin[2] - size//2, self.origin[2] + size//2]
        self.size = size
        self.points = []
        #has range
        #has 8 children <x<y<z, <x<y>z.... how about 0 to 7 in binary

from queue import PriorityQueue

class MyPriorityQueue(PriorityQueue):

    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter +=1

    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item


class Octree():

    def __init__(self, size):
        #bitmask to indicate which nodes are actively used
        #min size --- how many framse
        self.origin = ((size-1)//2, (size-1)//2, (size-1)//2)
        self.root = CubeNode(self.origin, size)
        self.size = size

    #nearest nehbor search within octant

    def special_distance(self, search_point, node):

        x,y,z = search_point
        x0,x1,y0, y1, z0, z1 = node.bounds

        #check the bounds of the octant
        if x < x0:
            newx = x0
        elif x > x1:
            newx = x1
        else:
            newx = x

        if y < y0:
            newy = y0
        elif y > y1:
            newy = y1
        else:
            newy = y

        if z < z0:
            newz = z0
        elif z > z1:
            newz = z

        return self.dist(search_point, (newx, newy, newz))



        #perpendicular quadrant, special distance == distance from edge
        #crosswise quadrant, special distance == one axis the same, others point to 1,1 off


    def find_nearest_point(self, searchpoint):
        q = MyPriorityQueue()
        #put root.origin in queue
        q.put(self.root, self.dist(self.closest_point_within_octant(self.root.origin, searchpoint)))

        while len(q) > 0:
            next_object = q.get()
            if isinstance(next_object, tuple):
                return tuple

                #this is the closest point, because it has a shorter distance
                #if self.dist(searchpoint, next_object) < self.dist(searchpoint, mindistpoint):
                #    mindistpoint = next_object
            else:
                for childnode in next_object.children:
                    if childnode is not None:
                        q.put(childnode, self.special_distance(searchpoint, childnode))
                    for point in childnode.points:
                        q.put(point, self.dist(searchpoint, point))



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

    def dist(self, p1, p2):
        return (p1[0] - p2[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p2[2])**2

    def closest_point_within_octant(self, node, point):
        quadrant_number = self.find_quadrant_number(node, point)
        x = quadrant_number & 1
        y = quadrant_number & 2
        z = quadrant_number & 4
        if x == 1:
            newx = node.origin[0] +1
        else:
            newx = node.origin[0] -1

        if y == 1:
            newy = node.origin[1] +1
        else:
            newy = node.origin[1] -1

        if z == 1:
            newz = node.origin[2] +1
        else:
            newz = node.origin[2] -1

        return (newx, newy, newz)


        #if nochildren / is leaf
    def insert(self, point):
        self.insert_aux(self.root, point)


    def insert_aux(self, root, point):
        #error if point larger than
        if root.size <= 1:
            root.points.append(point)
        #collision detection
        elif point[0] == root.origin[0] or point[1] == root.origin[1] or point[2] == root.origin[2]:
            root.points.append(point)
        else:
            quadrant_number = self.find_quadrant_number(root, point)
            if root.children[quadrant_number]:
                self.insert_aux(root.children[quadrant_number], point)
            else:
                #create new node
                #find out whether x is < or >, #find out whether y is < or >
                new_origin = self.find_new_origin(root, quadrant_number,  root.size//2,point)
                new_node = CubeNode(new_origin, root.size//2)
                root.children[quadrant_number] = new_node
                self.insert_aux(root.children[quadrant_number], point)

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

#x = Octree(16)
#pq = PriorityQueue
#pq.put(x.root, 1)

#Holy fuck, what if the nearest search value is not in the same branch????


#kd tree
#supports orthogonal range searching
#O(n^(1-1/3) + k0 worst case query time,
