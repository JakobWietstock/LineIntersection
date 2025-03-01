from typing import TypeVar, Self

"""
AVL-Tree script

This Script implements a self balancing Binary Tree (AVL) allowing for insertion, removal and retrieval of at least
ordinal data with a worstcase runtime of log(n).

Interaction with the tree is handled via the AVLTree Class which offers functions to insert, remove, and find objects
To initialize a new Tree the user needs to provide a list of key-value pairs:
example [(key0, value0), (key1, value1), ...]

In addition a comparator method and an equals method able to compare two keys are required

for numerical keys default methods are provided.

Example call for creation of a new AVL tree: 
My_Tree = AVLTree(elements=[(0.0, value0), (1.0, value1), (3.5, value2)], comparator=None, equals=None):
"""


class TreeObject:
    """
    Class describing the nodes of the avl tree Saves each Key value pair at it appropriate place in the tree, and
    ensures that the treee remains balanced.

    Attributes:
    -----------
        key: T
            Ordinal object used to sort the tree nodes to structure the binary tree.
        value: U
            The data to be saved in the tree.
        tree: AvlTree
            The AvlTree-object the node is a part of.
        left_child: TreeObject
            Left child of the current tree node. An Object is sorted as a left child of another, when the comparator
            returns true.
        right_child: TreeObject
            Right child of the current tree node. A node is sorted as a left child of another, when th comparator
            returns false.
        parent: TreeObject
            The predecessor of the current tree node. The current node is either the left_child or right_child of its
            parent. The root of the Tree has None as its parent.
        comparator: staticmethod -> bool
            Method that the determines the ordinal relationships of two tree nodes by comparing their keys.
        equals: staticmethod -> bool
            Method tht determines whether two nodes are considered the same by comparing their key. When the method
            returns true the two nodes are considered to be the same.


    Methods:
    --------
        insert(obj: Self): None
            Inserts obj into the tree at the appropriate position.
        remove(key: T): None
            Remove the node with "key" from the tree.
        remove_pair(key: T, value: U): None
            Removes the node with the key-value-pair with "key" and "value" from the tree.
        replace_self(substitute: Self): None
            Removes self from the tree while preserving the tree structure.
        find_rightmost(): TreeObject
            Finds the rightmost node in own subtree.
        find_leftmost(): TreeObject
            Finds the leftmost node in own subtree.
        substitute_right(): None
            Removes self from tree structure if the current node is the right child of its parent.
        substitute_left(): None
            Removes self from tree structure if the current node is the left child of its parent.
        check_balance(): int
            Checks the balance of the subtree having the current node as its root.
        check_height():  int
            Checks the height of the subtree having the current node as its root.
        height_left(): int
            Checks the height of the left subtree of the current node.
        height_right(): int
            Checks the height of the right subtree of the current node.
        simple_rot_right(): None
            Rotation to the right of the subtree with the current node as root. This is done the keep the tree balanced.
        simple_rot_left(): None
            Rotation to the left of the subtree with the current node as root. This is done the keep the tree balanced.
        find_highest(self): Self
            Finds and returns the node with the greatest key in the subtree.
        pop_highest(self): Self
            Finds, returns and removes the node with the greatest key in the subtree.
        find_lowest(self): Self
            Finds and returns the node with the lowest key in the subtree.
        pop_lowest(self): Self
            Finds, returns and removes the node with the lowest key in the subtree.
        find_neighbors(self, key: T): Self
            Finds the next greater and next lower nodes to the node with key "key".
        find_left_neighbor(self, key: T): Self
            Finds the next lower node to the node with key "key".
        find_right_neighbor(self, key: T): Self
            Finds the next greater node to the node with key "key".
        find_left_neighbor_by_pair(self, key: T, value: U): Self
            Finds the next lower node to the node with key-value-pair with key "key" and "value".
        find_right_neighbor_by_pair(self, key: T, value: U): Self
            Finds the next greater node to the node with key-value-pair with key "key" and "value".
        is_in(self, key: T): bool
            Checks whether a node with key "key" is in the subtree including teh current node.
        print_tree(self): None
            Prints the subtree below and including the current node structure to the console.
    """
    T = TypeVar('T')
    U = TypeVar('U')

    def __init__(self, value: U, key: T, tree, comparator: staticmethod, equals: staticmethod):
        """
        :param value: U
            value for the tree node.
        :param key: T
            key for the tree node.
        :param tree: AvlTree
            the Avl Tree the node is part of.
        :param comparator: staticmethod
            a method to determine the order of two keys.
        :param equals: staticmethod
            a method to check two keys for equality.
        """
        self.key = key
        self.value = value
        self.tree = tree
        self.left_child = None
        self.right_child = None
        self.parent = None
        self.comparator = comparator
        self.equals = equals

    def insert(self, obj: Self) -> None:
        """
        Inserts a given TreeObject at the appropriate position in the tree
        :param obj: TreeObject
            The tree object to be inserted into the tree.
        :return: Nothing
        """
        if self.comparator(key1=obj.key, key2=self.key):
            if self.equals(key1=obj.key, key2=self.key):
                if obj.value is self.value:
                    return
            elif self.left_child is None:
                self.left_child = obj
                obj.parent = self
            else:
                self.left_child.insert(obj=obj)
        else:
            if self.right_child is None:
                self.right_child = obj
                obj.parent = self
            else:
                self.right_child.insert(obj=obj)
        balance = self.check_balance()
        if balance < -1:
            self.simple_rot_right()
        elif balance > 1:
            self.simple_rot_left()

    def remove(self, key: T) -> None:
        """
        Removes the TreeObject with the provided key from the tree.
        :param key: T
            The key of the tree node to be removed.
        :return: Nothing
        """
        if self.equals(key1=self.key, key2=key):
            if self.right_child is None and self.left_child is None:
                if self.parent is None:
                    self.tree.root = None
                else:
                    self.replace_self(substitute=None)
            elif self.left_child is not None:
                substitute = self.left_child.find_rightmost()
                substitute.substitute_right()
                self.replace_self(substitute=substitute)
            else:
                substitute = self.right_child.find_leftmost()
                substitute.substitute_left()
                self.replace_self(substitute=substitute)
        else:
            if self.comparator(key1=self.key, key2=key):
                if self.left_child is not None:
                    self.left_child.remove(key)
            else:
                if self.right_child is not None:
                    self.right_child.remove(key)
        balance = self.check_balance()
        if balance < -1:
            self.simple_rot_right()
        if balance > 1:
            self.simple_rot_left()

    def remove_pair(self, key: T, value: U) -> None:
        """
        Removes the key-value pair with the provided key and value from the tree. This function was added for
         the line intersection algorithm, since keys can be non-unique in the status structure.
        :param key: T
            The key of the TreeObject to be removed.
        :param value: U
            The value of the TreeObject to be removed.
        :return: Nothing
        """
        if self.equals(key1=self.key, key2=key) and self.value is value:
            if self.right_child is None and self.left_child is None:
                if self.parent is None:
                    self.tree.root = None
                else:
                    self.replace_self(None)
            elif self.left_child is not None:
                substitute = self.left_child.find_rightmost()
                substitute.substitute_right()
                self.replace_self(substitute)
            else:
                substitute = self.right_child.find_leftmost()
                substitute.substitute_left()
                self.replace_self(substitute)
        else:
            if self.comparator(key1=self.key, key2=key):
                if self.left_child is not None:
                    self.left_child.remove(key)
            else:
                if self.right_child is not None:
                    self.right_child.remove(key)
        balance = self.check_balance()
        if balance < -1:
            self.simple_rot_right()
        if balance > 1:
            self.simple_rot_left()

    def replace_self(self, substitute: Self) -> None:
        """
        The Tree object replaces its spot in the tree with the provided substitute. This is part of the removal process.
        :param substitute: TreeObject
            The TreeObject taking the spot of the current node.
        :return: Nothing
        """
        if substitute is not None:
            substitute.parent = self.parent
        if self.parent is None:
            self.tree.root = substitute
        if self.left_child is not None and self.left_child.key != substitute.key:
            substitute.left_child = self.left_child
            self.left_child.parent = substitute
        if self.right_child is not None and self.right_child.key != substitute.key:
            substitute.right_child = self.right_child
            self.right_child.parent = substitute
        if self.left_child is not None and self.parent is not None and \
                self.equals(key1=self.parent.left_child.key, key2=self.key):
            self.parent.left_child = substitute
        elif self.parent is not None:
            if self.parent.right_child is self:
                self.parent.right_child = substitute
            else:
                self.parent.left_child = substitute

    def find_rightmost(self) -> Self:
        """
        Finds the rightmost node in own subtree.

        :return: TreeObject
            The rightmost object in the subtree.
        """
        if self.right_child is None:
            return self
        else:
            return self.right_child.find_rightmost()

    def find_leftmost(self) -> Self:
        """
        Finds the leftmost node in own subtree.

        :return: TreeObject
            The leftmost object in the subtree.
        """
        if self.left_child is None:
            return self
        else:
            return self.left_child.find_leftmost()

    def substitute_right(self) -> None:
        """
        removes self from tree structure if the current node is the right child of its parent.
        This is part of the removal process.
        :return: Nothing
        """
        if self.parent.right_child is self:
            if self.left_child is not None:
                self.left_child.parent = self.parent
                self.parent.right_child = self.left_child
            else:
                self.parent.right_child = None

    def substitute_left(self) -> None:
        """
        removes self from tree structure if the current node is the left child of its parent.
        This is part of the removal process.
        :return: Nothing
        """
        if self.parent.left_child is self:
            if self.right_child is not None:
                self.right_child.parent = self.parent
                self.parent.left_child = self.right_child
            else:
                self.parent.left_child = None

    def check_balance(self) -> int:
        """
        Checks the balance of the subtree having the current node as its root.
        :return: int
            The balance of the subtree.
        """
        return self.height_right() - self.height_left()

    def check_height(self) -> int:
        """
        Checks the height of the subtree having the current node as its root.
        :return: int
            The height of the subtree.
        """
        return max(self.height_left(), self.height_right())

    def height_left(self) -> int:
        """
        Checks the height of the left subtree of the current node.
        :return: int
            height of the left subtree
        """
        if self.left_child is not None:
            return 1 + self.left_child.check_height()
        else:
            return 0

    def height_right(self) -> int:
        """
        Checks the height of the right subtree of the current node.
        :return: int
            height of the right subtree
        """
        if self.right_child is not None:
            return 1 + self.right_child.check_height()
        else:
            return 0

    def simple_rot_right(self) -> None:
        """
        Rotation to the right of the subtree with the current node as root. This is done the keep the tree balanced.
        :return: Nothing
        """
        if self.parent is None:
            self.tree.root = self.left_child
        new_left = self.left_child.right_child
        self.left_child.parent = self.parent
        if self.parent is not None:
            if self.parent.right_child is self:
                self.parent.right_child = self.left_child
            else:
                self.parent.left_child = self.left_child
        self.left_child.right_child = self
        self.parent = self.left_child
        self.left_child = new_left
        if new_left is not None:
            new_left.parent = self

    def simple_rot_left(self) -> None:
        """
        Rotation to the left of the subtree with the current node as root. This is done the keep the tree balanced.
        :return: Nothing
        """
        if self.parent is None:
            self.tree.root = self.right_child
        new_right = self.right_child.left_child
        self.right_child.parent = self.parent
        if self.parent is not None:
            if self.parent.right_child is self:
                self.parent.right_child = self.right_child
            else:
                self.parent.left_child = self.right_child
        self.right_child.left_child = self
        self.parent = self.right_child
        self.right_child = new_right
        if new_right is not None:
            new_right.parent = self

    def find_highest(self) -> Self:
        """
        Finds and returns the node with the greatest key in the subtree.

        :return: U
            The value of the TreeObject with the greatest Key
        """
        if self.right_child is None:
            return self.value
        else:
            return self.right_child.find_highest()

    def pop_highest(self) -> Self:
        """
        Finds, returns and removes the node with the greatest key in the subtree.
        :return: U
             The value of the TreeObject with the greatest Key
        """
        if self.right_child is None:
            if self.parent is not None:
                self.parent.right_child = self.left_child
            else:
                self.tree.root = None
            return self
        else:
            return self.right_child.pop_highest()

    def find_lowest(self) -> Self:
        """
        Finds and returns the node with the lowest key in the subtree.
        :return: TreeObject
            The value of the TreeObject with the smallest key.
        """
        if self.left_child is None:
            return self.value
        else:
            return self.left_child.find_lowest()

    def pop_lowest(self) -> Self:
        """
        Finds, returns and removes the node with the lowest key in the subtree.
        :return: TreeObject
            The value of the TreeObject with the smallest key.
        """
        if self.left_child is None:
            if self.parent is not None:
                self.parent.left_child = self.right_child
            else:
                self.tree.root = self.right_child
            if self.right_child is not None:
                self.right_child.parent = self.parent
            return self.value
        else:
            return self.left_child.pop_lowest()

    def find_neighbors(self, key: T) -> Self:
        """
        Finds the next greater and next lower nodes to the node with the provided key.
        :param key: T
            The key of the TreeObject for which the neighbors are wanted.
        :return: TreeObject
            The TreeObjects with the next grater and next smaller keys.
        """
        try:
            left = self.find_left_neighbor(key=key).value
        except AttributeError:
            left = None
        try:
            right = self.find_right_neighbor(key=key).value
        except AttributeError:
            right = None
        return left, right

    def find_left_neighbor(self, key: T) -> Self:
        """
        Finds the node with the next lower key to the node with the provided key.
        :param key: T
            The key of the TreeObject for which the left neighbor are wanted.
        :return: TreeObject
            The TreeObject with next smaller key.
        """
        if self.equals(key1=key, key2=self.key):
            if self.left_child is not None:
                return self.left_child.find_rightmost()
            elif self.parent is not None and self.parent.right_child is self:
                return self.parent
            elif self.parent is not None and self.parent.left_child is self:
                if self.parent.parent is not None and self.parent.parent.right_child is self.parent:
                    return self.parent.parent
        elif self.comparator(key1=key, key2=self.key):
            if self.left_child is not None:
                return self.left_child.find_left_neighbor(key=key)
        elif not self.comparator(key1=key, key2=self.key):
            if self.right_child is not None:
                return self.right_child.find_left_neighbor(key=key)
        return None

    def find_right_neighbor(self, key: T) -> Self:
        """
        Finds the node with the next greater key to the node with the provided key.
        :param key: T
            The key of the TreeObject for which the right neighbor are wanted.
        :return: TreeObject
            The TreeObject with next greater key.
        """
        if self.equals(key1=key, key2=self.key):
            if self.right_child is not None:
                return self.right_child.find_leftmost()
            elif self.parent is not None and self.parent.left_child is self:
                return self.parent
            elif self.parent is not None and self.parent.right_child is self:
                if self.parent.parent is not None and self.parent.parent.left_child is self.parent:
                    return self.parent.parent
        elif self.comparator(key1=key, key2=self.key):
            if self.left_child is not None:
                return self.left_child.find_right_neighbor(key=key)
        elif not self.comparator(key1=key, key2=self.key):
            if self.right_child is not None:
                return self.right_child.find_right_neighbor(key=key)
        return None

    def find_left_neighbor_by_pair(self, key: T, value: U) -> Self:
        """
        Finds the node with the next lower key to the node with the provided key-value pair. This function was added for
        the line intersection algorithm, since keys can be non-unique in the status structure.
        :param key: T
            The key of the TreeObject for which the left neighbor are wanted.
        :param value: U
            The value of the TreeObject for which the left neighbor are wanted.
        :return: TreeObject
            The TreeObject with next smaller key.
        """
        if self.equals(key1=key, key2=self.key) and value is self.value:
            if self.left_child is not None:
                return self.left_child.find_rightmost()
            elif self.parent is not None and self.parent.right_child is self:
                return self.parent
            elif self.parent is not None and self.parent.left_child is self:
                if self.parent.parent is not None and self.parent.parent.right_child is self.parent:
                    return self.parent.parent
        elif self.comparator(key1=key, key2=self.key):
            if self.left_child is not None:
                return self.left_child.find_left_neighbor_by_pair(key=key, value=value)
        elif not self.comparator(key1=key, key2=self.key):
            if self.right_child is not None:
                return self.right_child.find_left_neighbor_by_pair(key=key, value=value)
        return None

    def find_right_neighbor_by_pair(self, key: T, value: U) -> Self:
        """
        Finds the node with the next greater key to the node with the provided key-value pair. This function
        was added for the line intersection algorithm, since keys can be non-unique in the status structure.
        :param key: T
            The key of the TreeObject for which the right neighbor are wanted.
        :param value: U
            The value of the TreeObject for which the right neighbor are wanted.
        :return: TreeObject
            The TreeObject with next greater key.
        """
        if self.equals(key1=key, key2=self.key) and value is self.value:
            if self.right_child is not None:
                return self.right_child.find_leftmost()
            elif self.parent is not None and self.parent.left_child is self:
                return self.parent
            elif self.parent is not None and self.parent.right_child is self:
                if self.parent.parent is not None and self.parent.parent.left_child is self.parent:
                    return self.parent.parent
        elif self.comparator(key1=key, key2=self.key):
            if self.left_child is not None:
                return self.left_child.find_right_neighbor_by_pair(key=key, value=value)
        elif not self.comparator(key1=key, key2=self.key):
            if self.right_child is not None:
                return self.right_child.find_right_neighbor_by_pair(key=key, value=value)
        return None

    def is_in(self, key: T) -> bool:
        """
        Checks whether a node with the provided key is in the subtree including the current node.
        :param key: T
            The key of the object that is to be found.
        :return: bool
            True if a TreeObject with the key is found, False otherwise.
        """
        if self.equals(key1=key, key2=self.key):
            return True
        else:
            if self.comparator(key1=key, key2=self.key):
                if self.left_child is not None:
                    return self.left_child.is_in(key=key)
            else:
                if self.right_child is not None:
                    return self.right_child.is_in(key=key)
        return False

    def print_tree(self) -> None:
        """
        Prints the subtree below and including the current node structure to the console.
        :return: Nothing
        """
        print(self.key, self.value)
        if self.left_child is not None:
            print("left:")
            self.left_child.print_tree()
        else:
            print(None)
        if self.right_child is not None:
            print("right:")
            self.right_child.print_tree()
        else:
            print(None)
        print("--------------")


