package Test;

import Test.Test;
import Map.*;

class MapTest<T> extends Test {
  public static void run() {
    String[] types = {"free", "optimistic", "fine-grained"};
    for (String type : types) {
      MapBuilder mb = new MapBuilder(type);
      testFindNull(mb);
      testAddAndFind(mb);
      testAddAndFindMany(mb);
      testRemove(mb);
    }
  }

  static void testFindNull(MapBuilder mb) {
    printCase(String.format("Map(%s)", mb.type), "findNull");

    Map<String> m = mb.newMap();
    String s = m.find(0);

    Assert(s == null);

    Success();
  }

  static void testAddAndFind(MapBuilder mb) {
    printCase(String.format("Map(%s)", mb.type), "addAndFind");

    Map<String> m = mb.newMap();
    String s = "Ahoy there!";
    int key = s.hashCode();
    
    m.add(s);

    Assert(m.find(key) == s, "Couldn't find"); 
    Assert(m.find(key+1) == null, "Found another key");

    Success();
  }

  static void testAddAndFindMany(MapBuilder mb) {
    printCase(String.format("Map(%s)", mb.type), "addAndFindMany");

    Map<String> m = mb.newMap();
    String s0 = "Ahoy there!";
    String s1 = "My friend!";
    int k0 = s0.hashCode();
    int k1 = s1.hashCode();
    
    m.add(s0);
    m.add(s1);

    Assert(m.find(k0) == s0, "Couldn't find s0"); 
    Assert(m.find(k1) == s1, "Couldn't find s1");

    Success();
  }

  static void testRemove(MapBuilder mb) {
    printCase(String.format("Map(%s)", mb.type), "addAndRemove");

    Map<String> m = mb.newMap();
    String s = "Ahoy there!";
    int key = s.hashCode();
    
    m.add(s);
    m.remove(key);

    Assert(m.find(key) == null, "Still found s"); 

    Success();
  }
}

