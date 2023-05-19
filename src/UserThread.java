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
      case "removePost": removePost(); break;
      case "nextPost": nextPost(); break;
    }
  }

  void logIn() {
    int uid = (int)Math.floor(Math.random() * 1000000); // TODO: Max users param
    int sid = pool.twiner.logIn(uid);
    if (sid != -1) {
      pool.addUser(new User(uid, sid));
    }
  }

  void logOut() {
    User user = pool.getRandomUser();
    if (pool.twiner.logOut(user.userId, user.sessionId)) {
      pool.removeUser(user);
    }
  }

  void newPost() {
    User user = pool.getRandomUser();
    int date = pool.twiner.newPost(user.userId, user.sessionId);
    if (date != -1) {
      pool.setLastPost(date); // TODO: Save posts per-user
    }
  }

  void removePost() {
    User user = pool.getRandomUser(); // TODO: Get random user/owned post pair
    int date = (int)Math.floor(Math.random() * pool.lastPost);

    pool.twiner.removePost(date, user.userId, user.sessionId);
  }

  void nextPost() {
    User user = pool.getRandomUser();
    pool.twiner.nextPost(user.userId, user.sessionId);
  }
}
