import Twiner.Twiner;

class Main {
  public static void main(String args[]) {
    Twiner t = new Twiner();

    int s0 = t.logIn(0);
    int s1 = t.logIn(1);

    int post = t.newPost(0, s0);
    t.removePost(post, 2, 0);
    t.removePost(post, 1, s0);
  
    t.logOut(0, s0);
    s0 = t.logIn(0);

    System.out.println(t.removePost(post, 0, s0));
    //System.out.println(sessionId);
  }
}

