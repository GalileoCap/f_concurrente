import Set.*;
import Utils.Utils;
import java.util.ArrayList;
import java.util.concurrent.Semaphore;

public class ThreadPool {
  public Set<Integer> set; // U: Set that all threads share
  public Semaphore startSem; // U: Semaphore to control that threads all start at the same time
  ArrayList<Integer> elems; // U: Elements currently in the set
  ArrayList<UserThread> threads;

  public static void main(String[] args) {
    String mode = args[0]; // U: Mode for the set, one of:
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

    SetBuilder setBuilder = new SetBuilder(mode);
    set = setBuilder.newSet();

    startSem = new Semaphore(total);
    elems = new ArrayList<Integer>();
    threads = new ArrayList<UserThread>();

    startSem.acquireUninterruptibly(total);

    // Initialize the set with some elements
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
      set.add(i);
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
