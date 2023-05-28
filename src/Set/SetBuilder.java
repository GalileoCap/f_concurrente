package Set;

import Set.*;

public class SetBuilder {
  public String type;

  public SetBuilder(String _type) {
    type = _type;
  }

  public <T> Set<T> newSet() {
    return switch (type) {
      case "free" -> new SetFree<T>();
      case "lazy" -> new SetLazy<T>();
      case "optimistic" -> new SetO<T>();
      case "fine-grained" -> new SetFG<T>();
      case "monitor" -> new SetMonitor<T>();
      default -> null; // TODO: Error
    };
  }
}
