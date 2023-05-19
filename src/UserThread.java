import Twiner.User;
import Utils.*;

class UserThread extends Thread {
  String mode;
  int actions;
  ThreadPool pool;

  public UserThread(String mode, int actions, ThreadPool pool) {
    this.mode = mode;
    this.actions = actions;
    this.pool = pool;
    this.start();
  }

  public void run() {
    pool.startSem.acquireUninterruptibly();

    for (int i = 0; i < actions; i++) {
      performAction();
    }

    // TODO: Report results
  }

  void performAction() {
    switch (mode) {
      case "logIn": logIn(); break;
      case "logOut": logOut(); break;
      case "newPost": newPost(); break;
      case "nextPost": nextPost(); break;
      //case "removePost": removePost(); break;
    }
  }

  void logIn() {
    int uid = (int)Math.floor(Math.random() * 10000);
    int sid = pool.twiner.logIn(uid);
    pool.addUser(new User(uid, sid));
  }

  void logOut() {
    User user = pool.getRandomUser();
    if (pool.twiner.logOut(user.userId, user.sessionId)) {
      pool.removeUser(user);
    }
  }

  void newPost() {
    User user = pool.getRandomUser();
    pool.twiner.newPost(user.userId, user.sessionId); // TODO: Save posts
  }

  void nextPost() {
    User user = pool.getRandomUser();
    pool.twiner.nextPost(user.userId, user.sessionId);
  }
}
