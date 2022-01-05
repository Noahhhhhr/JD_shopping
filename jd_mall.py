import pymysql
from datetime import datetime
import time


class JD(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root',
                                    password="******", database='jd',
                                    charset='utf8')
        self.cs = self.conn.cursor()
        self.logged_in = False
        self.customer_id = 0
        self.cart = []

    def __del__(self):
        self.cs.close()
        self.conn.close()

    def log_in(self):
        user_name = input("请输入用户名(q返回上一层):\t")
        if user_name == 'q':
            self.reg_log()
            return
        password = input('请输入密码：\t')
        sql = """SELECT id, name, password FROM customers WHERE name=%s;"""
        self.cs.execute(sql, [user_name])
        user_info = self.cs.fetchone()
        if not user_info:
            print("用户不存在！")
            return
        if user_info[2] != password:
            print("密码错误！")
            return
        print("登陆成功！")
        self.logged_in = True
        self.customer_id = user_info[0]

    def sign_up(self):
        user_name = input("请输入用户名(q返回上一层):\t")
        if user_name == 'q':
            self.reg_log()
            return
        password = input('请输入密码：\t')
        sql = """SELECT name FROM customers WHERE name=%s;"""
        self.cs.execute(sql, [user_name])
        if self.cs.rowcount:
            print("用户已存在！")
            return
        address = input("请输入地址：\n")
        tel = input("请输入电话号码：\n")
        try:
            statement = "INSERT INTO customers VALUES (%s, %s, %s, %s, %s);"
            self.cs.execute(statement, [0, user_name, address, tel, password])
            self.conn.commit()
            print("注册成功！请重新登录！")
        except:
            print("注册失败！")
        self.log_in()

    def show_all_items(self):
        """显示所有商品"""
        sql = """SELECT g.id, g.name, g.price, c.name, b.name FROM goods AS g 
                LEFT JOIN goods_cates AS c ON g.cate_id=c.id
                LEFT JOIN goods_brands AS b on g.brand_id=b.id;"""
        self.cs.execute(sql)
        for temp in self.cs.fetchall():
            print(temp)
        self.select_items()

    def show_cates(self):
        """显示所有商品分类"""
        sql = "SELECT * FROM goods_cates;"
        self.cs.execute(sql)
        for temp in self.cs.fetchall():
            print(temp)
        cate_num = input("请选择所要查看的分类序号(返回上一层:q)：\n")
        if cate_num == 'q':
            return
        sql1 = """SELECT g.id, g.name, g.price, c.name, b.name FROM goods AS g 
                LEFT JOIN goods_cates AS c ON g.cate_id=c.id
                LEFT JOIN goods_brands AS b on g.brand_id=b.id
                WHERE g.cate_id=%s;"""
        try:
            self.cs.execute(sql1, [cate_num])
            for temp in self.cs.fetchall():
                print(temp)
            self.select_items()
        except:
            print("输入内容有误!")

    def show_brands(self):
        """显示所有商品品牌"""
        sql = "SELECT * FROM goods_brands;"
        self.cs.execute(sql)
        for temp in self.cs.fetchall():
            print(temp)
        brand_num = input("请选择所要查看的品牌序号(返回上一层:q)：\n")
        if brand_num == 'q':
            return
        sql1 = """SELECT g.id, g.name, g.price, c.name, b.name FROM goods AS g 
                LEFT JOIN goods_cates AS c ON g.cate_id=c.id
                LEFT JOIN goods_brands AS b on g.brand_id=b.id
                WHERE g.brand_id=%s;"""
        try:
            self.cs.execute(sql1, [brand_num])
            for temp in self.cs.fetchall():
                print(temp)
            self.select_items()
        except:
            print("输入内容有误!")

    def get_info_by_name(self):
        find_name = input("请输入要查询的商品名(返回上一层:q)：\n")
        if find_name == 'q':
            return
        sql = f"""SELECT * FROM goods WHERE name=%s;"""
        self.cs.execute(sql, [find_name])
        if not self.cs.rowcount:
            print("商品不存在")
            return
        for temp in self.cs.fetchall():
            print(temp)
        self.select_items()

    def select_items(self):
        num = input("请输入想购买商品的序号(返回上一层：q)：\n")
        if num == "q":
            return
        sql = "SELECT id, name, price FROM goods WHERE id=%s;"
        self.cs.execute(sql, [num])
        if self.cs.rowcount:
            item = self.cs.fetchone()
            item_num = 0
            while item_num < 1:
                item_num = int(input("请输入购买数量：\n"))
            print(f"已添加{item_num}个{item[1]}到购物车。")
            self.add_to_cart(item[0], item[1], item_num, item[2])

    def add_to_cart(self, id, name, num, price):
        self.cart.append([id, name, num, price])
        message = input("是否查看购物车？（y/n）")
        if message == "y":
            self.check_cart()
        else:
            return

    def check_cart(self):
        if not self.cart:
            print("购物车为空！")
            return
        for items in self.cart:
            print(f"{items[1]}: {items[2]}个\t")
        message = input("是否结账？（y/n）")
        if message == "y":
            self.check_out()
        else:
            return

    def check_out(self):
        sum_price = 0
        for items in self.cart:
            single_price = float(items[2]) * float(items[3])
            print(f'{items[1]} {items[2]}:\t{single_price}元')
            sum_price += single_price
        print(f"总价：\n{sum_price}元")
        prompt = input("是否支付？(y/n)")
        if prompt == "y":
            self.add_order(sum_price)
        else:
            pass

    def add_order(self, sum_price):
        sql = """INSERT INTO orders VALUES (%s, %s, %s, %s);"""
        purchase_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cs.execute(sql, [0, purchase_time, self.customer_id, sum_price])
        self.conn.commit()
        sql1 = """SELECT * FROM orders 
                WHERE order_date_time = %s AND customer_id = %s;"""
        self.cs.execute(sql1, [purchase_time, self.customer_id])
        order_id = self.cs.fetchone()[0]
        sql2 = "INSERT INTO order_details VALUES (%s, %s, %s, %s);"
        purchase_list = []
        while self.cart:
            purchase_list.append(self.cart.pop())
        for items in purchase_list:
            self.cs.execute(sql2, [0, order_id, items[0], items[2]])
        self.conn.commit()
        print(f"购买成功，共支付{sum_price}元。")

    @staticmethod
    def print_menu():
        print("------JD Mall------")
        print("1.所有商品")
        print("2.商品分类")
        print("3.商品品牌")
        print("4.根据名字查询商品")
        print("5.查看购物车")
        print("退出登录并返回上一层：q")
        num = input("请输入功能对应序号：\n")
        return num

    @staticmethod
    def print_log():
        print("------JD Mall------")
        print("您是否有京东账户？")
        print("1.已是会员")
        print("2.现在注册")
        num = input("请输入对应序号（退出：q）：\n")
        return num

    def reg_log(self):
        num = self.print_log()
        if num == "1":
            self.log_in()
        if num == '2':
            self.sign_up()
        if num == 'q':
            exit()

    def show_goods(self):
        num = self.print_menu()
        if num == "1":
            self.show_all_items()
        elif num == "2":
            self.show_cates()
        elif num == "3":
            self.show_brands()
        elif num == "4":
            self.get_info_by_name()
        elif num == "5":
            self.check_cart()
        elif num == "q":
            self.logged_in = False
        else:
            print("输入有误，请重新输入...")

    def run(self):
        while True:
            if not self.logged_in:
                self.reg_log()
            else:
                self.show_goods()


def main():
    # 创建一个京东商城对象
    jd = JD()
    # 调用对象的run方法
    jd.run()


if __name__ == '__main__':
    main()
