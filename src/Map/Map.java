package Map;

public interface Map<T> {
  public Boolean add(T newItem);
  public Boolean remove(int key);
  public T findAfter(int key);
  public T find(int key);
}
