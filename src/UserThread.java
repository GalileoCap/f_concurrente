import Twiner.User;
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
    int sid = pool.twiner.logIn(uid);
    long delta = System.nanoTime() - start;
    times.add(delta); // TODO: Also report whether it was a success (sid != -1)

    if (sid != -1) {
      pool.addUser(new User(uid, sid));
    }
  }

  void logOut() {
    User user = pool.getRandomUser();

    long start = System.nanoTime();
    boolean success = pool.twiner.logOut(user.userId, user.sessionId);
    long delta = System.nanoTime() - start;
    times.add(delta); // TODO: Also report whether it was a success

    if (success) {
      pool.removeUser(user);
    }
  }

  void apiRequest() {
    User user = pool.getRandomUser();

    long start = System.nanoTime();
    Boolean success = pool.twiner.apiRequest(user.userId, user.sessionId);
    long delta = System.nanoTime() - start;
    times.add(delta); // TODO: Also report whether it was a success
  }
}
