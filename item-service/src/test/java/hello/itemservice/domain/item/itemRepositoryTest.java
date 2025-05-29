package hello.itemservice.domain.item;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.assertj.core.api.Assertions.*;

class itemRepositoryTest {

    itemRepository itemRepository = new itemRepository();

    @AfterEach
    void afterEach() {
        itemRepository.clearStore();
    }

    @Test
    void save() {
        item item = new item("itemA", 10000, 10);

        item saveItem = itemRepository.save(item);

        item finditem = itemRepository.findById(saveItem.getId());
        assertThat(finditem).isEqualTo(saveItem);
    }

    @Test
    void findAll() {
        item item1 = new item("item1", 10000, 10);
        item item2 = new item("item2", 20000, 20);

        itemRepository.save(item1);
        itemRepository.save(item2);

        List<item> result = itemRepository.findAll();

        assertThat(result.size()).isEqualTo(2);
        assertThat(result).contains(item1, item2);
    }

    @Test
    void updateItem() {
        item item1 = new item("item1", 10000, 10);

        item savedItem = itemRepository.save(item1);
        long itemid = savedItem.getId();

        item updateparam = new item("item2", 20000, 30);

        itemRepository.update(itemid, updateparam);

        item finditem = itemRepository.findById(itemid);

        assertThat(finditem.getItemName()).isEqualTo(updateparam.getItemName());
        assertThat(finditem.getPrice()).isEqualTo(updateparam.getPrice());
        assertThat(finditem.getQuantity()).isEqualTo(updateparam.getQuantity());
    }
}