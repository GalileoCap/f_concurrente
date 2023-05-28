import Utils.*;
import java.util.ArrayList;

class UserThread extends Thread {
  String mode;
  int actions;
  ThreadPool pool;
  ArrayList<Long> times;

  public UserThread(String mode, int actions, ThreadPool pool) {
    this.mode = mode;
    this.actions = actions;
    this.pool = pool;
    this.times = new ArrayList<>();
    this.start();
  }

  public void run() {
    pool.startSem.acquireUninterruptibly();

    for (int i = 0; i < actions; i++) {
      performAction();
    }
  }

  void performAction() {
    switch (mode) {
      case "add": add(); break;
      case "remove": remove(); break;
      case "find": find(); break;
    }
  }

  void add() {
    Integer elem = (int)Math.floor(Math.random() * Integer.MAX_VALUE);

    long start = System.nanoTime();
    boolean success = pool.set.add(elem);
    long delta = System.nanoTime() - start;
    times.add(delta); // TODO: Also report whether it was a success

    if (success) {
      pool.addElement(elem);
    }
  }

  void remove() {
    Integer elem = pool.getRandomElement();

    long start = System.nanoTime();
    boolean success = pool.set.remove(elem);
    long delta = System.nanoTime() - start;
    times.add(delta); // TODO: Also report whether it was a success

    if (success) {
      pool.removeElement(elem);
    }
  }

  void find() {
    Integer elem = pool.getRandomElement();

    long start = System.nanoTime();
    Integer success = pool.set.find(elem); // TODO: Change to boolean
    long delta = System.nanoTime() - start;
    times.add(delta); // TODO: Also report whether it was a success
  }
}
