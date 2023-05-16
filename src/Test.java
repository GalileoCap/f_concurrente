package Test;

import Test.MapTest;

class RunTests {
  public static void main(String args[]) {
    MapTest.run();
  }
}

class Test {
  //public static void run();

  public static void printCase(String suiteName, String caseName) {
    System.out.print(String.format("%s::%s", suiteName, caseName));
  }

  public static void success() {
    System.out.println(" SUCCESS");
  }

  public static void error() {
    System.out.println(" ERROR");
  }

  public static void fail() {
    System.out.println(" FAIL");
    System.exit(1);
  }
}

