import Map.*;
import Utils.Utils;
import java.util.ArrayList;
import java.util.concurrent.Semaphore;

public class ThreadPool {
  public Map<Integer> map; // U: Map that all threads share
  public Semaphore startSem; // U: Semaphore to control that threads all start at the same time
  ArrayList<Integer> elems; // U: Elements currently in the map
  ArrayList<UserThread> threads;

  public static void main(String[] args) {
    String mode = args[0]; // U: Mode for the map, one of:
                           // String[] types = {"free", "lazy", "optimistic", "fine-grained", "monitor"};

    int actions = Utils.atoi(args[1]); // U: Number of actions per thread

    // U: Number of threads doing each action
    int add = Utils.atoi(args[2]); 
    int remove = Utils.atoi(args[3]);
    int find = Utils.atoi(args[4]);

    new ThreadPool(mode, actions, add, remove, find);
  }

  public ThreadPool(String mode, int actions, int add, int remove, int find) {
    int total = add + remove + find;

    MapBuilder mapBuilder = new MapBuilder(mode);
    map = mapBuilder.newMap();

    startSem = new Semaphore(total);
    elems = new ArrayList();
    threads = new ArrayList();

    startSem.acquireUninterruptibly(total);

    // Initialize the map with some elements
    addElements(total);

    spawnThreads(add, "add", actions);
    spawnThreads(remove, "remove", actions);
    spawnThreads(find, "find", actions);

    startSem.release(total);

    // Wait until each thread is done and report its results
    for (UserThread thread : threads) {
      while(thread.isAlive());
      System.out.print(thread.mode + ", ");
      System.out.println(thread.times.toString().replace("[", "").replace("]", "")); 
    }
  }

  void addElements(int n) {
    for (int i = 0; i < n; ++i) {
      map.add(i);
      addElement(i);
    }
  }

  void spawnThreads(int n, String mode, int actions) {
    for (int i = 0; i < n; ++i) {
      threads.add(new UserThread(mode, actions, this));
    }
  }

  public synchronized Integer getRandomElement() {
    if (elems.size() == 0) {
      return 123; // Random element
    }
    int idx = (int)Math.floor(Math.random() * elems.size());
    return elems.get(idx);
  }

  public synchronized void addElement(Integer elem) {
    elems.add(elem);
  }

  public synchronized void removeElement(Integer elem) {
    elems.remove(elem);
  }
}