class AvlTree:
    """
    Wrapper for the AVL Tree Contains the root of the Tree, as well as the comparators for the key of the tree
    allows for the standard interactions with the tree such as Insertion and removal of elements or lists of elements.

    Attributes:
    ----------
        root: TreeObject
            Root-node of the AVL-Tree
        comparator: Method, optional
            Method to allow ordinal placement of keys of tree nodes, if no Method is given a default comparator is used.
        equals: method, optional
            Method to determine equality between tree nodes, if no method is given a default method is used.

    Methods:
    -------
        default_comparator(key1: float, key2: float): bool
            Determines whether key1 is smaller than key2.
        default_equals(key1: float, key2:float): bool
            Determines whether key1 and key2 are equal.
        insert_list(elements: list): None
            Inserts all key-value-pairs in elements into the tree.
        insert(element:list): None
            Inserts the key-value-pair in element into the tree.
        check_balance(): int
            Returns the current height difference between subtrees of the tree.
            Trees with height differences -1, 0 or 1 are considered balanced.
        check_height(): int
            Returns the current height of the tree.
        remove(key): None
            Removes the object with key as key from the tree.
        remove_pair(key, value): None
            Removes object with key and value from the trees. Useful when equal keys between objects are allowed.
        delete_root(): None
            Deletes the reference to the current root and therefore access to the tree.
        find_highest(): U
            Finds and returns the object with the key considered greatest with respect to assigned comparator.
        pop_highest(): U
            Finds, removes and returns the object with the key considered greatest with respect to assigned comparator.
        find_lowest(): U
            Finds and returns the object with the key considered lowest with respect to assigned comparator.
        pop_lowest(): U
            Finds, removes and returns the object with the key considered lowest with respect to assigned comparator.
        pop_all(): list
            Removes all objects from the tree, and returns them in a list.
        find_neighbors(key): U
            Returns the left and right Child of the object with the Key.
        find_left_neighbor_by_pair(key, value):
            Returns the next smaller object to the object with the key-value-pair.
        find_right_neighbor_by_pair(): U
            Returns the next larger object to the object with the key-value-pair.
        is_in(key): bool
            Checks whether the object with the key is in the tree.
        print_tree(): None
            Prints the tree structure to the console.
    """
    root = None
    T = TypeVar('T')
    U = TypeVar('U')

    def __init__(self, elements: [(T, U)], comparator=None, equals=None):
        """

        :param elements: [(T,U)]
            list of key-value pairs to be added into the tree.
        :param comparator: @staticmethod
            static method that allows to establish an ordinal relationship between keys
        :param equals: @staticmethod
            static method which checks two keys for equality
        """
        if comparator is None:
            self.comparator = self.default_comparator
        else:
            self.comparator = comparator
        if equals is None:
            self.equals = self.default_equals
        else:
            self.equals = equals
        if len(elements) > 0:

            self.root = TreeObject(key=elements[0][0], value=elements[0][1], tree=self, comparator=comparator,
                                   equals=equals)
            elements.pop(0)
            if len(elements) > 0:
                self.insert_list(elements)

    @staticmethod
    def default_comparator(key1: float, key2: float) -> bool:
        """
        Determines whether key1 is smaller than key2. This default method is used as comparator if none is provided
        on initialization.
        :param key1: float
            Key to be compared.
        :param key2: float
            Key to be compared.
        :return: float
            True if key1 is smaller than key2, else False.
        """
        return key1 < key2

    @staticmethod
    def default_equals(key1: float, key2: float) -> bool:
        """
        Determines whether key1 is equal to key2. This default method is used as equals if none is provided
        on initialization.
        :param key1: float
            Key to be checked for equality.
        :param key2: float
            Key to be checked for equality.
        :return: bool
            True if both keys are equal, else False
        """
        return key1 == key2

    def insert_list(self, elements: [(T, U)]) -> None:
        """
        Inserts a list of key-value pairs into the tree.
        :param elements: [(T, U)]
            List of key-value pairs to be inserted into the tree.
        :return: Nothing
        """
        if not elements:
            return
        if self.root is None:
            self.root = TreeObject(key=elements[0][0], value=elements[0][1], tree=self, comparator=self.comparator,
                                   equals=self.equals)
            elements.pop(0)
            if len(elements) != 0:
                self.insert_list(elements=elements)
        else:
            for element in elements:
                self.insert(element=element)

    def insert(self, element: (T, U)) -> None:
        """
        Inserts a key-value Pair into the tree.
        :param element: (T, U)
            key-value pair to be added into the tree
        :return: Nothing
        """
        if self.root is None:
            self.root = TreeObject(key=element[0], value=element[1], tree=self, comparator=self.comparator,
                                   equals=self.equals)
        else:
            self.root.insert(obj=TreeObject(key=element[0], value=element[1], tree=self, comparator=self.comparator,
                             equals=self.equals))
            self.check_balance()

    def check_balance(self) -> int:
        """
        Checks the current balance of the binary tree. The tree is considered balanced for values -1,0,1.
        :return: int
            The balance value of the tree.
        """
        return self.root.check_balance()

    def check_height(self) -> int:
        """
        Checks the current height of the binary tree.
        :return: int
            The height value of the tree.
        """
        return self.root.check_height()

    def remove(self, key: T) -> None:
        """
        Removes the tree node with the provided key from the tree
        :param key: T
            the key of the node to be removed
        :return: Nothing
        """
        self.root.remove(key=key)

    def remove_pair(self, key: T, value: U) -> None:
        """
        Removes a key-value pir from the tree. This function was added for the line intersection algorithm, since keys
        can be non-unique in the status structure.
        :param key: T
            key of the tree node to be removed.
        :param value: U
            value of the tree node to be removed.
        :return: Nothing
        """
        if self.root is not None:
            self.root.remove_pair(key=key, value=value)

    def delete_root(self) -> None:
        """
        Deletes the root of the tree and therefore the complete tree.
        :return: Nothing
        """
        self.root = None

    def find_highest(self) -> U:
        """
        finds the node with the largest key
        :return: U
            value of the tree node with the highest key.
        """
        return self.root.find_highest()

    def pop_highest(self) -> U:
        """
        finds and removes the node with the largest key
        :return: U
            value of the tree node with the highest key.
        """
        if self.root is None:
            return None
        else:
            return self.root.pop_highest().value

    def find_lowest(self) -> U:
        """
        finds the node with the smallest key
        :return: U
            value of the tree node with the smallest key.
        """
        return self.root.find_lowest()

    def pop_lowest(self) -> U:
        """
        finds and removes the node with the smallest key
        :return: U
            value of the tree node with the smallest key.
        """
        if self.root is None:
            return None
        else:
            return self.root.pop_lowest()

    def pop_all(self) -> [U]:
        """
        retrieves and removes all nodes from the tree in ascending order of keys
        :return: [U]
            list of values of all tree nodes ordered by the size of their keys
        """
        ordered_tree = []
        while self.root is not None:
            ordered_tree.append(self.pop_lowest())
        return ordered_tree

    def find_neighbors(self, key: T) -> (U, U):
        """
        Finds the value of the tree nodes with the next greater and next smaller keys for a given key.
        :param key: T
            the key, for which the neighbors are wanted.
        :return: (U, U)
            neighbors of the tree node with the provided key
        """
        if self.root is None:
            return None, None
        return self.root.find_neighbors(key=key)

    def find_left_neighbor_by_pair(self, key: T, value: U) -> U:
        """
        finds the tree node with the next smaller key for a provided key-value pair. This function was added for
        the line intersection algorithm, since keys can be non-unique in the status structure.
        :param key: T
            The key of the tree node.
        :param value: U
            The value of the tree node.
        :return: U
            the value of the left neighbor of the key-value pair
        """
        if self.root is not None:
            try:
                return self.root.find_left_neighbor_by_pair(key=key, value=value).value
            except AttributeError:
                pass
        return None

    def find_right_neighbor_by_pair(self, key: T, value: U) -> U:
        """
        finds the tree node with the next greater key for a provided key-value pair. This function was added for
        the line intersection algorithm, since keys can be non-unique in the status structure.
        :param key: T
            The key of the tree node.
        :param value: U
            The value of the tree node.
        :return: U
            the value of the right neighbor of the key-value pair
        """
        if self.root is not None:
            try:
                return self.root.find_right_neighbor_by_pair(key=key, value=value).value
            except AttributeError:
                pass
        return None

    def is_in(self, key: T) -> bool:
        """
        checks whether a tree node with the given tree is in the tree.
        :param key: T
            the key to look for in the tree
        :return: bool
            True if the tree node exists in the tree, False if not.
        """
        if self.root is not None:
            return self.root.is_in(key=key)
        return False

    def print_tree(self) -> None:
        """
        prints the whole binary tree to the console.
        :return: Nothing
        """
        if self.root is not None:
            print("root:")
            self.root.print_tree()
        else:
            print("empty tree")
