package Test;

import Test.Test;
import Twiner.Twiner;

class TwinerTest extends Test {
  private static String mapType = "monitor";

  public static void run() {
    testLogIn();
    testLogOut();
    testLogOutWrongSID();
    testNewPost();
    testNewPostWrongSID();
    testNextPostNull();
    testNextPost();
    testNextPostWrongSID();
    testRemovePost();
    testRemovePostWrongSID();
  }

  static void testLogIn() {
    printCase("Twiner", "logIn");

    Twiner t = new Twiner(mapType);

    int uid = 0;
    int sid = t.logIn(uid);

    Assert(t.logIn(uid) == -1, "Logged in twice");

    Success();
  }

  static void testLogOut() {
    printCase("Twiner", "logOut");

    Twiner t = new Twiner(mapType);

    int uid = 0;
    int sid = t.logIn(uid);

    Assert(t.logOut(uid, sid), "Coulnd't log out");
    Assert(t.logIn(uid) != -1, "Couldn't log back in");

    Success();
  }

  static void testLogOutWrongSID() {
    printCase("Twiner", "logOutWrongSID");

    Twiner t = new Twiner(mapType);

    int uid = 0;
    int sid = t.logIn(uid);

    Assert(!t.logOut(uid, sid+1), "Was able to log out");

    Success();
  }

  static void testNewPost() {
    printCase("Twiner", "newPost");

    Twiner t = new Twiner(mapType);
    int uid = 0;
    int sid = t.logIn(uid);

    Assert(t.newPost(uid, sid) != -1, "Couldn't post");

    Success();
  }

  static void testNewPostWrongSID() {
    printCase("Twiner", "newPostWrongSID");

    Twiner t = new Twiner(mapType);
    int uid = 0;
    int sid = t.logIn(uid);

    Assert(t.newPost(uid, sid+1) == -1, "Was able to post");

    Success();
  }

  static void testNextPostNull() {
    printCase("Twiner", "nextPostNull");

    Twiner t = new Twiner(mapType);
    int uid = 0;
    int sid = t.logIn(uid);

    Assert(t.nextPost(uid, sid) == -1, "Found a post");

    Success();
  }

  static void testNextPost() {
    printCase("Twiner", "nextPost");

    Twiner t = new Twiner(mapType);
    int uid = 0;
    int sid = t.logIn(uid);

    int date = t.newPost(uid, sid);
    Assert(t.nextPost(uid, sid) == date, "Couldn't find post");
    Assert(t.nextPost(uid, sid) == -1, "Found another post");

    Success();
  }

  static void testNextPostWrongSID() {
    printCase("Twiner", "nextPostWrongSID");

    Twiner t = new Twiner(mapType);
    int uid = 0;
    int sid = t.logIn(uid);

    int date = t.newPost(uid, sid);
    Assert(t.nextPost(uid, sid+1) == -1, "Was able to move");

    Success();
  }

  static void testRemovePost() {
    printCase("Twiner", "removePost");

    Twiner t = new Twiner(mapType);
    int uid = 0;
    int sid = t.logIn(uid);

    int date = t.newPost(uid, sid);
    Assert(t.removePost(date, uid, sid), "Couldn't remove post");
    Assert(t.nextPost(uid, sid) == -1, "Found another post");

    Success();
  }

  static void testRemovePostWrongSID() {
    printCase("Twiner", "removePostWrongSID");

    Twiner t = new Twiner(mapType);
    int uid = 0;
    int sid = t.logIn(uid);

    int date = t.newPost(uid, sid);
    Assert(!t.removePost(date, uid, sid+1), "Was able to remove post");
    Assert(t.nextPost(uid, sid) == date, "Couldn't find post");

    Success();
  }
}
