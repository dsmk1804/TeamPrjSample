package dto;


import lombok.*;

@Getter
@Setter
@ToString
@AllArgsConstructor
@NoArgsConstructor
public class Product {
    private int idx;
    private String name;
    private int price;
    private int quantity;
}
