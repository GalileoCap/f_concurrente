package Twiner;

import Map.Map;

class User {
  public int userId;
  public int sessionId;

  public User(int _userId, int _sessionId) {
    userId = _userId;
    sessionId = _sessionId;
  }

  public int hashCode() {
    return userId;
  }
}

public class Twiner {
  private Map<User> loggedIn;

  private int lastSessionId;

  public Twiner() {
    lastSessionId = 1;
    loggedIn = new Map<User>();
  }

  public int logIn(int userId) {
    User user = new User(userId, lastSessionId);
    if (loggedIn.add(user)) { // Success
      lastSessionId++;
      return user.sessionId;
    } else return 0; // Already logged in
  }

  public Boolean logOut(int userId, int sessionId) {
    User user = loggedIn.find(userId);
    if (user == null || user.sessionId != sessionId)
      return false;

    return loggedIn.remove(userId);
  }
}
