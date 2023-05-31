package Map;

import Map.*;

public class MapBuilder {
  public String type;

  public MapBuilder(String _type) {
    type = _type;
  }

  public <T> Map<T> newMap() {
    return switch (type) {
      case "free" -> new MapFree<T>();
      case "optimistic" -> new MapO<T>();
      case "fine-grained" -> new MapFG<T>();
      default -> null; // TODO: Error
    };
  }
}
