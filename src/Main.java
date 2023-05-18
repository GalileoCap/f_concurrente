import Twiner.Twiner;
import Utils.*;
import java.util.Vector;
import java.util.concurrent.Semaphore;

class Main {
  static Vector<UserThread> threads = new Vector<UserThread>();
  static Semaphore startSem;

  public static void main(String args[]) {
    Twiner t = new Twiner("monitor");

    int logIn = Utils.atoi(args[0]),
        logOut = Utils.atoi(args[1]),
        newPost = Utils.atoi(args[2]),
        readPost = Utils.atoi(args[3]),
        deletePost = Utils.atoi(args[4]);

    int total = logIn + logOut + newPost + readPost + deletePost;

    startSem = new Semaphore(total);
    startSem.acquireUninterruptibly(total);

    spawnThreads(logIn, "logIn");
    spawnThreads(logOut, "logOut");
    spawnThreads(newPost, "newPost");
    spawnThreads(readPost, "readPost");
    spawnThreads(deletePost, "deletePost");

    startSem.release(total);
  }

  static void spawnThreads(int n, String mode) {
    for (int i = 0; i < n; i++) {
      threads.add(new UserThread(mode, startSem));
    }
  }
}

