import Twiner.Twiner;
import Map.Map;

class Main {
  public static void main(String args[]) {
    Twiner t = new Twiner();

    int s0 = t.logIn(0);
    int s1 = t.logIn(1);

    t.newPost(0, s0);
    t.newPost(0, s0);
    t.newPost(1, s1);
  
    System.out.println(t.nextPost(0, s0));
    System.out.println(t.nextPost(1, s1));
    System.out.println(t.nextPost(0, s0));
    t.logOut(0, s0);
    s0 = t.logIn(0);
    System.out.println(t.nextPost(0, s0));
    System.out.println(t.nextPost(1, s1));
    //System.out.println(sessionId);
  }
}

