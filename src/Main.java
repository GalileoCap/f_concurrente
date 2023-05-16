import Twiner.Twiner;

class Main {
  public static void main(String args[]) {
    Twiner t = new Twiner();

    int sessionId = t.logIn(0);
    System.out.println(sessionId);
    System.out.println(t.logOut(1, sessionId));
    System.out.println(t.logOut(0, 99));
    System.out.println(t.logOut(0, sessionId));
    System.out.println(t.logOut(0, sessionId));
  }
}

