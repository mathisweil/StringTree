class STNode:
    def __init__(self,d):
        self.data = d
        self.left = self.right = self.mid = None
        self.mult = 0
        self.dlistPtr = None
        self.parent = None
    
    # update child and parent pointer of child
    def updateChild(self, oldChild, newChild):
        if newChild != None:
            newChild.parent = self
        if self.mid == oldChild:
            self.mid = newChild
        elif self.left == oldChild:
            self.left = newChild
        elif self.right == oldChild:
            self.right = newChild
        else:
            raise Exception("updateChild error")

    # performs BST search for d starting from d. If d is not in the
    # tree, it returns the parent node of where it should have been
    def bin_search(self, d):
        if self.data == d: return self
        if self.data > d: 
            if self.left == None: return self
            return self.left.bin_search(d)
        if self.data < d: 
            if self.right == None: return self
            return self.right.bin_search(d)
        assert(0) # should not get here    

    # prints the node's data and multiplicity
    def __str__(self):
        return "("+str(self.data)+", "+str(self.mult)+")"   

    # returns string corresponding to node
    def strFromTop(self):
        ptr = self
        s = str(self.data)
        while ptr.parent != None and ptr.parent.mid != ptr:
            ptr = ptr.parent
        if ptr.parent == None: return s
        return ptr.parent.strFromTop()+s
   
    # prints the node and all its children in a string
    def strTree(self):  
        st = "("+str(self.data)+", "+str(self.mult)+")"
        if self.left == self.mid == self.right == None: return st
        st += " -> ["
        if self.left != None:
            st += self.left.strTree()
        else: st += "□"
        if self.mid != None:
            st += ", "+self.mid.strTree()
        else: st += ", □"
        if self.right != None:
            st += ", "+self.right.strTree()
        else: st += ", □"
        return st + "]"
    
