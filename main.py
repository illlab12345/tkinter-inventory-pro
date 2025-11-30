import sys
import os
from database import DatabaseManager
from gui import main as gui_main

def initialize_sample_data():
    """初始化示例数据"""
    db = DatabaseManager()
    
    # 检查是否已有数据
    categories = db.get_categories()
    if len(categories) > 1:  # 已经有数据（包含默认类目）
        return
    
    print("正在初始化示例数据...")
    
    # 添加物资类目
    categories_data = [
        ("办公用品", "办公文具和耗材"),
        ("电子设备", "电脑、打印机等电子设备"),
        ("耗材", "打印机墨盒、纸张等消耗品"),
        ("工具", "维修和操作工具"),
        ("清洁用品", "清洁和卫生用品")
    ]
    
    for category_name, description in categories_data:
        db.add_category(category_name, description)
    
    # 获取类目ID
    categories = db.get_categories()
    category_map = {cat['category_name']: cat['category_id'] for cat in categories}
    
    # 添加物资信息
    items_data = [
        # 办公用品
        ("BG001", "A4打印纸", category_map["办公用品"], "80g/包", "包", "晨光文具", 25.00, 30.00, 10, 200),
        ("BG002", "中性笔", category_map["办公用品"], "0.5mm黑色", "支", "真彩文具", 2.50, 3.50, 50, 500),
        ("BG003", "文件夹", category_map["办公用品"], "A4蓝色", "个", "得力文具", 3.00, 5.00, 20, 200),
        
        # 电子设备
        ("DZ001", "笔记本电脑", category_map["电子设备"], "ThinkPad X1 Carbon", "台", "联想", 8000.00, 9500.00, 2, 20),
        ("DZ002", "激光打印机", category_map["电子设备"], "HP LaserJet Pro", "台", "惠普", 1500.00, 1800.00, 1, 10),
        ("DZ003", "显示器", category_map["电子设备"], "24寸IPS", "台", "戴尔", 1200.00, 1500.00, 3, 30),
        
        # 耗材
        ("HC001", "打印机墨盒", category_map["耗材"], "HP 305黑色", "个", "惠普", 80.00, 100.00, 5, 50),
        ("HC002", "硒鼓", category_map["耗材"], "DR-3350", "个", "兄弟", 300.00, 380.00, 2, 20),
        ("HC003", "复印纸", category_map["耗材"], "70g/包", "包", "亚太森博", 20.00, 25.00, 15, 150),
        
        # 工具
        ("GJ001", "螺丝刀套装", category_map["工具"], "24件套", "套", "世达", 150.00, 200.00, 2, 20),
        ("GJ002", "万用表", category_map["工具"], "数字式", "个", "福禄克", 300.00, 380.00, 1, 10),
        ("GJ003", "电烙铁", category_map["工具"], "60W可调温", "个", "白光", 80.00, 100.00, 3, 30),
        
        # 清洁用品
        ("QJ001", "洗手液", category_map["清洁用品"], "500ml", "瓶", "蓝月亮", 15.00, 20.00, 5, 50),
        ("QJ002", "垃圾袋", category_map["清洁用品"], "45*50cm", "卷", "美丽雅", 8.00, 12.00, 10, 100),
        ("QJ003", "抹布", category_map["清洁用品"], "超细纤维", "包", "3M", 5.00, 8.00, 20, 200)
    ]
    
    for item_data in items_data:
        db.add_item(*item_data)
    
    # 添加示例用户
    users_data = [
        ("manager", "manager123", "张经理", "admin"),
        ("operator1", "op123456", "李操作员", "user"),
        ("operator2", "op123456", "王操作员", "user")
    ]
    
    for user_data in users_data:
        db.add_user(*user_data)
    
    # 添加示例入库记录
    items = db.get_items()
    for i, item in enumerate(items):
        # 为每个物资添加一些初始库存
        quantity = [100, 50, 200, 10, 5, 8, 30, 15, 80, 12, 6, 10, 25, 40, 60][i % 15]
        price = item['purchase_price'] or 10.0
        
        db.stock_in(
            item_id=item['item_id'],
            quantity=quantity,
            unit_price=price,
            supplier=item['supplier'] or "默认供应商",
            batch_number=f"BATCH2024{i+1:03d}",
            operator_id=1
        )
    
    print("示例数据初始化完成！")

def main():
    """主函数"""
    try:
        # 初始化示例数据
        initialize_sample_data()
        
        # 启动GUI界面
        print("启动库存管理系统...")
        gui_main()
        
    except Exception as e:
        print(f"系统启动失败: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()