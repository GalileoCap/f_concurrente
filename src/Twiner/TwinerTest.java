package Test;

import Test.Test;
import Twiner.Twiner;

class TwinerTest extends Test {
  private static String mapType = "monitor";

  public static void run() {
    testLogIn();
    testLogOut();
    testApiRequest();
    testApiRequestWrongUser();
  }

  static void testLogIn() {
    printCase("Twiner", "logIn");

    Twiner t = new Twiner(mapType);

    int uid = 0;
    Assert(t.logIn(uid), "Couldn't log in");
    Assert(!t.logIn(uid), "Logged in twice");

    Success();
  }

  static void testLogOut() {
    printCase("Twiner", "logOut");

    Twiner t = new Twiner(mapType);

    int uid = 0;
    t.logIn(uid);

    Assert(t.logOut(uid), "Coulnd't log out");
    Assert(t.logIn(uid), "Couldn't log back in");

    Success();
  }

  static void testApiRequest() {
    printCase("Twiner", "apiRequest");

    Twiner t = new Twiner(mapType);
    int uid = 0;
    t.logIn(uid);

    Assert(t.apiRequest(uid), "Couldn't send api request");

    Success();
  }

  static void testApiRequestWrongUser() {
    printCase("Twiner", "apiRequestWrongUser");

    Twiner t = new Twiner(mapType);

    Assert(!t.apiRequest(0), "Was able to send api request");

    Success();
  }
}
