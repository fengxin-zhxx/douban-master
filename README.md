# douban-master
---
## 功能

数据获取: 使用爬虫工具, 在豆瓣TOP250榜单, 猫眼网票房排行榜上爬取电影相关数据, 如评分,票房等

数据持久化: 使用pandas中的DataFrame存储csv的方式和MySQL关系型数据库存储两种方式分别实现持久化

可视化分析: 从持久化的数据中选取相应数据的关系进行可视化分析

票房预测: 通过可视化分析得到的结论, 选取可能影响票房的因素, 建立预测模型和算法, 进行预测

## 技术栈

Python爬虫与数据处理: requests,  lxml,  re,  pandas  

数据持久化: pymysql,  pandas,  MySQL   

数据清洗: pandas,  MySQL (实际上没做)

可视化分析: pyecharts,  matplotlib, SQL,  pandas

模型预测: sklearn,  numpy,  matplotlib


## 可视化举例
![p1](./result/p%20(1).png)
![p2](./result/p%20(2).png)
![p3](./result/p%20(3).png)
![p4](./result/p%20(4).png)
![p5](./result/p%20(5).png)
![p6](./result/p%20(6).png)
![p7](./result/p%20(7).png)
![p8](./result/p%20(8).png)
![p9](./result/p%20(9).png)
![p10](./result/p%20(10).png)
![p11](./result/p%20(11).png)



## 票房预测举例
单位/万元

![p1](./result/预测1.png)

![p2](./result/预测2.png)









