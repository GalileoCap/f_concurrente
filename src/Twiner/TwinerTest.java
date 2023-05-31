package Test;

import Test.Test;
import Twiner.Twiner;

class TwinerTest extends Test {
  private static String mapType = "fine-grained";

  public static void run() {
    testLogIn();
    testLogOut();
    testLogOutWrongSID();
    testApiRequest();
    testApiRequestWrongUser();
    testApiRequestWrongSID();
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

  static void testApiRequest() {
    printCase("Twiner", "apiRequest");

    Twiner t = new Twiner(mapType);
    int uid = 0;
    int sid = t.logIn(uid);

    Assert(t.apiRequest(uid, sid), "Couldn't send api request");

    Success();
  }

  static void testApiRequestWrongUser() {
    printCase("Twiner", "apiRequestWrongUser");

    Twiner t = new Twiner(mapType);

    Assert(!t.apiRequest(0, 0), "Was able to send api request");

    Success();
  }

  static void testApiRequestWrongSID() {
    printCase("Twiner", "apiRequestWrongSID");

    Twiner t = new Twiner(mapType);
    int uid = 0;
    int sid = t.logIn(uid);

    Assert(!t.apiRequest(uid, sid+1), "Was able to send api request");

    Success();
  }
}
