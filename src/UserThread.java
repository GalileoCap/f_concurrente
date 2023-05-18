import java.util.concurrent.Semaphore;

public class UserThread extends Thread {
  Semaphore startSem;
  String mode;

  public UserThread(String mode, Semaphore startSem) {
    this.mode = mode;
    this.startSem = startSem;
    this.start();
  }

  public void run() {
    startSem.acquireUninterruptibly();

    System.out.println("Ahoy!" + mode);
  }
}
