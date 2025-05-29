package hello.itemservice.web.basic;

import hello.itemservice.domain.item.item;
import hello.itemservice.domain.item.itemRepository;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

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

    @PostConstruct
    public void init() {
        itemRepository.save(new item("itemA", 10000, 10));
        itemRepository.save(new item("itemB", 20000, 20));
    }
}
