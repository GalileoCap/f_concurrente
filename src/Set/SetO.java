package Set;

import java.util.concurrent.locks.ReentrantLock;

public class SetO<T> implements Set<T> {
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

  public SetO() {
    head = new Node<T>(Integer.MIN_VALUE, null);
    head.next = new Node<T>(Integer.MAX_VALUE, null);
  }

  private Boolean validate(Node<T> prev, Node<T> curr) {
    Node<T> node = head;
    while (node.key < prev.key)
      node = node.next;

    return node == prev && prev.next == curr;
  }

  public Boolean add(T newItem) {
    int key = newItem.hashCode();
    while (true) {
      Node<T> prev = head,
              curr = prev.next;
      while (curr.key < key) {
        prev = curr;
        curr = curr.next;
      }

      prev.lock(); curr.lock();
      try {
        if (!validate(prev, curr))
          continue;

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
  }

  public Boolean remove(int key) {
    while (true) {
      Node<T> prev = head,
              curr = prev.next;
      while (curr.key < key) {
        prev = curr;
        curr = curr.next;
      }

      prev.lock(); curr.lock();
      try {
        if (!validate(prev, curr))
          continue;

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
  }

  public T find(int key) {
    while (true) {
      Node<T> prev = head,
              curr = prev.next;
      while (curr.key < key) {
        prev = curr;
        curr = curr.next;
      }

      prev.lock(); curr.lock();
      try {
        if (!validate(prev, curr))
          continue;

        if (curr.key == Integer.MAX_VALUE)
          return null;
        return curr.value;
      } finally {
        curr.unlock();
        prev.unlock();
      }
    }
  }
}
