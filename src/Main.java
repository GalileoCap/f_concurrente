import Map.Map;

class Main {
  public static void main(String args[]) {
    Map<String> map = new Map<String>();

    String item0 = "Ahoy",
           item1 = "my friend!",
           item2 = "there!";

    map.add(item0);
    map.add(item1);
    map.add(item2);

    map.remove(item1.hashCode());
    System.out.println(map.get(item0.hashCode()));
    System.out.println(map.get(item1.hashCode()));
    System.out.println(map.get(item2.hashCode()));
  }
}
