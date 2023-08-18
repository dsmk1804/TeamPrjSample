package dto;

import lombok.*;

@Getter
@Setter
@ToString
@AllArgsConstructor
@NoArgsConstructor
@Builder

public class Post {
    private int idx;
    private String content;
}
