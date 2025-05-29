package hello.itemservice.domain.item;

import lombok.Data;

@Data
public class item {

    private Long id;
    private String itemName;
    private Integer price;
    private Integer quantity;

    public item() {
    }

    public item(String itemName, Integer price, Integer quantity) {
        this.itemName = itemName;
        this.price = price;
        this.quantity = quantity;
    }
}
