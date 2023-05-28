package Map;

import java.util.concurrent.locks.ReentrantLock;

public class MapFG<T> implements Map<T> {
  class Node<T> {
    public int key;
    public T value;
    public volatile Node<T> next;
    private ReentrantLock lock;

    public Node(int _key, T _value) {
      key = _key;
      value = _value;
      lock = new ReentrantLock();
    }

    public void lock() {
      lock.lock();
    }

    public void unlock() {
      lock.unlock();
    }
  }

  private Node<T> head;

  public MapFG() {
    head = new Node<T>(Integer.MIN_VALUE, null);
    head.next = new Node<T>(Integer.MAX_VALUE, null);
  }

  public Boolean add(T newItem) {
    int key = newItem.hashCode();
    Node<T> prev, curr;
    prev = head; prev.lock();
    curr = prev.next; curr.lock();
    try {
      while (curr.key < key) {
        prev.unlock();
        prev = curr;
        curr = curr.next;
        curr.lock();
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
      curr.unlock();
      prev.unlock();
    }
  }

  public Boolean remove(int key) {
    Node<T> prev, curr;
    prev = head; prev.lock();
    curr = prev.next; curr.lock();
    try {
      while (curr.key < key) {
        prev.unlock();
        prev = curr;
        curr = curr.next;
        curr.lock();
      }

      if (key != curr.key)
        return false; 
      else {
        prev.next = curr.next;
        return true;
      }
    } finally {
      curr.unlock();
      prev.unlock();
    }
  }

  public T find(int key) {
    Node<T> prev, curr;
    prev = head; prev.lock();
    curr = prev.next; curr.lock();
    try {
      while (curr.key < key) {
        prev.unlock();
        prev = curr;
        curr = curr.next;
        curr.lock();
      }

      if (key == curr.key) return curr.value;
      else return null;
    } finally {
      curr.unlock();
      prev.unlock();
    }
  }
}
