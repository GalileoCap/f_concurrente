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
      case "newPost": newPost(); break;
      case "removePost": removePost(); break;
      case "nextPost": nextPost(); break;
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

  void newPost() {
    User user = pool.getRandomUser();

    long start = System.nanoTime();
    int date = pool.twiner.newPost(user.userId, user.sessionId);
    long delta = System.nanoTime() - start;
    times.add(delta); // TODO: Also report whether it was a success (date != -1)

    if (date != -1) {
      pool.setLastPost(date); // TODO: Save posts per-user
    }
  }

  void removePost() {
    User user = pool.getRandomUser(); // TODO: Get random user/owned post pair
    int date = (int)Math.floor(Math.random() * pool.lastPost);

    long start = System.nanoTime();
    boolean success = pool.twiner.removePost(date, user.userId, user.sessionId);
    long delta = System.nanoTime() - start;
    times.add(delta); // TODO: Also report whether it was a success
  }

  void nextPost() {
    User user = pool.getRandomUser();

    long start = System.nanoTime();
    int date = pool.twiner.nextPost(user.userId, user.sessionId);
    long delta = System.nanoTime() - start;
    times.add(delta); // TODO: Also report whether it was a success (date != -1)
  }
}
