package Test;

import Test.SetTest;

class RunTests {
  public static void main(String args[]) {
    SetTest.run();
  }
}

class Test {
  //public static void run();

  static void printCase(String suiteName, String caseName) {
    System.err.print(String.format("%s::%s", suiteName, caseName));
  }

  static void Success(String msg) {
    System.err.println(String.format(" SUCCESS: %s", msg));
  }
  static void Success() {
    System.err.println(" SUCCESS");
  }

  static void Error(String msg) {
    System.err.println(String.format(" ERROR: %s", msg));
  }
  static void Error() {
    System.err.println(" ERROR");
  }

  static void Fail(String msg) {
    System.err.println(String.format(" FAIL: %s", msg));
    System.exit(1);
  }
  static void Fail() {
    System.err.println(" FAIL");
    System.exit(1);
  }

  static Boolean Expect(Boolean cond, String msg) {
    if (!cond) Error(msg);
    return cond;
  }
  static Boolean Expect(Boolean cond) {
    if (!cond) Error();
    return cond;
  }

  static void Assert(Boolean cond, String msg) {
    if (!cond) Fail(msg);
  }
  static void Assert(Boolean cond) {
    if (!cond) Fail();
  }
}

