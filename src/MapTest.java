package Test;

import Test.Test;
import Map.Map;

class MapTest extends Test {
  public static void run() {
    testFindNull();
    testAddAndFind();
    testAddAndFindMany();
    testRemove();
    testFindAfter();
  }

  static void testFindNull() {
    printCase("Map", "findNull");

    Map<String> m = new Map<String>();
    String s = m.find(0);

    Assert(s == null);

    Success();
  }

  static void testAddAndFind() {
    printCase("Map", "addAndFind");

    Map<String> m = new Map<String>();
    String s = "Ahoy there!";
    int key = s.hashCode();
    
    m.add(s);

    Assert(m.find(key) == s, "Couldn't find"); 
    Assert(m.find(key+1) == null, "Found another key");

    Success();
  }

  static void testAddAndFindMany() {
    printCase("Map", "addAndFindMany");

    Map<String> m = new Map<String>();
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

  static void testRemove() {
    printCase("Map", "addAndRemove");

    Map<String> m = new Map<String>();
    String s = "Ahoy there!";
    int key = s.hashCode();
    
    m.add(s);
    m.remove(key);

    Assert(m.find(key) == null, "Still found s"); 

    Success();
  }

 static void testFindAfter() {
    printCase("Map", "findAfter");

    class Item {
      int hash;
      public Item(int _hash) {
        hash = _hash;
      }

      public int hashCode() {
        return hash;
      }
    }

    Map<Item> m = new Map<Item>();
    Item i0 = new Item(0);
    Item i1 = new Item(1);
    
    m.add(i0);
    m.add(i1);

    Assert(m.findAfter(0) == i1, "Couldn't find i1"); 
    Assert(m.findAfter(1) == null, "Found another element");

    Success();
  }
}
