package Twiner;

import Map.*;

public class Twiner {
  private Map<User> loggedIn;
  private Map<Post> posts;

  private MapBuilder mapBuilder;
  private int lastSessionId;
  private int date;

  public Twiner(String mapType) {
    mapBuilder = new MapBuilder(mapType);

    lastSessionId = 0;
    loggedIn = mapBuilder.newMap();

    date = 0;
    posts = mapBuilder.newMap();
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

  public int newPost(int userId, int sessionId) {
    if (!checkUser(userId, sessionId))
      return -1;

    Post post = new Post(userId, date++);
    if (!posts.add(post))
      return -1;

    return post.date;
  }

  public Boolean removePost(int date, int userId, int sessionId) {
    if (!checkUser(userId, sessionId))
      return false;

    Post post = posts.find(date);
    if (post == null || post.ownerId != userId)
      return false;

    return posts.remove(date);
  }

  public int nextPost(int userId, int sessionId) {
    User user = findUser(userId, sessionId);
    if (user == null)
      return -1;

    Post post = posts.findAfter(user.currentPost);
    if (post == null)
      return -1;

    user.currentPost = post.date;
    return user.currentPost;
  }
}