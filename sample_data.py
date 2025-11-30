#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例数据生成器
用于创建丰富的测试数据
"""

import sqlite3
from datetime import datetime, timedelta
import random

class SampleDataGenerator:
    """示例数据生成器"""
    
    def __init__(self, db_path="inventory.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    
    def generate_comprehensive_data(self):
        """生成完整的示例数据"""
        print("开始生成完整的示例数据...")
        
        # 清空现有数据（保留管理员用户）
        self._clear_existing_data()
        
        # 生成基础数据
        self._generate_categories()
        self._generate_users()
        self._generate_items()
        
        # 生成业务数据
        self._generate_stock_records()
        
        print("示例数据生成完成！")
    
    def _clear_existing_data(self):
        """清空现有数据"""
        tables = ['categories', 'items', 'inventory', 'stock_in', 'stock_out']
        for table in tables:
            self.cursor.execute(f"DELETE FROM {table}")
        # 保留管理员用户
        self.cursor.execute("DELETE FROM users WHERE username != 'admin'")
        self.conn.commit()
    
    def _generate_categories(self):
        """生成物资类目"""
        categories = [
            # 一级类目
            ("办公用品", "办公文具和日常用品", None),
            ("电子设备", "电脑、打印机等电子设备", None),
            ("耗材", "打印机墨盒、纸张等消耗品", None),
            ("工具设备", "维修和操作工具", None),
            ("清洁用品", "清洁和卫生用品", None),
            ("劳保用品", "劳动保护用品", None),
            
            # 办公用品子类目
            ("文具", "书写和办公文具", 1),
            ("纸张", "各种规格的纸张", 1),
            ("文件夹", "文件整理用品", 1),
            
            # 电子设备子类目
            ("电脑", "台式机和笔记本电脑", 2),
            ("打印机", "各种类型的打印机", 2),
            ("网络设备", "路由器和交换机", 2),
            
            # 耗材子类目
            ("打印耗材", "墨盒和硒鼓", 3),
            ("办公耗材", "其他办公消耗品", 3),
            
            # 工具设备子类目
            ("手动工具", "螺丝刀、钳子等", 4),
            ("电动工具", "电钻、角磨机等", 4),
            ("测量工具", "尺子、万用表等", 4),
            
            # 清洁用品子类目
            ("清洁剂", "各种清洁液体", 5),
            ("清洁工具", "拖把、抹布等", 5),
            
            # 劳保用品子类目
            ("防护用品", "手套、口罩等", 6),
            ("安全设备", "安全帽、护目镜等", 6)
        ]
        
        for name, description, parent_id in categories:
            self.cursor.execute('''
                INSERT INTO categories (category_name, description, parent_category_id)
                VALUES (?, ?, ?)
            ''', (name, description, parent_id))
        
        self.conn.commit()
        print("✓ 生成物资类目数据")
    
    def _generate_users(self):
        """生成用户数据"""
        users = [
            ("manager", "manager123", "张经理", "admin"),
            ("warehouse", "warehouse123", "李仓库管理员", "user"),
            ("operator1", "op123456", "王操作员", "user"),
            ("operator2", "op123456", "赵操作员", "user"),
            ("finance", "finance123", "钱财务", "user"),
            ("purchaser", "purchase123", "孙采购员", "user")
        ]
        
        for username, password, fullname, role in users:
            self.cursor.execute('''
                INSERT INTO users (username, password, full_name, role)
                VALUES (?, ?, ?, ?)
            ''', (username, password, fullname, role))
        
        self.conn.commit()
        print("✓ 生成用户数据")
    
    def _generate_items(self):
        """生成物资信息"""
        # 获取类目ID映射
        self.cursor.execute("SELECT category_id, category_name FROM categories")
        categories = {row[1]: row[0] for row in self.cursor.fetchall()}
        
        items = [
            # 文具类
            ("BG001", "A4打印纸", categories["纸张"], "80g/包，500张", "包", "亚太森博", 25.0, 30.0, 10, 200),
            ("BG002", "中性笔", categories["文具"], "0.5mm黑色，12支装", "盒", "真彩", 15.0, 20.0, 20, 500),
            ("BG003", "文件夹", categories["文件夹"], "A4蓝色，带标签", "个", "得力", 3.0, 5.0, 30, 300),
            ("BG004", "笔记本", categories["文具"], "A5，100页", "本", "晨光", 5.0, 8.0, 20, 400),
            ("BG005", "订书机", categories["文具"], "标准型", "个", "可得优", 12.0, 18.0, 5, 50),
            
            # 电子设备类
            ("DZ001", "笔记本电脑", categories["电脑"], "ThinkPad X1 Carbon", "台", "联想", 8000.0, 9500.0, 2, 20),
            ("DZ002", "激光打印机", categories["打印机"], "HP LaserJet Pro", "台", "惠普", 1500.0, 1800.0, 1, 10),
            ("DZ003", "显示器", categories["电脑"], "24寸IPS", "台", "戴尔", 1200.0, 1500.0, 3, 30),
            ("DZ004", "路由器", categories["网络设备"], "千兆无线", "台", "TP-LINK", 200.0, 250.0, 2, 20),
            ("DZ005", "扫描仪", categories["打印机"], "高速文档扫描", "台", "富士通", 3000.0, 3500.0, 1, 5),
            
            # 耗材类
            ("HC001", "打印机墨盒", categories["打印耗材"], "HP 305黑色", "个", "惠普", 80.0, 100.0, 5, 50),
            ("HC002", "硒鼓", categories["打印耗材"], "DR-3350", "个", "兄弟", 300.0, 380.0, 2, 20),
            ("HC003", "复印纸", categories["纸张"], "70g/包", "包", "亚太森博", 20.0, 25.0, 15, 150),
            ("HC004", "色带", categories["打印耗材"], "LQ-630K", "个", "爱普生", 15.0, 20.0, 10, 100),
            ("HC005", "墨粉", categories["打印耗材"], "TN-2335", "瓶", "佳能", 150.0, 180.0, 3, 30),
            
            # 工具类
            ("GJ001", "螺丝刀套装", categories["手动工具"], "24件套", "套", "世达", 150.0, 200.0, 2, 20),
            ("GJ002", "万用表", categories["测量工具"], "数字式", "个", "福禄克", 300.0, 380.0, 1, 10),
            ("GJ003", "电烙铁", categories["电动工具"], "60W可调温", "个", "白光", 80.0, 100.0, 3, 30),
            ("GJ004", "钳子", categories["手动工具"], "8寸斜口钳", "把", "史丹利", 25.0, 35.0, 5, 50),
            ("GJ005", "电钻", categories["电动工具"], "13mm冲击钻", "台", "博世", 400.0, 500.0, 1, 10),
            
            # 清洁用品类
            ("QJ001", "洗手液", categories["清洁剂"], "500ml", "瓶", "蓝月亮", 15.0, 20.0, 5, 50),
            ("QJ002", "垃圾袋", categories["清洁工具"], "45*50cm", "卷", "美丽雅", 8.0, 12.0, 10, 100),
            ("QJ003", "抹布", categories["清洁工具"], "超细纤维", "包", "3M", 5.0, 8.0, 20, 200),
            ("QJ004", "消毒液", categories["清洁剂"], "1L", "瓶", "威露士", 25.0, 35.0, 3, 30),
            ("QJ005", "拖把", categories["清洁工具"], "旋转拖把", "个", "美丽雅", 50.0, 70.0, 2, 20),
            
            # 劳保用品类
            ("LB001", "安全帽", categories["安全设备"], "ABS材质", "个", "3M", 30.0, 45.0, 5, 50),
            ("LB002", "防护手套", categories["防护用品"], "丁腈材质", "双", "安思尔", 5.0, 8.0, 20, 200),
            ("LB003", "护目镜", categories["安全设备"], "防冲击", "个", "霍尼韦尔", 15.0, 25.0, 10, 100),
            ("LB004", "口罩", categories["防护用品"], "KN95", "包", "3M", 20.0, 30.0, 50, 500),
            ("LB005", "安全鞋", categories["安全设备"], "防砸防刺", "双", "代尔塔", 200.0, 280.0, 2, 20)
        ]
        
        for item_data in items:
            self.cursor.execute('''
                INSERT INTO items (item_code, item_name, category_id, specification, 
                                 unit, supplier, purchase_price, selling_price, 
                                 min_stock, max_stock)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', item_data)
        
        self.conn.commit()
        print("✓ 生成物资信息数据")
    
    def _generate_stock_records(self):
        """生成库存记录"""
        # 获取物资和用户列表
        self.cursor.execute("SELECT item_id, item_name, purchase_price FROM items")
        items = self.cursor.fetchall()
        
        self.cursor.execute("SELECT user_id FROM users")
        users = [row[0] for row in self.cursor.fetchall()]
        
        # 生成入库记录（过去30天内）
        start_date = datetime.now() - timedelta(days=30)
        
        for item_id, item_name, purchase_price in items:
            # 每个物资生成2-5次入库记录
            for i in range(random.randint(2, 5)):
                # 随机日期
                days_ago = random.randint(0, 30)
                operation_time = start_date + timedelta(days=days_ago, 
                                                       hours=random.randint(8, 17),
                                                       minutes=random.randint(0, 59))
                
                quantity = random.randint(10, 100)
                batch_number = f"BATCH{operation_time.strftime('%Y%m%d')}{i+1:02d}"
                operator_id = random.choice(users)
                
                # 计算金额
                unit_price = purchase_price * random.uniform(0.9, 1.1)  # 价格波动±10%
                total_amount = quantity * unit_price
                
                # 添加入库记录
                self.cursor.execute('''
                    INSERT INTO stock_in (item_id, quantity, unit_price, total_amount,
                                        supplier, batch_number, operator_id, operation_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (item_id, quantity, unit_price, total_amount, 
                      "示例供应商", batch_number, operator_id, operation_time))
                
                # 更新库存
                self.cursor.execute('''
                    INSERT OR REPLACE INTO inventory (item_id, quantity, batch_number)
                    VALUES (?, COALESCE((SELECT quantity FROM inventory WHERE item_id=? AND batch_number=?), 0) + ?, ?)
                ''', (item_id, item_id, batch_number, quantity, batch_number))
        
        # 生成出库记录（过去15天内）
        start_date = datetime.now() - timedelta(days=15)
        
        for item_id, item_name, selling_price in items:
            # 每个物资生成1-3次出库记录
            for i in range(random.randint(1, 3)):
                # 随机日期
                days_ago = random.randint(0, 15)
                operation_time = start_date + timedelta(days=days_ago,
                                                       hours=random.randint(8, 17),
                                                       minutes=random.randint(0, 59))
                
                # 获取当前库存
                self.cursor.execute("SELECT SUM(quantity) FROM inventory WHERE item_id=?", (item_id,))
                current_stock = self.cursor.fetchone()[0] or 0
                
                if current_stock > 0:
                    quantity = random.randint(1, min(20, current_stock))
                    operator_id = random.choice(users)
                    
                    # 计算金额
                    unit_price = selling_price * random.uniform(0.95, 1.05)  # 价格波动±5%
                    total_amount = quantity * unit_price
                    
                    # 添加出库记录
                    self.cursor.execute('''
                        INSERT INTO stock_out (item_id, quantity, unit_price, total_amount,
                                            recipient, purpose, operator_id, operation_time)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (item_id, quantity, unit_price, total_amount,
                          "示例领用人", "日常领用", operator_id, operation_time))
                    
                    # 更新库存（从最早批次开始出库）
                    self.cursor.execute('''
                        SELECT inventory_id, quantity FROM inventory 
                        WHERE item_id=? AND quantity > 0 
                        ORDER BY created_at LIMIT 1
                    ''', (item_id,))
                    
                    result = self.cursor.fetchone()
                    if result:
                        inv_id, inv_quantity = result
                        new_quantity = inv_quantity - quantity
                        
                        if new_quantity > 0:
                            self.cursor.execute("UPDATE inventory SET quantity=? WHERE inventory_id=?", 
                                             (new_quantity, inv_id))
                        else:
                            self.cursor.execute("DELETE FROM inventory WHERE inventory_id=?", (inv_id,))
        
        self.conn.commit()
        print("✓ 生成库存记录数据")
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()

def create_sample_data():
    """创建示例数据"""
    generator = SampleDataGenerator()
    try:
        generator.generate_comprehensive_data()
        print("\n示例数据创建成功！")
        print("包含：")
        print("- 30个物资类目（包含子类目）")
        print("- 6个系统用户")
        print("- 25种物资信息")
        print("- 丰富的入库出库记录")
        print("- 完整的库存数据")
    except Exception as e:
        print(f"创建示例数据失败: {e}")
    finally:
        generator.close()

if __name__ == "__main__":
    create_sample_data()