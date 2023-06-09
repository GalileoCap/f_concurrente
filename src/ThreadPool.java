import Twiner.Twiner;
import Twiner.User;
import Utils.Utils;
import java.util.ArrayList;
import java.util.concurrent.Semaphore;

public class ThreadPool {
  public Twiner twiner; // U: Twiner that all threads share
  public Semaphore startSem; // U: Semaphore to control that threads all start at the same time
  ArrayList<User> users; // U: Created users by logIn threads
  ArrayList<UserThread> threads;

  public static void main(String[] args) {
    String mode = args[0]; // U: Mode for the maps Twiner uses, one of:
                           // String[] types = {"free", "optimistic", "fine-grained"};

    int actions = Utils.atoi(args[1]); // U: Number of actions per thread

    // U: Number of threads doing each action
    int logIn = Utils.atoi(args[2]); 
    int logOut = Utils.atoi(args[3]);
    int apiRequest = Utils.atoi(args[4]);

    new ThreadPool(mode, actions, logIn, logOut, apiRequest);
  }

  public ThreadPool(String mode, int actions, int logIn, int logOut, int apiRequest) {
    int total = logIn + logOut + apiRequest;

    twiner = new Twiner(mode);
    startSem = new Semaphore(total);
    users = new ArrayList();
    threads = new ArrayList();

    startSem.acquireUninterruptibly(total);

    // Make sure there's an user for each thread
    createUsers(total);

    spawnThreads(logIn, "logIn", actions);
    spawnThreads(logOut, "logOut", actions);
    spawnThreads(apiRequest, "apiRequest", actions);

    startSem.release(total);

    // Wait until each thread is done and report its results
    for (UserThread thread : threads) {
      while(thread.isAlive());
      System.out.print(thread.mode + ", ");
      System.out.println(thread.times.toString().replace("[", "").replace("]", "")); 
    }
  }

  void createUsers(int n) {
    for (int i = 0; i < n; ++i) {
      int sid = twiner.logIn(i);
      addUser(new User(i, sid));
    }
  }

  void spawnThreads(int n, String mode, int actions) {
    for (int i = 0; i < n; ++i) {
      threads.add(new UserThread(mode, actions, this));
    }
  }

  public synchronized User getRandomUser() {
    if (users.size() == 0) {
      return new User(123, 123); // Invalid user
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
