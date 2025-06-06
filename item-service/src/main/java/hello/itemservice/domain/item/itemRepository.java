package hello.itemservice.domain.item;

import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Repository
public class itemRepository {

    private static final Map<Long, item> store = new HashMap<>(); //static
    private static long sequence = 0L; //static

    public item save(item item) {
        item.setId(++sequence);
        store.put(item.getId(), item);
        return item;
    }

    public item findById(Long id) {
        return store.get(id);
    }

    public List<item> findAll() {
        return new ArrayList<>(store.values());
    }

    public void update(long itemid, item updateParam) {
        item finditem = findById(itemid);
        finditem.setItemName(updateParam.getItemName());
        finditem.setPrice(updateParam.getPrice());
        finditem.setQuantity(updateParam.getQuantity());
    }

    public void clearStore() {
        store.clear();
    }

}
