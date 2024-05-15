class ListNode:
    def __init__(self, value):
        self.value = value
        self.next = self.prev = None

class DoublyLinkedList:
    def __init__(self, *values):
        self.head = self.tail = None
        self.size = 0
        self.extend(values)

    def __len__(self):
        return self.size

    def __str__(self):
        return "None <= " + " <=> ".join(map(str, self)) + " => None"

    def __repr__(self):
        return self.__str__()

    def __contains__(self, item):
        node = self.head
        while node:
            if node.value == item:
                return True
            node = node.next
        return False

    def __eq__(self, other):
        if type(other) is not type(self) or len(self) != len(other):
            return False
        node_self = self.head
        node_other = other.head
        while node_self and node_other:
            if node_self.value != node_other.value:
                return False
            node_self = node_self.next
            node_other = node_other.next
        return True

    def __validate_and_repair_index(self, index):
        if not isinstance(index, int):
            raise TypeError("List index must be an integer")
        index = self.size + index if index < 0 else index
        return index

    def __getitem__(self, index):
        index = self.__validate_and_repair_index(index)
        if 0 <= index < self.size:
            i = 0
            node = self.head
            while node:
                if i == index:
                    return node.value
                node = node.next
                i += 1
        raise IndexError("List index out of range")

    def __setitem__(self, index, item):
        index = self.__validate_and_repair_index(index)
        if 0 <= index < self.size:
            i = 0
            node = self.head
            while node:
                if i == index:
                    node.value = item
                    return
                node = node.next
                i += 1
        raise IndexError("List assignment index out of range")

    def __delitem__(self, index):
        index = self.__validate_and_repair_index(index)
        if 0 < index < self.size - 1:
            i = 0
            node = self.head
            while node:
                if i == index:
                    node.prev.next = node.next
                    node.next.prev = node.prev
                    self.size -= 1
                    return
                node = node.next
                i += 1
        elif index == 0 and self.head is not None:
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            self.size -= 1
        elif index == self.size - 1 and self.head is not None:
            self.tail = self.tail.prev
            if self.tail:
                self.tail.next = None
            self.size -= 1
        else:
            raise IndexError("List index out of range")

    def insertStart(self, item):
        new_node = ListNode(item)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def insertEnd(self, item):
        new_node = ListNode(item)
        if not self.tail:
            self.tail = new_node
            self.head = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def insert(self, index, item):
        index = self.__validate_and_repair_index(index)
        if index > self.size - 1:
            self.insertEnd(item)
        elif index <= 0:
            self.insertStart(item)
        else:
            i = 0
            node = self.head
            while node:
                if i == index - 1:
                    new_node = ListNode(item)
                    new_node.next = node.next
                    new_node.prev = node
                    node.next = new_node
                    if new_node.next:
                        new_node.next.prev = new_node
                    self.size += 1
                    return
                node = node.next
                i += 1

    def extend(self, seq=()):
        for i in seq:
            self.insertEnd(i)

    def remove(self, item):
        if not self.head:
            raise IndexError("List is empty")
        else:
            if self.head.value == item:
                self.head = self.head.next
                if self.head:
                    self.head.prev = None
            elif self.tail.value == item:
                self.tail = self.tail.prev
                if self.tail:
                    self.tail.next = None
            else:
                node = self.head
                try:
                    while node:
                        if node.value == item:
                            node.prev.next = node.next
                            if node.next:
                                node.next.prev = node.prev
                            self.size -= 1
                            return
                        node = node.next
                except AttributeError:
                    raise ValueError("Value not present in list") from None
            self.size -= 1

    def pop(self, index=-1):
        if self.size == 0:
            raise IndexError("List is empty")
        t = type(index)
        if t is not int:
            raise TypeError("{} can't be interpreted as an integer".format(t))
        index = self.__validate_and_repair_index(index)
        if index == self.size - 1:
            item = self.tail.value
            del self[self.size - 1]
            return item
        if index == 0:
            item = self.head.value
            del self[0]
            return item
        i = 0
        node = self.head
        while node:
            if i == index:
                item = node.value
                del self[index]
                return item
            node = node.next
            i += 1

    def index(self, item):
        for index, el in enumerate(self):
            if el == item:
                return index
        return -1

    def count(self, item):
        count = 0
        node = self.head
        while node:
            if node.value == item:
                count += 1
            node = node.next
        return count
