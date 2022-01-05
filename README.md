# JD_shopping

来自 [b站某MySQL课程](https://www.bilibili.com/video/BV1Fx411d7E)的作业。
学规划的转行菜鸡初次使用Python和MySQL设计简单的JD商城购物系统。

使用E-R模型，在JD数据库中共有goods, goods_cates. goods_brands, customers, orders, order_deails六个表。
读取前三个表中的商品信息，并将购买信息和用户信息储存在后三个表中。

## 登录

1. 增加类属性储存登陆状态，如果未登录则运行脚本询问登录还是注册。
2. 登录模块中输入用户名和密码并查询数据库，cursor对象为空则提示无用户，如果不为空与cursor中的密码匹配，符合即登陆成功，不匹配则提示密码错误，重新输入。
3. 注册模块中输入用户名并查询数据，重名则提示，不重名则提示输入密码（<20），然后一次输入地址和电话，并添加进数据库。
4. 使用变量储存用户id。

## 商品查看和选择

1. 完成登录或注册后查看、搜索商品和查看购物车。增加类属性以字典形式保存购物车内容。
2. 如需购买，输入商品对应的id，不需要则r返回搜索界面，退出输入q。

## 购买

1. 选择好商品和数量后，将储存的用户ID插入orders表，然后提示是否确认订单，确认``commit()``则将信息插入order_details表中。
1. 是否继续购物（y/n），返回商品查看和搜索模块。

## End

太多地方都做的很差，菜鸡第一步吧。加油。
