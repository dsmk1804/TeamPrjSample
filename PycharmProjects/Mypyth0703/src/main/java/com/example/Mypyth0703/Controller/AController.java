package com.example.Mypyth0703.Controller;

import dao.PostsRepository;
import dto.People;
import dto.Product;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;

@Controller
public class AController {
    @Autowired
    DataSource ds;

    @Autowired
    PostsRepository postsrepository;

    @GetMapping("/")
    public String index(Model model) {
        ArrayList<People> al = new ArrayList<>();
        ArrayList<Product> products = new ArrayList<>();
        Connection conn = null;

        try {
            conn= ds.getConnection();
            PreparedStatement pstmt
                    = conn.prepareStatement("select * from people");
            ResultSet rs = pstmt.executeQuery();
            while (rs.next()) {
                String name = rs.getString("name");
                String age = rs.getString("age");
                People temp = new People(name, age);
                al.add(temp);
            }
            pstmt
                    = conn.prepareStatement("select * from products");
            rs = pstmt.executeQuery();
            while (rs.next()) {
                String name = rs.getString("name");
                int price = rs.getInt("price");
                int quantitiy = rs.getInt("quantity");
                int idx = rs.getInt("idx");
                Product p = new Product(idx, name,price,quantitiy);
                products.add(p);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (conn != null) try {
                conn.close();
            } catch (Exception e) {
            }
        }
        model.addAttribute("al", al);
        model.addAttribute("products", products);
        return "index";
    }

    @PostMapping("/post")
    public String post(String content, HttpServletRequest request){
        System.out.println("헬로");
        System.out.println(content);
        postsrepository.doInsert(content);
        return "index";
    }
}


