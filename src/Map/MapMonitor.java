package Map;

import java.util.concurrent.locks.ReentrantLock;

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
  private ReentrantLock lock;

  public MapMonitor() {
    head = new Node<T>(Integer.MIN_VALUE, null);
    head.next = new Node<T>(Integer.MAX_VALUE, null);
    lock = new ReentrantLock();
  }

  public Boolean add(T newItem) {
    lock.lock();

    try {
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
    } finally {
      lock.unlock();
    }
  }

  public Boolean remove(int key) {
    lock.lock();

    try {
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
    } finally {
      lock.unlock();
    }
  }

  public T findAfter(int key) {
    lock.lock();

    try {
      Node<T> prev = head,
              curr = prev.next;
      while (curr.key <= key) {
        prev = curr;
        curr = curr.next;
      }

      if (curr.key == Integer.MAX_VALUE)
        return null;
      return curr.value;
    } finally {
      lock.unlock();
    }
  }

  public T find(int key) {
    lock.lock();

    try {
      Node<T> prev = head,
              curr = prev.next;
      while (curr.key < key) {
        prev = curr;
        curr = curr.next;
      }

      if (key == curr.key) return curr.value;
      else return null;
    } finally {
      lock.unlock();
    }
  }
}
