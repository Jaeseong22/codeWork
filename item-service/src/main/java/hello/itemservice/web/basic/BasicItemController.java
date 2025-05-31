package hello.itemservice.web.basic;

import hello.itemservice.domain.item.item;
import hello.itemservice.domain.item.itemRepository;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/basic/items")
@RequiredArgsConstructor
public class BasicItemController {

    private final itemRepository itemRepository;

    @GetMapping
    public String items(Model model) {
        List<item> items = itemRepository.findAll();
        model.addAttribute("items", items);
        return "basic/items";
    }

    @GetMapping("/{itemId}")
    public String item(@PathVariable("itemId") long itemId, Model model) {
        item item = itemRepository.findById(itemId);
        model.addAttribute("item", item);
        return "basic/item";
    }

    @GetMapping("/add")
    public String addForm() {
        return "basic/addForm";
    }

    // @PostMapping("/add")
    public String addItemV1(@RequestParam("itemName") String itemName,
                       @RequestParam("price") int price,
                       @RequestParam("quantity") int quantity,
                       Model model) {
        item item = new item();
        item.setItemName(itemName);
        item.setPrice(price);
        item.setQuantity(quantity);

        itemRepository.save(item);

        model.addAttribute("item", item);

        return "basic/item";
    }

//    @PostMapping("/add")
    public String addItemV2(@ModelAttribute("item") item item) {

        itemRepository.save(item);
//        model.addAttribute("item", item);

        return "basic/item";
    }

//    @PostMapping("/add")
    public String addItemV3(@ModelAttribute item item) {

        itemRepository.save(item);
//        model.addAttribute("item", item);

        return "basic/item";
    }

//    @PostMapping("/add")
    public String addItemV4(item item) {

        itemRepository.save(item);
        return "basic/item";
    }

    @PostMapping("/add")
    public String addItemV5(item item) {

        itemRepository.save(item);
        return "redirect:/basic/items/" + item.getId();
    }

    @GetMapping("/{itemId}/edit")
    public String editForm(@PathVariable("itemId") long itemId, Model model) {
        item item = itemRepository.findById(itemId);
        model.addAttribute("item", item);
        return "basic/editForm";
    }

    @PostMapping("/{itemId}/edit")
    public String edit(@PathVariable("itemId") long itemId, @ModelAttribute item item) {
        itemRepository.update(itemId, item);
        return "redirect:/basic/items/{itemId}";
    }

    @PostConstruct
    public void init() {
        itemRepository.save(new item("itemA", 10000, 10));
        itemRepository.save(new item("itemB", 20000, 20));
    }


}
