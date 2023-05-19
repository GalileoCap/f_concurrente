import Twiner.Twiner;
import Twiner.User;
import Utils.Utils;
import java.util.ArrayList;
import java.util.concurrent.Semaphore;

public class ThreadPool {
  public Twiner twiner;
  public Semaphore startSem;
  ArrayList<User> users;
  ArrayList<UserThread> threads;

  public static void main(String[] args) {
    String mode = args[0];
    int logIn = Utils.atoi(args[1]);
    int logOut = Utils.atoi(args[2]);
    int newPost = Utils.atoi(args[3]);
    int nextPost = Utils.atoi(args[4]);
    int removePost = Utils.atoi(args[5]);
    int actions = Utils.atoi(args[6]);
    new ThreadPool(mode, logIn, logOut, newPost, nextPost, removePost, actions);
  }

  public ThreadPool(String mode, int logIn, int logOut, int newPost, int nextPost, int removePost, int actions) {
    int total = logIn + logOut + newPost + nextPost + removePost;

    twiner = new Twiner(mode);
    startSem = new Semaphore(total);
    users = new ArrayList();
    threads = new ArrayList();

    startSem.acquireUninterruptibly(total);

    spawnThreads(logIn, "logIn", actions);
    spawnThreads(logOut, "logOut", actions);
    spawnThreads(newPost, "newPost", actions);
    spawnThreads(nextPost, "nextPost", actions);
    spawnThreads(removePost, "removePost", actions);

    startSem.release(total);
  }

  void spawnThreads(int n, String mode, int actions) {
    for (int i = 0; i < n; ++i) {
      threads.add(new UserThread(mode, actions, this));
    }
  }

  public synchronized User getRandomUser() {
    if (users.size() == 0) {
      return new User(123, 123);
    }
    int idx = (int)Math.floor(Math.random() * users.size());
    return users.get(idx);
  }

  public synchronized void addUser(User user) {
    users.add(user);
  }

  public synchronized void removeUser(User user) {
    users.remove(user);
  }
}
