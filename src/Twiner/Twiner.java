package Twiner;

import Map.*;

public class Twiner {
  private Map<User> loggedIn;

  private MapBuilder mapBuilder;
  private int lastSessionId;

  public Twiner(String mapType) {
    mapBuilder = new MapBuilder(mapType);

    lastSessionId = 0;
    loggedIn = mapBuilder.newMap();
  }
  
  private User findUser(int userId, int sessionId) {
    User user = loggedIn.find(userId);
    if (user == null || user.sessionId != sessionId)
      return null;
    return user;
  }

  private Boolean checkUser(int userId, int sessionId) {
    User user = findUser(userId, sessionId);
    return user != null;
  }

  public int logIn(int userId) {
    User user = new User(userId, lastSessionId);
    if (!loggedIn.add(user)) // Already logged in
      return -1;

    lastSessionId++;
    return user.sessionId;
  }

  public Boolean logOut(int userId, int sessionId) {
    if (!checkUser(userId, sessionId))
      return false;

    return loggedIn.remove(userId);
  }

  public Boolean apiRequest(int userId, int sessionId) {
    return checkUser(userId, sessionId);
  }
}
