package Map;

public class MapMonitor<T> implements Map<T> {
  class Node<T> {
    public int key;
    public T value;
    public Node<T> next;

    public Node(int _key, T _value) {
      key = _key;
      value = _value;
    }
  }

  private Node<T> head;

  public MapMonitor() {
    head = new Node<T>(Integer.MIN_VALUE, null);
    head.next = new Node<T>(Integer.MAX_VALUE, null);
  }

  public synchronized Boolean add(T newItem) {
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

  public synchronized Boolean remove(int key) {
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

  public synchronized T findAfter(int key) {
    Node<T> prev = head,
            curr = prev.next;
    while (curr.key <= key) {
      prev = curr;
      curr = curr.next;
    }

    if (curr.key == Integer.MAX_VALUE)
      return null;
    return curr.value;
  }

  public synchronized T find(int key) {
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
