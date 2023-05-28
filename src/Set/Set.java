package Set;

public interface Set<T> {
  public Boolean add(T newItem);
  public Boolean remove(int key);
  public T find(int key);
}
