"""Contact storage using a fixed array and separate chaining, without dict."""


class Contact:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return f"{self.name}: {self.number}"


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, size):
        if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
            raise ValueError("Table size must be a positive integer")
        self.size = size
        self.data = [None] * size

    def hash_function(self, key):
        # Character sums make the Amy/May collision easy to demonstrate.
        return sum(ord(character) for character in key) % self.size

    def insert(self, key, value):
        """Insert a name and phone number; update an existing name in place."""
        index = self.hash_function(key)
        current = self.data[index]
        if current is None:
            self.data[index] = Node(key, Contact(key, value))
            return
        while True:
            if current.key == key:
                current.value.number = value
                return
            if current.next is None:
                current.next = Node(key, Contact(key, value))
                return
            current = current.next

    def search(self, key):
        current = self.data[self.hash_function(key)]
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def print_table(self):
        for index, head in enumerate(self.data):
            contacts = []
            current = head
            while current is not None:
                contacts.append(str(current.value))
                current = current.next
            print(f"Index {index}: " + (" - " + " - ".join(contacts) if contacts else "Empty"))


if __name__ == "__main__":
    table = HashTable(10)
    table.print_table()
    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")
    print("\nSearch result:", table.search("John"))
    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")
    table.insert("Rebecca", "999-444-9999")
    print("\nAfter collisions and duplicate update:")
    table.print_table()
    print("\nMissing contact:", table.search("Chris"))


# Contact Management System Design Memo
# 
# A hash table is a good choice for this contact manager because the main task is finding a contact by an exact name. Instead of checking every contact, the hash function turns the name into an index in a fixed array. My function adds the Unicode values returned by ord() and takes the remainder after division by the table size. The same name always produces the same index. Hashing a name takes time proportional to its length. With short names and well-distributed entries, inserting and searching are approximately constant time on average.
# 
# I handled collisions with separate chaining. Every array position starts as None. When a contact is added, that position points to a Node containing the name, a Contact object, and a next pointer. If another name has the same index, I walk through the linked list and add the new node at the end. Amy and May intentionally collide because they contain the same letters. Both contacts remain available. Before adding a node, I check for an existing name. A duplicate name updates its phone number rather than creating another entry. A missing search returns None.
# 
# An engineer might choose a hash table over a list when exact lookups happen often and sorted order is unnecessary. A balanced tree is better when sorted traversal or range searches matter. This simple character-sum hash can produce many collisions, especially for anagrams. Also, the table does not resize, so long chains can make operations take linear time. The array and linked nodes use O(m + n) space for m buckets and n contacts.
# 
