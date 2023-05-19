package Twiner;

public class User {
  public int userId;
  public int sessionId;
  public int currentPost;

  public User(int _userId, int _sessionId) {
    userId = _userId;
    sessionId = _sessionId;
    currentPost = -1;
  }

  public int hashCode() {
    return userId;
  }
}
