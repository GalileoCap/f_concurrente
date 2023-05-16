package Map;

import java.util.concurrent.atomic.AtomicMarkableReference;

public class MapFree<T> implements Map<T> {
  class Node<T> {
    public int key;
    public T value;
    public AtomicMarkableReference<Node<T>> next;

    public Node(int _key, T _value) {
      key = _key;
      value = _value;
    }
  }

  class NPair<T> {
    public final Node<T> prev, curr;
    public NPair(Node<T> _prev, Node<T> _curr) {
      prev = _prev; curr = _curr;
    }
  }

  private Node<T> head;

  public MapFree() {
    head = new Node<T>(Integer.MIN_VALUE, null);

    Node<T> tail = new Node<T>(Integer.MAX_VALUE, null);

    head.next = new AtomicMarkableReference<>(tail, false);
    tail.next = new AtomicMarkableReference<>(null, false);
  }

  private NPair<T> findInternal(int key) { //TODO: Rename
    Node<T> prev, curr, next;
    boolean[] marked = { false };
    retry: while (true) {
      prev = head; curr = prev.next.getReference();
      while (true) {
        next = curr.next.get(marked);
        while (marked[0]) {
          if (!prev.next.compareAndSet(curr, next, false, false))
            continue retry;

          curr = next;
          next = curr.next.get(marked);
        }

        if (key <= curr.key)
          return new NPair<T>(prev, curr);
        prev = curr;
        curr = next;
      }
    }
  }

  public Boolean add(T newItem) {
    int key = newItem.hashCode();
    Node<T> prev, curr,
            newNode = new Node<T>(key, newItem);

    while (true) {
      NPair<T> pair = findInternal(key);
      prev = pair.prev; curr = pair.curr; // Rename

      if (curr.key == key)
        return false;

      newNode.next = new AtomicMarkableReference<>(curr, false);
      if (prev.next.compareAndSet(curr, newNode, false, false))
        return true;
    }
  }

  public synchronized Boolean remove(int key) {
    Node<T> prev, curr, next;
    boolean snip;

    while (true) {
      NPair pair = findInternal(key);
      prev = pair.prev; curr = pair.curr; // Rename

      if (curr.key != key)
        return false;

      next = curr.next.getReference();
      snip = curr.next.attemptMark(next, true);
      if (!snip)
        continue;

      prev.next.compareAndSet(curr, next, false, false);
      return true;
    }
  }

  public synchronized T findAfter(int key) {
    return find(key+1);
  }

  public synchronized T find(int key) {
    Node<T> prev, curr;

    NPair pair = findInternal(key);
    prev = pair.prev; curr = pair.curr; // Rename

    if (curr.key != key)
      return null;
    return curr.value;
  }
}
