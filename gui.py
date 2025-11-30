import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import tkinter.font as tkfont
from database import DatabaseManager
from datetime import datetime

class InventoryManagementSystem:
    """库存管理系统主界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("库存管理系统")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        
        # 初始化数据库
        self.db = DatabaseManager()
        
        # 当前登录用户
        self.current_user = {
            'user_id': 1,
            'username': 'admin',
            'full_name': '系统管理员',
            'role': 'admin'
        }
        
        # 预警通知相关变量
        self.last_alert_check = None
        self.alert_notification_shown = False
        
        # 设置样式
        self.setup_styles()
        
        # 创建主界面
        self.create_main_interface()
        
        # 启动时检查库存预警
        self.check_stock_alerts()
    
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.configure('Title.TLabel', font=('微软雅黑', 16, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('微软雅黑', 12, 'bold'), foreground='#34495e')
        style.configure('Normal.TLabel', font=('微软雅黑', 10))
        style.configure('Accent.TButton', font=('微软雅黑', 10, 'bold'), foreground='white')
    
    def check_stock_alerts(self, manual_check=False):
        """检查库存预警并显示通知
        
        Args:
            manual_check: 是否为手动检查（True表示用户点击按钮）
        """
        try:
            # 获取库存状态数据
            inventory_data = self.db.get_inventory_status()
            
            # 统计预警信息
            low_stock_items = []
            high_stock_items = []
            
            for item in inventory_data:
                if item['status'] == '库存不足':
                    low_stock_items.append(item)
                elif item['status'] == '库存过高':
                    high_stock_items.append(item)
            
            # 显示预警通知的条件：
            # 1. 有预警信息且未显示过通知（自动检查）
            # 2. 有预警信息且是手动检查（用户点击按钮）
            if (low_stock_items or high_stock_items) and (not self.alert_notification_shown or manual_check):
                self.show_alert_notification(low_stock_items, high_stock_items)
                self.alert_notification_shown = True
            
            # 更新最后检查时间
            self.last_alert_check = datetime.now()
            
            # 更新预警统计标签
            self.update_alert_summary()
            
        except Exception as e:
            print(f"检查库存预警时出错: {e}")
    
    def update_alert_summary(self):
        """更新预警统计标签"""
        try:
            # 获取当前预警统计
            low_stock_count, high_stock_count = self.get_alert_summary()
            
            # 查找预警统计标签并更新文本
            for widget in self.content_frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label) and "库存预警" in child.cget("text"):
                            alert_text = f"库存预警: 库存不足 {low_stock_count} 种 | 库存过高 {high_stock_count} 种"
                            child.configure(text=alert_text, 
                                          fg='#e74c3c' if low_stock_count > 0 or high_stock_count > 0 else '#27ae60')
                            break
        except Exception as e:
            print(f"更新预警统计标签时出错: {e}")
    
    def show_alert_notification(self, low_stock_items, high_stock_items):
        """显示库存预警通知"""
        # 构建预警消息
        alert_message = "库存预警通知：\n\n"
        
        if low_stock_items:
            alert_message += f"⚠️ 库存不足物资 ({len(low_stock_items)}种):\n"
            for item in low_stock_items[:5]:  # 最多显示5种
                alert_message += f"   • {item['item_name']} (当前: {item['current_stock']}{item['unit']}, 最低: {item['min_stock']}{item['unit']})\n"
            if len(low_stock_items) > 5:
                alert_message += f"   ... 还有 {len(low_stock_items) - 5} 种物资库存不足\n"
            alert_message += "\n"
        
        if high_stock_items:
            alert_message += f"📦 库存过高物资 ({len(high_stock_items)}种):\n"
            for item in high_stock_items[:5]:  # 最多显示5种
                alert_message += f"   • {item['item_name']} (当前: {item['current_stock']}{item['unit']}, 最高: {item['max_stock']}{item['unit']})\n"
            if len(high_stock_items) > 5:
                alert_message += f"   ... 还有 {len(high_stock_items) - 5} 种物资库存过高\n"
        
        # 显示通知对话框
        messagebox.showwarning("库存预警", alert_message)
    
    def get_alert_summary(self):
        """获取预警摘要信息"""
        try:
            inventory_data = self.db.get_inventory_status()
            
            low_stock_count = 0
            high_stock_count = 0
            
            for item in inventory_data:
                if item['status'] == '库存不足':
                    low_stock_count += 1
                elif item['status'] == '库存过高':
                    high_stock_count += 1
            
            return low_stock_count, high_stock_count
        except Exception as e:
            print(f"获取预警摘要时出错: {e}")
            return 0, 0
        
    def create_main_interface(self):
        """创建主界面"""
        # 创建顶部标题栏
        self.create_header()
        
        # 创建左侧导航栏
        self.create_sidebar()
        
        # 创建主内容区域
        self.create_content_area()
        
        # 默认显示库存状态
        self.show_inventory_status()
    
    def create_header(self):
        """创建顶部标题栏"""
        header_frame = tk.Frame(self.root, bg='#3498db', height=80)
        header_frame.pack(fill='x', side='top')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="库存管理系统", 
                              font=('微软雅黑', 24, 'bold'), 
                              fg='white', bg='#3498db')
        title_label.pack(side='left', padx=20, pady=20)
        
        # 用户信息
        user_info = tk.Label(header_frame, text=f"欢迎，{self.current_user['full_name']}",
                            font=('微软雅黑', 12), fg='white', bg='#3498db')
        user_info.pack(side='right', padx=20, pady=20)
    
    def create_sidebar(self):
        """创建左侧导航栏"""
        sidebar_frame = tk.Frame(self.root, bg='#2c3e50', width=200)
        sidebar_frame.pack(fill='y', side='left')
        sidebar_frame.pack_propagate(False)
        
        # 导航按钮
        nav_buttons = [
            ("库存状态", self.show_inventory_status),
            ("物资类目管理", self.show_category_management),
            ("物资信息管理", self.show_item_management),
            ("物资入库", self.show_stock_in),
            ("物资出库", self.show_stock_out),
            ("入库记录", self.show_stock_in_records),
            ("出库记录", self.show_stock_out_records),
            ("用户管理", self.show_user_management)
        ]
        
        for text, command in nav_buttons:
            btn = tk.Button(sidebar_frame, text=text, command=command,
                          font=('微软雅黑', 11), bg='#34495e', fg='white',
                          relief='flat', width=15, anchor='w')
            btn.pack(fill='x', padx=10, pady=5)
            
            # 鼠标悬停效果
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg='#3498db'))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(bg='#34495e'))
    
    def create_content_area(self):
        """创建主内容区域"""
        self.content_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.content_frame.pack(fill='both', expand=True, side='right', padx=20, pady=20)
    
    def clear_content(self):
        """清空内容区域"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_inventory_status(self):
        """显示库存状态"""
        self.clear_content()
        
        title_label = tk.Label(self.content_frame, text="库存状态", 
                              font=('微软雅黑', 18, 'bold'), bg='#f0f0f0')
        title_label.pack(anchor='w', pady=(0, 10))
        
        # 预警统计和检查按钮
        alert_frame = tk.Frame(self.content_frame, bg='#f0f0f0')
        alert_frame.pack(fill='x', pady=(0, 10))
        
        # 获取预警统计
        low_stock_count, high_stock_count = self.get_alert_summary()
        
        # 预警统计标签
        alert_text = f"库存预警: 库存不足 {low_stock_count} 种 | 库存过高 {high_stock_count} 种"
        alert_label = tk.Label(alert_frame, text=alert_text, 
                              font=('微软雅黑', 11), bg='#f0f0f0',
                              fg='#e74c3c' if low_stock_count > 0 or high_stock_count > 0 else '#27ae60')
        alert_label.pack(side='left', padx=(0, 20))
        
        # 检查预警按钮
        check_alert_btn = tk.Button(alert_frame, text="检查库存预警", 
                                   command=lambda: self.check_stock_alerts(manual_check=True),
                                   font=('微软雅黑', 10), bg='#f39c12', fg='white')
        check_alert_btn.pack(side='left')
        
        # 添加搜索框
        search_frame = tk.Frame(self.content_frame, bg='#f0f0f0')
        search_frame.pack(fill='x', pady=(0, 10))
        
        # 第一行：关键词搜索
        keyword_frame = tk.Frame(search_frame, bg='#f0f0f0')
        keyword_frame.pack(fill='x', pady=(0, 5))
        
        tk.Label(keyword_frame, text="关键词:", bg='#f0f0f0', font=('微软雅黑', 10)).pack(side='left', padx=(0, 5))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(keyword_frame, textvariable=self.search_var, width=30, font=('微软雅黑', 10))
        search_entry.pack(side='left', padx=5)
        
        # 第二行：多条件搜索
        filter_frame = tk.Frame(search_frame, bg='#f0f0f0')
        filter_frame.pack(fill='x', pady=(0, 5))
        
        tk.Label(filter_frame, text="类目:", bg='#f0f0f0', font=('微软雅黑', 10)).pack(side='left', padx=(0, 5))
        
        self.category_filter_var = tk.StringVar(value="全部")
        categories = self.db.get_categories()
        category_names = ["全部"] + [cat['category_name'] for cat in categories]
        category_combo = ttk.Combobox(filter_frame, textvariable=self.category_filter_var, 
                                     values=category_names, width=15, font=('微软雅黑', 9))
        category_combo.pack(side='left', padx=5)
        
        tk.Label(filter_frame, text="状态:", bg='#f0f0f0', font=('微软雅黑', 10)).pack(side='left', padx=(20, 5))
        
        self.status_filter_var = tk.StringVar(value="全部")
        status_combo = ttk.Combobox(filter_frame, textvariable=self.status_filter_var, 
                                   values=["全部", "正常", "库存不足", "库存过高"], width=15, font=('微软雅黑', 9))
        status_combo.pack(side='left', padx=5)
        
        # 第三行：按钮
        button_frame = tk.Frame(search_frame, bg='#f0f0f0')
        button_frame.pack(fill='x')
        
        search_btn = tk.Button(button_frame, text="搜索", command=self.search_inventory,
                              font=('微软雅黑', 10), bg='#3498db', fg='white')
        search_btn.pack(side='left', padx=5)
        
        clear_btn = tk.Button(button_frame, text="清除搜索", command=self.clear_search_inventory,
                             font=('微软雅黑', 10), bg='#95a5a6', fg='white')
        clear_btn.pack(side='left', padx=5)
        
        # 创建表格框架（包含水平和垂直滚动条）
        table_container = tk.Frame(self.content_frame, bg='white')
        table_container.pack(fill='both', expand=True)
        
        # 创建水平滚动条
        h_scrollbar = ttk.Scrollbar(table_container, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # 创建垂直滚动条
        v_scrollbar = ttk.Scrollbar(table_container, orient='vertical')
        v_scrollbar.pack(side='right', fill='y')
        
        # 创建表格
        columns = ('item_code', 'item_name', 'category', 'unit', 'min_stock', 
                  'max_stock', 'current_stock', 'status')
        tree = ttk.Treeview(table_container, columns=columns, show='headings', height=20,
                           xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        # 设置列标题
        tree.heading('item_code', text='物资编码')
        tree.heading('item_name', text='物资名称')
        tree.heading('category', text='类目')
        tree.heading('unit', text='单位')
        tree.heading('min_stock', text='最低库存')
        tree.heading('max_stock', text='最高库存')
        tree.heading('current_stock', text='当前库存')
        tree.heading('status', text='状态')
        
        # 设置列宽
        tree.column('item_code', width=100)
        tree.column('item_name', width=150)
        tree.column('category', width=100)
        tree.column('unit', width=60)
        tree.column('min_stock', width=80)
        tree.column('max_stock', width=80)
        tree.column('current_stock', width=80)
        tree.column('status', width=80)
        
        # 获取库存数据
        inventory_data = self.db.get_inventory_status()
        
        # 添加数据到表格
        for item in inventory_data:
            status_color = '#e74c3c' if item['status'] == '库存不足' else (
                '#f39c12' if item['status'] == '库存过高' else '#27ae60'
            )
            
            tree.insert('', 'end', values=(
                item['item_code'], item['item_name'], item['category_name'],
                item['unit'], item['min_stock'], item['max_stock'],
                item['current_stock'], item['status']
            ), tags=(status_color,))
        
        # 设置标签样式
        tree.tag_configure('#e74c3c', foreground='#e74c3c')
        tree.tag_configure('#f39c12', foreground='#f39c12')
        tree.tag_configure('#27ae60', foreground='#27ae60')
        
        # 配置滚动条
        h_scrollbar.config(command=tree.xview)
        v_scrollbar.config(command=tree.yview)
        
        tree.pack(side='left', fill='both', expand=True)
        
        # 统计信息
        total_items = len(inventory_data)
        low_stock = len([i for i in inventory_data if i['status'] == '库存不足'])
        high_stock = len([i for i in inventory_data if i['status'] == '库存过高'])
        
        stats_frame = tk.Frame(self.content_frame, bg='#f0f0f0')
        stats_frame.pack(fill='x', pady=10)
        
        stats_text = f"总物资数: {total_items} | 库存不足: {low_stock} | 库存过高: {high_stock}"
        stats_label = tk.Label(stats_frame, text=stats_text, 
                              font=('微软雅黑', 12), bg='#f0f0f0')
        stats_label.pack(anchor='w')
    
    def show_category_management(self):
        """显示物资类目管理"""
        self.clear_content()
        
        title_label = tk.Label(self.content_frame, text="物资类目管理", 
                              font=('微软雅黑', 18, 'bold'), bg='#f0f0f0')
        title_label.pack(anchor='w', pady=(0, 20))
        
        # 添加类目按钮
        add_frame = tk.Frame(self.content_frame, bg='#f0f0f0')
        add_frame.pack(fill='x', pady=(0, 10))
        
        add_btn = tk.Button(add_frame, text="添加类目", command=self.add_category_dialog,
                           font=('微软雅黑', 10), bg='#27ae60', fg='white')
        add_btn.pack(side='left')
        
        # 创建表格容器（包含水平和垂直滚动条）
        table_container = tk.Frame(self.content_frame, bg='white')
        table_container.pack(fill='both', expand=True)
        
        # 创建水平滚动条
        h_scrollbar = ttk.Scrollbar(table_container, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # 创建垂直滚动条
        v_scrollbar = ttk.Scrollbar(table_container, orient='vertical')
        v_scrollbar.pack(side='right', fill='y')
        
        # 创建表格
        columns = ('category_id', 'category_name', 'description', 'parent_category', 'created_at')
        tree = ttk.Treeview(table_container, columns=columns, show='headings', height=15,
                           xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        tree.heading('category_id', text='ID')
        tree.heading('category_name', text='类目名称')
        tree.heading('description', text='描述')
        tree.heading('parent_category', text='父类目')
        tree.heading('created_at', text='创建时间')
        
        # 获取类目数据
        categories = self.db.get_categories()
        for category in categories:
            tree.insert('', 'end', values=(
                category['category_id'], category['category_name'],
                category['description'] or '', category['parent_category'] or '',
                category['created_at']
            ))
        
        # 配置滚动条
        h_scrollbar.config(command=tree.xview)
        v_scrollbar.config(command=tree.yview)
        
        tree.pack(side='left', fill='both', expand=True)
    
    def show_item_management(self):
        """显示物资信息管理"""
        self.clear_content()
        
        title_label = tk.Label(self.content_frame, text="物资信息管理", 
                              font=('微软雅黑', 18, 'bold'), bg='#f0f0f0')
        title_label.pack(anchor='w', pady=(0, 10))
        
        # 搜索框架
        search_frame = tk.Frame(self.content_frame, bg='#f0f0f0')
        search_frame.pack(fill='x', pady=(0, 10))
        
        # 第一行：关键词搜索
        keyword_frame = tk.Frame(search_frame, bg='#f0f0f0')
        keyword_frame.pack(fill='x', pady=(0, 5))
        
        tk.Label(keyword_frame, text="关键词:", bg='#f0f0f0', font=('微软雅黑', 10)).pack(side='left', padx=(0, 5))
        
        self.item_search_var = tk.StringVar()
        search_entry = tk.Entry(keyword_frame, textvariable=self.item_search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        # 第二行：多条件搜索
        filter_frame = tk.Frame(search_frame, bg='#f0f0f0')
        filter_frame.pack(fill='x', pady=(0, 5))
        
        tk.Label(filter_frame, text="类目:", bg='#f0f0f0', font=('微软雅黑', 10)).pack(side='left', padx=(0, 5))
        
        self.item_category_filter_var = tk.StringVar(value="全部")
        categories = self.db.get_categories()
        category_names = ["全部"] + [cat['category_name'] for cat in categories]
        category_combo = ttk.Combobox(filter_frame, textvariable=self.item_category_filter_var, 
                                     values=category_names, width=15, font=('微软雅黑', 9))
        category_combo.pack(side='left', padx=5)
        
        tk.Label(filter_frame, text="供应商:", bg='#f0f0f0', font=('微软雅黑', 10)).pack(side='left', padx=(20, 5))
        
        self.supplier_filter_var = tk.StringVar(value="全部")
        suppliers = self.db.get_items()
        supplier_names = ["全部"] + list(set([item['supplier'] for item in suppliers if item['supplier']]))
        supplier_combo = ttk.Combobox(filter_frame, textvariable=self.supplier_filter_var, 
                                     values=supplier_names, width=15, font=('微软雅黑', 9))
        supplier_combo.pack(side='left', padx=5)
        
        # 第三行：按钮
        button_frame = tk.Frame(search_frame, bg='#f0f0f0')
        button_frame.pack(fill='x')
        
        search_btn = tk.Button(button_frame, text="搜索", command=self.search_items,
                              font=('微软雅黑', 9), bg='#3498db', fg='white')
        search_btn.pack(side='left', padx=5)
        
        clear_btn = tk.Button(button_frame, text="清除搜索", command=self.clear_search_items,
                             font=('微软雅黑', 9), bg='#95a5a6', fg='white')
        clear_btn.pack(side='left', padx=5)
        
        # 添加物资按钮
        add_frame = tk.Frame(self.content_frame, bg='#f0f0f0')
        add_frame.pack(fill='x', pady=(0, 10))
        
        add_btn = tk.Button(add_frame, text="添加物资", command=self.add_item_dialog,
                           font=('微软雅黑', 10), bg='#27ae60', fg='white')
        add_btn.pack(side='left')
        
        # 创建表格容器（包含水平和垂直滚动条）
        table_container = tk.Frame(self.content_frame, bg='white')
        table_container.pack(fill='both', expand=True)
        
        # 创建水平滚动条
        h_scrollbar = ttk.Scrollbar(table_container, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # 创建垂直滚动条
        v_scrollbar = ttk.Scrollbar(table_container, orient='vertical')
        v_scrollbar.pack(side='right', fill='y')
        
        # 创建表格
        columns = ('item_id', 'item_code', 'item_name', 'category', 'specification', 
                  'unit', 'supplier', 'purchase_price', 'selling_price')
        self.item_tree = ttk.Treeview(table_container, columns=columns, show='headings', height=15,
                           xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        self.item_tree.heading('item_id', text='ID')
        self.item_tree.heading('item_code', text='物资编码')
        self.item_tree.heading('item_name', text='物资名称')
        self.item_tree.heading('category', text='类目')
        self.item_tree.heading('specification', text='规格')
        self.item_tree.heading('unit', text='单位')
        self.item_tree.heading('supplier', text='供应商')
        self.item_tree.heading('purchase_price', text='采购价')
        self.item_tree.heading('selling_price', text='销售价')
        
        # 获取物资数据
        items = self.db.get_items()
        for item in items:
            self.item_tree.insert('', 'end', values=(
                item['item_id'], item['item_code'], item['item_name'],
                item['category_name'], item['specification'] or '',
                item['unit'], item['supplier'] or '',
                f"¥{item['purchase_price']:.2f}" if item['purchase_price'] else '',
                f"¥{item['selling_price']:.2f}" if item['selling_price'] else ''
            ))
        
        # 配置滚动条
        h_scrollbar.config(command=self.item_tree.xview)
        v_scrollbar.config(command=self.item_tree.yview)
        
        self.item_tree.pack(side='left', fill='both', expand=True)
    
    def show_stock_in(self):
        """显示物资入库界面"""
        self.clear_content()
        
        title_label = tk.Label(self.content_frame, text="物资入库", 
                              font=('微软雅黑', 18, 'bold'), bg='#f0f0f0')
        title_label.pack(anchor='w', pady=(0, 20))
        
        # 创建表单
        form_frame = tk.Frame(self.content_frame, bg='#f0f0f0')
        form_frame.pack(fill='x', pady=10)
        
        # 物资选择
        tk.Label(form_frame, text="选择物资:", bg='#f0f0f0', font=('微软雅黑', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.item_var = tk.StringVar()
        items = self.db.get_items()
        item_names = [f"{item['item_code']} - {item['item_name']}" for item in items]
        item_combo = ttk.Combobox(form_frame, textvariable=self.item_var, values=item_names, width=30)
        item_combo.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        
        # 入库数量
        tk.Label(form_frame, text="入库数量:", bg='#f0f0f0', font=('微软雅黑', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.quantity_var = tk.StringVar()
        quantity_entry = tk.Entry(form_frame, textvariable=self.quantity_var, width=30)
        quantity_entry.grid(row=1, column=1, sticky='w', pady=5, padx=5)
        
        # 单价
        tk.Label(form_frame, text="单价:", bg='#f0f0f0', font=('微软雅黑', 10)).grid(row=2, column=0, sticky='w', pady=5)
        self.price_var = tk.StringVar()
        price_entry = tk.Entry(form_frame, textvariable=self.price_var, width=30)
        price_entry.grid(row=2, column=1, sticky='w', pady=5, padx=5)
        
        # 供应商
        tk.Label(form_frame, text="供应商:", bg='#f0f0f0', font=('微软雅黑', 10)).grid(row=3, column=0, sticky='w', pady=5)
        self.supplier_var = tk.StringVar()
        supplier_entry = tk.Entry(form_frame, textvariable=self.supplier_var, width=30)
        supplier_entry.grid(row=3, column=1, sticky='w', pady=5, padx=5)
        
        # 批次号
        tk.Label(form_frame, text="批次号:", bg='#f0f0f0', font=('微软雅黑', 10)).grid(row=4, column=0, sticky='w', pady=5)
        self.batch_var = tk.StringVar()
        batch_entry = tk.Entry(form_frame, textvariable=self.batch_var, width=30)
        batch_entry.grid(row=4, column=1, sticky='w', pady=5, padx=5)
        
        # 入库按钮
        submit_btn = tk.Button(form_frame, text="确认入库", command=self.submit_stock_in,
                              font=('微软雅黑', 12), bg='#3498db', fg='white', width=15)
        submit_btn.grid(row=5, column=0, columnspan=2, pady=20)
    
    def show_stock_out(self):
        """显示物资出库界面"""
        self.clear_content()
        
        title_label = tk.Label(self.content_frame, text="物资出库", 
                              font=('微软雅黑', 18, 'bold'), bg='#f0f0f0')
        title_label.pack(anchor='w', pady=(0, 20))
        
        # 创建表单
        form_frame = tk.Frame(self.content_frame, bg='#f0f0f0')
        form_frame.pack(fill='x', pady=10)
        
        # 物资选择
        tk.Label(form_frame, text="选择物资:", bg='#f0f0f0', font=('微软雅黑', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.out_item_var = tk.StringVar()
        items = self.db.get_items()
        item_names = [f"{item['item_code']} - {item['item_name']}" for item in items]
        item_combo = ttk.Combobox(form_frame, textvariable=self.out_item_var, values=item_names, width=30)
        item_combo.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        
        # 出库数量
        tk.Label(form_frame, text="出库数量:", bg='#f0f0f0', font=('微软雅黑', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.out_quantity_var = tk.StringVar()
        quantity_entry = tk.Entry(form_frame, textvariable=self.out_quantity_var, width=30)
        quantity_entry.grid(row=1, column=1, sticky='w', pady=5, padx=5)
        
        # 单价
        tk.Label(form_frame, text="单价:", bg='#f0f0f0', font=('微软雅黑', 10)).grid(row=2, column=0, sticky='w', pady=5)
        self.out_price_var = tk.StringVar()
        price_entry = tk.Entry(form_frame, textvariable=self.out_price_var, width=30)
        price_entry.grid(row=2, column=1, sticky='w', pady=5, padx=5)
        
        # 领用人
        tk.Label(form_frame, text="领用人:", bg='#f0f0f0', font=('微软雅黑', 10)).grid(row=3, column=0, sticky='w', pady=5)
        self.recipient_var = tk.StringVar()
        recipient_entry = tk.Entry(form_frame, textvariable=self.recipient_var, width=30)
        recipient_entry.grid(row=3, column=1, sticky='w', pady=5, padx=5)
        
        # 用途
        tk.Label(form_frame, text="用途:", bg='#f0f0f0', font=('微软雅黑', 10)).grid(row=4, column=0, sticky='w', pady=5)
        self.purpose_var = tk.StringVar()
        purpose_entry = tk.Entry(form_frame, textvariable=self.purpose_var, width=30)
        purpose_entry.grid(row=4, column=1, sticky='w', pady=5, padx=5)
        
        # 出库按钮
        submit_btn = tk.Button(form_frame, text="确认出库", command=self.submit_stock_out,
                              font=('微软雅黑', 12), bg='#e74c3c', fg='white', width=15)
        submit_btn.grid(row=5, column=0, columnspan=2, pady=20)
    
    def show_stock_in_records(self):
        """显示入库记录"""
        self.clear_content()
        
        title_label = tk.Label(self.content_frame, text="入库记录", 
                              font=('微软雅黑', 18, 'bold'), bg='#f0f0f0')
        title_label.pack(anchor='w', pady=(0, 20))
        
        # 创建表格容器（包含水平和垂直滚动条）
        table_container = tk.Frame(self.content_frame, bg='white')
        table_container.pack(fill='both', expand=True)
        
        # 创建水平滚动条
        h_scrollbar = ttk.Scrollbar(table_container, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # 创建垂直滚动条
        v_scrollbar = ttk.Scrollbar(table_container, orient='vertical')
        v_scrollbar.pack(side='right', fill='y')
        
        # 创建表格
        columns = ('stock_in_id', 'item_name', 'quantity', 'unit', 'unit_price', 
                  'total_amount', 'supplier', 'batch_number', 'operation_time', 'operator')
        tree = ttk.Treeview(table_container, columns=columns, show='headings', height=15,
                           xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        tree.heading('stock_in_id', text='ID')
        tree.heading('item_name', text='物资名称')
        tree.heading('quantity', text='数量')
        tree.heading('unit', text='单位')
        tree.heading('unit_price', text='单价')
        tree.heading('total_amount', text='总金额')
        tree.heading('supplier', text='供应商')
        tree.heading('batch_number', text='批次号')
        tree.heading('operation_time', text='操作时间')
        tree.heading('operator', text='操作员')
        
        # 获取入库记录
        records = self.db.get_stock_in_records()
        for record in records:
            tree.insert('', 'end', values=(
                record['stock_in_id'], record['item_name'], record['quantity'],
                record['unit'], f"¥{record['unit_price']:.2f}",
                f"¥{record['total_amount']:.2f}", record['supplier'] or '',
                record['batch_number'] or '', record['operation_time'],
                record['operator']
            ))
        
        # 配置滚动条
        h_scrollbar.config(command=tree.xview)
        v_scrollbar.config(command=tree.yview)
        
        tree.pack(side='left', fill='both', expand=True)
    
    def show_stock_out_records(self):
        """显示出库记录"""
        self.clear_content()
        
        title_label = tk.Label(self.content_frame, text="出库记录", 
                              font=('微软雅黑', 18, 'bold'), bg='#f0f0f0')
        title_label.pack(anchor='w', pady=(0, 20))
        
        # 创建表格容器（包含水平和垂直滚动条）
        table_container = tk.Frame(self.content_frame, bg='white')
        table_container.pack(fill='both', expand=True)
        
        # 创建水平滚动条
        h_scrollbar = ttk.Scrollbar(table_container, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # 创建垂直滚动条
        v_scrollbar = ttk.Scrollbar(table_container, orient='vertical')
        v_scrollbar.pack(side='right', fill='y')
        
        # 创建表格
        columns = ('stock_out_id', 'item_name', 'quantity', 'unit', 'unit_price', 
                  'total_amount', 'recipient', 'purpose', 'operation_time', 'operator')
        tree = ttk.Treeview(table_container, columns=columns, show='headings', height=15,
                           xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        tree.heading('stock_out_id', text='ID')
        tree.heading('item_name', text='物资名称')
        tree.heading('quantity', text='数量')
        tree.heading('unit', text='单位')
        tree.heading('unit_price', text='单价')
        tree.heading('total_amount', text='总金额')
        tree.heading('recipient', text='领用人')
        tree.heading('purpose', text='用途')
        tree.heading('operation_time', text='操作时间')
        tree.heading('operator', text='操作员')
        
        # 获取出库记录
        records = self.db.get_stock_out_records()
        for record in records:
            tree.insert('', 'end', values=(
                record['stock_out_id'], record['item_name'], record['quantity'],
                record['unit'], f"¥{record['unit_price']:.2f}",
                f"¥{record['total_amount']:.2f}", record['recipient'] or '',
                record['purpose'] or '', record['operation_time'],
                record['operator']
            ))
        
        # 配置滚动条
        h_scrollbar.config(command=tree.xview)
        v_scrollbar.config(command=tree.yview)
        
        tree.pack(side='left', fill='both', expand=True)
    
    def show_user_management(self):
        """显示用户管理界面"""
        self.clear_content()
        
        title_label = tk.Label(self.content_frame, text="用户管理", 
                              font=('微软雅黑', 18, 'bold'), bg='#f0f0f0')
        title_label.pack(anchor='w', pady=(0, 20))
        
        # 添加用户按钮
        add_frame = tk.Frame(self.content_frame, bg='#f0f0f0')
        add_frame.pack(fill='x', pady=(0, 10))
        
        add_btn = tk.Button(add_frame, text="添加用户", command=self.add_user_dialog,
                           font=('微软雅黑', 10), bg='#27ae60', fg='white')
        add_btn.pack(side='left')
        
        # 创建表格容器（包含水平和垂直滚动条）
        table_container = tk.Frame(self.content_frame, bg='white')
        table_container.pack(fill='both', expand=True)
        
        # 创建水平滚动条
        h_scrollbar = ttk.Scrollbar(table_container, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # 创建垂直滚动条
        v_scrollbar = ttk.Scrollbar(table_container, orient='vertical')
        v_scrollbar.pack(side='right', fill='y')
        
        # 创建表格
        columns = ('user_id', 'username', 'full_name', 'role', 'created_at')
        tree = ttk.Treeview(table_container, columns=columns, show='headings', height=15,
                           xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        tree.heading('user_id', text='ID')
        tree.heading('username', text='用户名')
        tree.heading('full_name', text='姓名')
        tree.heading('role', text='角色')
        tree.heading('created_at', text='创建时间')
        
        # 获取用户数据
        users = self.db.get_users()
        for user in users:
            tree.insert('', 'end', values=(
                user['user_id'], user['username'], user['full_name'],
                user['role'], user['created_at']
            ))
        
        # 配置滚动条
        h_scrollbar.config(command=tree.xview)
        v_scrollbar.config(command=tree.yview)
        
        tree.pack(side='left', fill='both', expand=True)
    
    # 对话框方法
    def add_category_dialog(self):
        """添加类目对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加物资类目")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="类目名称:").pack(pady=5)
        name_entry = tk.Entry(dialog, width=30)
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="描述:").pack(pady=5)
        desc_entry = tk.Entry(dialog, width=30)
        desc_entry.pack(pady=5)
        
        def submit():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            if name:
                if self.db.add_category(name, desc):
                    messagebox.showinfo("成功", "类目添加成功")
                    dialog.destroy()
                    self.show_category_management()
                else:
                    messagebox.showerror("错误", "类目名称已存在")
            else:
                messagebox.showerror("错误", "请输入类目名称")
        
        tk.Button(dialog, text="确认", command=submit).pack(pady=10)
    
    def add_item_dialog(self):
        """添加物资对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加物资")
        dialog.geometry("500x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 创建滚动窗口
        canvas = tk.Canvas(dialog)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 布局滚动窗口
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 表单字段
        fields = {
            "物资编码:": (tk.StringVar(), tk.Entry),
            "物资名称:": (tk.StringVar(), tk.Entry),
            "规格:": (tk.StringVar(), tk.Entry),
            "单位:": (tk.StringVar(), tk.Entry),
            "供应商:": (tk.StringVar(), tk.Entry),
            "采购价:": (tk.StringVar(), tk.Entry),
            "销售价:": (tk.StringVar(), tk.Entry),
            "最低库存:": (tk.StringVar(value="0"), tk.Entry),
            "最高库存:": (tk.StringVar(value="9999"), tk.Entry)
        }
        
        # 添加类目选择
        tk.Label(scrollable_frame, text="类目:", font=("微软雅黑", 10)).grid(row=0, column=0, sticky="w", pady=5)
        category_var = tk.StringVar()
        categories = self.db.get_categories()
        category_names = [cat['category_name'] for cat in categories]
        category_combo = ttk.Combobox(scrollable_frame, textvariable=category_var, values=category_names, width=30)
        if category_names:
            category_combo.current(0)
        category_combo.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        
        # 添加其他字段
        row = 1
        for label_text, (var, widget_type) in fields.items():
            tk.Label(scrollable_frame, text=label_text, font=("微软雅黑", 10)).grid(row=row, column=0, sticky="w", pady=5)
            widget = widget_type(scrollable_frame, textvariable=var, width=30)
            widget.grid(row=row, column=1, sticky="w", pady=5, padx=5)
            row += 1
        
        def submit():
            # 获取表单数据
            category_name = category_var.get()
            item_code = fields["物资编码:"][0].get()
            item_name = fields["物资名称:"][0].get()
            specification = fields["规格:"][0].get()
            unit = fields["单位:"][0].get()
            supplier = fields["供应商:"][0].get()
            purchase_price = fields["采购价:"][0].get()
            selling_price = fields["销售价:"][0].get()
            min_stock = fields["最低库存:"][0].get()
            max_stock = fields["最高库存:"][0].get()
            
            # 验证必填字段
            if not all([item_code, item_name, unit]):
                messagebox.showerror("错误", "请填写必填字段：物资编码、物资名称、单位")
                return
            
            # 验证数字字段
            try:
                purchase_price = float(purchase_price) if purchase_price else 0
                selling_price = float(selling_price) if selling_price else 0
                min_stock = int(min_stock) if min_stock else 0
                max_stock = int(max_stock) if max_stock else 0
            except ValueError:
                messagebox.showerror("错误", "价格和库存必须是数字")
                return
            
            # 获取类目ID
            category_id = None
            for cat in categories:
                if cat['category_name'] == category_name:
                    category_id = cat['category_id']
                    break
            
            # 添加物资
            try:
                success = self.db.add_item(
                    item_code=item_code,
                    item_name=item_name,
                    category_id=category_id,
                    specification=specification,
                    unit=unit,
                    supplier=supplier,
                    purchase_price=purchase_price,
                    selling_price=selling_price,
                    min_stock=min_stock,
                    max_stock=max_stock
                )
                
                if success:
                    messagebox.showinfo("成功", "物资添加成功")
                    dialog.destroy()
                    # 刷新物资列表
                    self.show_item_management()
                else:
                    messagebox.showerror("错误", "添加物资失败，请检查物资编码是否重复")
            except Exception as e:
                messagebox.showerror("错误", f"添加物资时出错：{str(e)}")
        
        # 添加按钮
        btn_frame = tk.Frame(scrollable_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="确认添加", command=submit, 
                 font=("微软雅黑", 10), bg="#27ae60", fg="white", width=15).pack(side="left", padx=10)
        tk.Button(btn_frame, text="取消", command=dialog.destroy, 
                 font=("微软雅黑", 10), bg="#95a5a6", fg="white", width=15).pack(side="left", padx=10)
    
    def add_user_dialog(self):
        """添加用户对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加用户")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="用户名:").pack(pady=5)
        username_entry = tk.Entry(dialog, width=30)
        username_entry.pack(pady=5)
        
        tk.Label(dialog, text="密码:").pack(pady=5)
        password_entry = tk.Entry(dialog, width=30, show='*')
        password_entry.pack(pady=5)
        
        tk.Label(dialog, text="姓名:").pack(pady=5)
        fullname_entry = tk.Entry(dialog, width=30)
        fullname_entry.pack(pady=5)
        
        tk.Label(dialog, text="角色:").pack(pady=5)
        role_var = tk.StringVar(value='user')
        role_combo = ttk.Combobox(dialog, textvariable=role_var, values=['admin', 'user'], width=27)
        role_combo.pack(pady=5)
        
        def submit():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            fullname = fullname_entry.get().strip()
            role = role_var.get()
            
            if username and password and fullname:
                if self.db.add_user(username, password, fullname, role):
                    messagebox.showinfo("成功", "用户添加成功")
                    dialog.destroy()
                    self.show_user_management()
                else:
                    messagebox.showerror("错误", "用户名已存在")
            else:
                messagebox.showerror("错误", "请填写完整信息")
        
        tk.Button(dialog, text="确认", command=submit).pack(pady=10)
    
    def search_inventory(self):
        """搜索库存状态"""
        keyword = self.search_var.get().strip()
        category_filter = self.category_filter_var.get()
        status_filter = self.status_filter_var.get()
        
        # 如果所有条件都是默认值，显示所有数据
        if not keyword and category_filter == "全部" and status_filter == "全部":
            self._update_inventory_table(self.db.get_inventory_status())
            messagebox.showinfo("提示", "显示所有库存记录")
            return
        
        # 调用数据库搜索方法
        results = self.db.search_inventory_status(keyword, category_filter, status_filter)
        
        # 更新表格显示
        self._update_inventory_table(results)
        
        # 显示搜索结果统计
        messagebox.showinfo("搜索结果", f"找到 {len(results)} 条匹配记录")
    
    def clear_search_inventory(self):
        """清除搜索条件"""
        self.search_var.set("")
        self.category_filter_var.set("全部")
        self.status_filter_var.set("全部")
        self._update_inventory_table(self.db.get_inventory_status())
        messagebox.showinfo("提示", "已清除搜索条件，显示所有库存记录")
    
    def search_items(self):
        """搜索物资信息"""
        keyword = self.item_search_var.get().strip()
        category_filter = self.item_category_filter_var.get()
        supplier_filter = self.supplier_filter_var.get()
        
        # 如果所有条件都是默认值，显示所有数据
        if not keyword and category_filter == "全部" and supplier_filter == "全部":
            self._update_item_table(self.db.get_items())
            messagebox.showinfo("提示", "显示所有物资记录")
            return
        
        # 调用数据库搜索方法
        results = self.db.search_items(keyword, category_filter, supplier_filter)
        
        # 更新表格内容
        self._update_item_table(results)
        
        # 显示搜索结果统计
        messagebox.showinfo("搜索结果", f"找到 {len(results)} 条匹配记录")
    
    def clear_search_items(self):
        """清除物资搜索"""
        self.item_search_var.set("")
        self.item_category_filter_var.set("全部")
        self.supplier_filter_var.set("全部")
        # 恢复显示所有数据
        results = self.db.get_items()
        self._update_item_table(results)
        messagebox.showinfo("提示", "已清除搜索条件，显示所有物资记录")
    
    def _update_item_table(self, data):
        """更新物资信息表格"""
        # 清空表格
        for item in self.item_tree.get_children():
            self.item_tree.delete(item)
        
        # 添加新数据
        for item in data:
            self.item_tree.insert('', 'end', values=(
                item['item_id'], item['item_code'], item['item_name'],
                item['category_name'], item['specification'] or '',
                item['unit'], item['supplier'] or '',
                f"¥{item['purchase_price']:.2f}" if item['purchase_price'] else '',
                f"¥{item['selling_price']:.2f}" if item['selling_price'] else ''
            ))
    
    def _update_inventory_table(self, data):
        """更新库存表格数据"""
        # 查找表格容器
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children():
                # 查找Treeview组件
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Treeview):
                        # 清空现有数据
                        child.delete(*child.get_children())
                        
                        # 添加新数据
                        for item in data:
                            status_color = '#e74c3c' if item['status'] == '库存不足' else (
                                '#f39c12' if item['status'] == '库存过高' else '#27ae60'
                            )
                            
                            child.insert('', 'end', values=(
                                item['item_code'], item['item_name'], item['category_name'],
                                item['unit'], item['min_stock'], item['max_stock'],
                                item['current_stock'], item['status']
                            ), tags=(status_color,))
                        return
    
    def submit_stock_in(self):
        """提交入库操作"""
        try:
            # 获取表单数据
            item_selection = self.item_var.get()
            quantity = self.quantity_var.get()
            unit_price = self.price_var.get()
            supplier = self.supplier_var.get()
            batch_number = self.batch_var.get()
            
            # 验证必填字段
            if not item_selection:
                messagebox.showerror("错误", "请选择物资")
                return
            if not quantity:
                messagebox.showerror("错误", "请输入入库数量")
                return
            if not unit_price:
                messagebox.showerror("错误", "请输入单价")
                return
            
            # 验证数据格式
            try:
                quantity = int(quantity)
                unit_price = float(unit_price)
            except ValueError:
                messagebox.showerror("错误", "数量和单价必须是数字")
                return
            
            # 验证数据合理性
            if quantity <= 0:
                messagebox.showerror("错误", "入库数量必须大于0")
                return
            if unit_price < 0:
                messagebox.showerror("错误", "单价不能为负数")
                return
            
            # 解析物资选择
            item_code = item_selection.split(' - ')[0]
            
            # 获取物资信息
            items = self.db.get_items()
            item_id = None
            for item in items:
                if item['item_code'] == item_code:
                    item_id = item['item_id']
                    break
            
            if not item_id:
                messagebox.showerror("错误", "未找到选择的物资")
                return
            
            # 执行入库操作
            success = self.db.stock_in(
                item_id=item_id,
                quantity=quantity,
                unit_price=unit_price,
                supplier=supplier,
                batch_number=batch_number,
                operator_id=self.current_user['user_id']
            )
            
            if success:
                messagebox.showinfo("成功", "入库操作成功")
                # 清空表单
                self.item_var.set("")
                self.quantity_var.set("")
                self.price_var.set("")
                self.supplier_var.set("")
                self.batch_var.set("")
                
                # 入库后检查库存预警
                self.alert_notification_shown = False  # 重置通知状态
                self.check_stock_alerts()
            else:
                messagebox.showerror("错误", "入库操作失败")
                
        except Exception as e:
            messagebox.showerror("错误", f"入库操作出错：{str(e)}")
    
    def submit_stock_out(self):
        """提交出库操作"""
        try:
            # 获取表单数据
            item_selection = self.out_item_var.get()
            quantity = self.out_quantity_var.get()
            unit_price = self.out_price_var.get()
            recipient = self.recipient_var.get()
            purpose = self.purpose_var.get()
            
            # 验证必填字段
            if not item_selection:
                messagebox.showerror("错误", "请选择物资")
                return
            if not quantity:
                messagebox.showerror("错误", "请输入出库数量")
                return
            if not unit_price:
                messagebox.showerror("错误", "请输入单价")
                return
            if not recipient:
                messagebox.showerror("错误", "请输入领用人")
                return
            
            # 验证数据格式
            try:
                quantity = int(quantity)
                unit_price = float(unit_price)
            except ValueError:
                messagebox.showerror("错误", "数量和单价必须是数字")
                return
            
            # 验证数据合理性
            if quantity <= 0:
                messagebox.showerror("错误", "出库数量必须大于0")
                return
            if unit_price < 0:
                messagebox.showerror("错误", "单价不能为负数")
                return
            
            # 解析物资选择
            item_code = item_selection.split(' - ')[0]
            
            # 获取物资信息
            items = self.db.get_items()
            item_id = None
            for item in items:
                if item['item_code'] == item_code:
                    item_id = item['item_id']
                    break
            
            if not item_id:
                messagebox.showerror("错误", "未找到选择的物资")
                return
            
            # 检查库存是否足够
            inventory = self.db.get_inventory_status()
            current_stock = 0
            for item in inventory:
                if item['item_code'] == item_code:
                    current_stock = item['current_stock']
                    break
            
            if current_stock < quantity:
                messagebox.showerror("错误", f"库存不足，当前库存：{current_stock}")
                return
            
            # 执行出库操作
            success = self.db.stock_out(
                item_id=item_id,
                quantity=quantity,
                unit_price=unit_price,
                recipient=recipient,
                purpose=purpose,
                operator_id=self.current_user['user_id']
            )
            
            if success:
                messagebox.showinfo("成功", "出库操作成功")
                # 清空表单
                self.out_item_var.set("")
                self.out_quantity_var.set("")
                self.out_price_var.set("")
                self.recipient_var.set("")
                self.purpose_var.set("")
                
                # 出库后检查库存预警
                self.alert_notification_shown = False  # 重置通知状态
                self.check_stock_alerts()
            else:
                messagebox.showerror("错误", "出库操作失败")
                
        except Exception as e:
            messagebox.showerror("错误", f"出库操作出错：{str(e)}")

def main():
    """主函数"""
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()