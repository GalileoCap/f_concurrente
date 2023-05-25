package Twiner;

import Map.*;

public class Twiner {
  private Map<Integer> loggedIn;

  private MapBuilder mapBuilder;

  public Twiner(String mapType) {
    mapBuilder = new MapBuilder(mapType);

    loggedIn = mapBuilder.newMap();
  }
  
  public Boolean logIn(int userId) {
    return loggedIn.add(userId);
  }

  public Boolean logOut(int userId) {
    return loggedIn.remove(userId);
  }

  public Boolean apiRequest(int userId) {
    return loggedIn.find(userId) != null;
  }
}
