package Map;

class Node<T> {
  public int key;
  public T value;
  public Node<T> next;

  public Node(int _key, T _value) {
    key = _key;
    value = _value;
  }
}

public class Map<T> {
  private Node<T> head;

  public Map() {
    head = new Node<T>(Integer.MIN_VALUE, null);
    head.next = new Node<T>(Integer.MAX_VALUE, null);
  }

  public Boolean add(T newItem) {
    int key = newItem.hashCode();
    Node<T> prev = head,
            curr = prev.next;
    while (curr.key < key) {
      prev = curr;
      curr = curr.next;
    }

    if (key == curr.key)
      return false;
    else {
      Node<T> newNode = new Node<T>(key, newItem);
      newNode.next = curr;
      prev.next = newNode;
      return true;
    }
  }

  public Boolean remove(int key) {
    Node<T> prev = head,
            curr = prev.next;
    while (curr.key < key) {
      prev = curr;
      curr = curr.next;
    }

    if (key != curr.key)
      return false; 
    else {
      prev.next = curr.next;
      return true;
    }
  }

  public T find(int key) {
    Node<T> prev = head,
            curr = prev.next;
    while (curr.key < key) {
      prev = curr;
      curr = curr.next;
    }

    if (key == curr.key) return curr.value;
    else return null;
  }
}