class StringTree:
    def __init__(self):
        self.root = None
        self.size = 0
        self.dlist = DLinkedList()
        
    def __str__(self):
        if self.root == None: return "empty"
        return self.root.strTree()

    def add(self,st):
        if st == "": return
        dlistPtr = self.updateDList(st)
        if self.root == None: 
            self.root = STNode(st[0])
        ptr = self.root
        for i in range(len(st)):
            char = st[i]
            found_node = ptr.bin_search(char)
            if char < found_node.data:
                found_node.left = STNode(char)
                found_node.left.parent = found_node
                ptr = found_node.left
            elif char > found_node.data:
                found_node.right = STNode(char)
                found_node.right.parent = found_node
                ptr = found_node.right
            else:
                ptr = found_node
            # after the ith character is put into place, we move ptr
            # one level below 
            if i < len(st)-1:
                if ptr.mid == None:
                    ptr.mid = STNode(st[i+1])
                    ptr.mid.parent = ptr
                ptr = ptr.mid
        ptr.mult += 1
        if ptr.mult == 1: 
            ptr.dlistPtr = dlistPtr
        self.size += 1
    
    def addAll(self,A):
        for x in A: self.add(x)

    def printElems(self):
        ptr = self.dlist.head
        st = ""
        while ptr != None:
            st += ptr.data
            if ptr.next != None:
                st += ", "
            ptr = ptr.next
        print(st)

    # returns the smallest string in the tree (None if tree empty)
    def min(self):
        if self.root == None: return None
        return self._min(self.root).strFromTop()

    # returns the lexicographically minimal node in the tree rooted at node
    def _min(self, node):
        ptr = node
        while True: 
            while ptr.left != None: ptr = ptr.left
            if ptr.mult > 0: return ptr 
            ptr = ptr.mid
            
    # returns the largest string in the tree (None if tree empty)
    def max(self):
        if self.root == None: return None
        return self._max(self.root).strFromTop()
    
    # returns the lexicographically maximal node in the tree rooted at node
    def _max(self, node):
        ptr = node
        while True:
            while ptr.right != None:
                ptr = ptr.right
            if ptr.mid != None:
                ptr = ptr.mid
            else:
                return ptr

    # returns the number of times that string st is stored in the tree
    def count(self, st):
        ptr = self._getStrNode(st)
        if ptr == None:
            return 0
        return ptr.mult

    # returns the string node of the string st if
    # st is in the tree, otherwise returns None
    def _getStrNode(self, st):
        ptr = self.root
        if ptr == None or st == "":
            return None
        for i in range(len(st)):
            char = st[i]
            ptr = ptr.bin_search(char)
            if char < ptr.data or char > ptr.data:
                return None
            else:
                if i < len(st) - 1:
                    if ptr.mid == None:
                        return None
                    ptr = ptr.mid
        if ptr.mult == 0:
            return None
        return ptr
    
    # insert st in doubly linked list and return pointer to new list node
    # inefficient version
    def updateDList(self, st):
        if self.dlist.length == 0:
            return self.dlist.insertLeft(st,None)
        ptr = self.dlist.head
        while ptr != None and ptr.data < st:
            ptr = ptr.next
        if ptr == None:
            return self.dlist.append(st)
        if ptr.data == st: return None
        return self.dlist.insertLeft(st,ptr)
        
    # returns the smallest string in the tree
    # that is larger than st. If no such string exists, return None
    def succ(self, st):
        ptr = self._succ(st)
        if ptr == None:
            return None
        return ptr.strFromTop()

    # returns the string node of the successor
    def _succ(self, st):
        ptr = self.root
        if ptr == None:
            return None
        if st == "":
            return self._min(self.root)
        for i in range(len(st)):
            char = st[i]
            ptr = ptr.bin_search(char)
            if char < ptr.data:
                return self._min(ptr)
            elif char > ptr.data:
                return self._next(ptr)
            else:
                if i < len(st) - 1:
                    if ptr.mid == None:
                        break
                    ptr = ptr.mid
        return self._nextNode(ptr)

    # returns the next string node in the tree rooted at node
    def _nextNode(self, ptr):
        if ptr.mid:
            return self._min(ptr.mid)
        elif ptr.right:
            return self._min(ptr.right)
        else:
            return self._next(ptr)

    # returns next string node in the tree rooted at node by 
    # going up the tree
    def _next(self, ptr):
        while ptr.parent:
            if ptr.parent.mid == ptr:
                ptr = ptr.parent
                if ptr.right:
                    return self._min(ptr.right)
            elif ptr.parent.left == ptr:
                ptr = ptr.parent
                if ptr.mult > 0:
                    return ptr
                return self._min(ptr.mid)
            else:
                ptr = ptr.parent
        return None
        
    # returns the largest string in the tree
    # that is smaller than st. If no such string exists, return None
    def pred(self, st): 
        # TODO
        return None

    # removes one occurrence of string st from the tree and returns None
    # if st does not occur in the tree then it returns without changing the tree
    # it updates the size of the tree accordingly
    def remove(self, st):
        ptr = self._getStrNode(st)
        if ptr:
            self.size -= 1
            ptr.mult -= 1
            # the string remains in the tree
            if ptr.mult > 0:
                return None
            else:
                # remove the string from the dlist
                self.dlist.remove(ptr.dlistPtr)
                ptr.dlistPtr = None
                # remove every nodes that needs to be removed
                while ptr.mid == None and ptr.mult == 0:
                    # the node is the root
                    if ptr == self.root:
                        self._removeRoot()
                        break
                    else:
                        self._removeNode(ptr)
                    ptr = ptr.parent
        return None
    
    # remove the node ptr from the tree
    def _removeNode(self, ptr):
        # there are 4 cases to consider
        # 1. the node has no left or right child
        if ptr.left == ptr.right == None:
            ptr.parent.updateChild(ptr, None)
        # 2. the node has a right child
        elif ptr.left == None:
            ptr.parent.updateChild(ptr, ptr.right)
        # 3. the node has a left child
        elif ptr.right == None:
            ptr.parent.updateChild(ptr, ptr.left)
        # 4. the node has a right and a left child
        else:
            minRNode = ptr.right
            while minRNode.left != None:
                minRNode = minRNode.left
            # replace the data of ptr with that of the min node
            ptr.data = minRNode.data
            if minRNode.mid:
                ptr.mid = minRNode.mid
                ptr.mid.parent = ptr
            ptr.mult = minRNode.mult
            ptr.dlistPtr = minRNode.dlistPtr
            # bypass the min node
            minRNode.parent.updateChild(minRNode, minRNode.right)

    # remove root of the tree
    def _removeRoot(self):
        parentRoot = STNode(None)
        parentRoot.left = self.root
        self.root.parent = parentRoot
        self._removeNode(self.root)
        self.root = parentRoot.left
        if self.root:
            self.root.parent = None
    
    # insert st in doubly linked list and return pointer to new list node
    # efficient version
    def updateDList2(self, st):
        # find successor string node of st
        ptr = self._succ(st)
        # st greater than all strings in the tree or equal to the
        # lexicographically largest one
        if ptr == None:
            if self.max() == st:
                return None
            return self.dlist.append(st)
        # st already in tree
        if ptr.dlistPtr.prev and ptr.dlistPtr.prev.data == st:
            return None
        # insert st at left of successor
        return self.dlist.insertLeft(st, ptr.dlistPtr)

class DNode:
    def __init__(self, d, n, p):
        self.data = d
        self.next = n
        self.prev = p

    def __str__(self):
        return str(self.data)
        
class DLinkedList:
    def __init__(self):
        self.head = self.tail = None
        self.length = 0

    # inserts a node to the left of n with data d and returns it. 
    # If it is an empty list, it does not matter what n is, 
    # we create just one node.
    def insertLeft(self, d, n):
        self.length += 1
        
        if self.length == 1: 
            self.head = DNode(d, None, None)
            self.tail = self.head
            return self.head

        np = n.prev
        n.prev = DNode(d, n, np)
        if np == None:
            self.head = n.prev
        else:
            np.next = n.prev
        return n.prev

    # inserts node with d at tail of list and returns it
    def append(self, d):
        if self.length == 0:
            return self.insertLeft(d,None)
        self.length += 1
        self.tail.next = DNode(d, None, self.tail)
        self.tail = self.tail.next
        return self.tail
        
    # removes node n off the list
    def remove(self, n): 
        self.length -= 1
        if n.prev == n.next == None:
            self.head = self.tail = None
            return
        if n.prev == None:
            n.next.prev = None
            self.head = n.next
            return
        if n.next == None:
            n.prev.next = None
            self.tail = n.prev
            return
        n.prev.next = n.next
        n.next.prev = n.prev

    def __str__(self):
        if self.head == None: 
            return "empty"
        st = "-"
        ptr = self.head
        while ptr != None:
            st += "-> "+str(ptr)+" "
            ptr = ptr.next
        return st+"|"