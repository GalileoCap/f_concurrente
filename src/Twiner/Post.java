package Twiner;

public class Post {
  public int ownerId;
  public int date;

  public Post(int _ownerId, int _date) {
    ownerId = _ownerId;
    date = _date;
  }

  public int hashCode() {
    return date;
  }
}
