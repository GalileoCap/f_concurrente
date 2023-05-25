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
      case "logIn": logIn(); break;
      case "logOut": logOut(); break;
      case "apiRequest": apiRequest(); break;
    }
  }

  void logIn() {
    int uid = (int)Math.floor(Math.random() * Integer.MAX_VALUE);

    long start = System.nanoTime();
    Boolean success = pool.twiner.logIn(uid);
    long delta = System.nanoTime() - start;
    times.add(delta); // TODO: Also report whether it was a success

    if (success) {
      pool.addUser(uid);
    }
  }

  void logOut() {
    Integer user = pool.getRandomUser();

    long start = System.nanoTime();
    boolean success = pool.twiner.logOut(user);
    long delta = System.nanoTime() - start;
    times.add(delta); // TODO: Also report whether it was a success

    if (success) {
      pool.removeUser(user);
    }
  }

  void apiRequest() {
    Integer user = pool.getRandomUser();

    long start = System.nanoTime();
    Boolean success = pool.twiner.apiRequest(user);
    long delta = System.nanoTime() - start;
    times.add(delta); // TODO: Also report whether it was a success
  }
}
