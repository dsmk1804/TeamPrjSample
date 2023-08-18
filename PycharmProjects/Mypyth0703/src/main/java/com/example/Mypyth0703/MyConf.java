package com.example.Mypyth0703;


import org.apache.commons.dbcp2.BasicDataSource;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.sql.DataSource;

@Configuration
public class MyConf {

     @Bean
     public DataSource dataSource(){
         BasicDataSource dbs = new BasicDataSource();
         dbs.setUrl("jdbc:mysql://localhost:3306/kcs");
         dbs.setDriverClassName("com.mysql.jdbc.Driver");
         dbs.setUsername("root");
         dbs.setPassword("1234");
         dbs.setInitialSize(10);
         return dbs;

     }
}
