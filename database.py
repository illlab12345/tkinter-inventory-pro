import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class DatabaseManager:
    """库存管理系统数据库管理器"""
    
    def __init__(self, db_path: str = "inventory.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建用户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建物资类目表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT UNIQUE NOT NULL,
                description TEXT,
                parent_category_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_category_id) REFERENCES categories (category_id)
            )
        ''')
        
        # 创建物资基本信息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_code TEXT UNIQUE NOT NULL,
                item_name TEXT NOT NULL,
                category_id INTEGER NOT NULL,
                specification TEXT,
                unit TEXT NOT NULL,
                supplier TEXT,
                purchase_price REAL,
                selling_price REAL,
                min_stock INTEGER DEFAULT 0,
                max_stock INTEGER DEFAULT 1000,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (category_id)
            )
        ''')
        
        # 创建库存表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                location TEXT,
                batch_number TEXT,
                production_date DATE,
                expiry_date DATE,
                status TEXT DEFAULT '正常',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id) REFERENCES items (item_id)
            )
        ''')
        
        # 创建入库记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_in (
                stock_in_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL,
                total_amount REAL,
                supplier TEXT,
                batch_number TEXT,
                production_date DATE,
                expiry_date DATE,
                operator_id INTEGER NOT NULL,
                operation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (item_id) REFERENCES items (item_id),
                FOREIGN KEY (operator_id) REFERENCES users (user_id)
            )
        ''')
        
        # 创建出库记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_out (
                stock_out_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL,
                total_amount REAL,
                recipient TEXT,
                purpose TEXT,
                operator_id INTEGER NOT NULL,
                operation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (item_id) REFERENCES items (item_id),
                FOREIGN KEY (operator_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # 插入默认管理员用户
        self._create_default_admin()
    
    def _create_default_admin(self):
        """创建默认管理员用户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查是否已存在管理员用户
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO users (username, password, full_name, role)
                VALUES (?, ?, ?, ?)
            ''', ('admin', 'admin123', '系统管理员', 'admin'))
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query: str, params: Tuple = ()):
        """执行查询并返回结果"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.close()
        return result
    
    def execute_update(self, query: str, params: Tuple = ()):
        """执行更新操作"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
    
    # 用户管理相关方法
    def add_user(self, username: str, password: str, full_name: str, role: str) -> bool:
        """添加用户"""
        try:
            self.execute_update('''
                INSERT INTO users (username, password, full_name, role)
                VALUES (?, ?, ?, ?)
            ''', (username, password, full_name, role))
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_users(self) -> List[Dict]:
        """获取所有用户"""
        result = self.execute_query('''
            SELECT user_id, username, full_name, role, created_at
            FROM users ORDER BY user_id
        ''')
        return [{
            'user_id': row[0],
            'username': row[1],
            'full_name': row[2],
            'role': row[3],
            'created_at': row[4]
        } for row in result]
    
    # 物资类目管理相关方法
    def add_category(self, category_name: str, description: str = "", parent_category_id: int = None) -> bool:
        """添加物资类目"""
        try:
            self.execute_update('''
                INSERT INTO categories (category_name, description, parent_category_id)
                VALUES (?, ?, ?)
            ''', (category_name, description, parent_category_id))
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_categories(self) -> List[Dict]:
        """获取所有类目"""
        result = self.execute_query('''
            SELECT c.category_id, c.category_name, c.description, 
                   p.category_name as parent_category, c.created_at
            FROM categories c
            LEFT JOIN categories p ON c.parent_category_id = p.category_id
            ORDER BY c.category_id
        ''')
        return [{
            'category_id': row[0],
            'category_name': row[1],
            'description': row[2],
            'parent_category': row[3],
            'created_at': row[4]
        } for row in result]
    
    # 物资基本信息管理相关方法
    def add_item(self, item_code: str, item_name: str, category_id: int, 
                 specification: str = "", unit: str = "个", supplier: str = "",
                 purchase_price: float = 0.0, selling_price: float = 0.0,
                 min_stock: int = 0, max_stock: int = 1000) -> bool:
        """添加物资基本信息"""
        try:
            self.execute_update('''
                INSERT INTO items (item_code, item_name, category_id, specification, 
                                 unit, supplier, purchase_price, selling_price, 
                                 min_stock, max_stock)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (item_code, item_name, category_id, specification, unit, 
                  supplier, purchase_price, selling_price, min_stock, max_stock))
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_items(self) -> List[Dict]:
        """获取所有物资信息"""
        result = self.execute_query('''
            SELECT i.item_id, i.item_code, i.item_name, c.category_name, 
                   i.specification, i.unit, i.supplier, i.purchase_price, 
                   i.selling_price, i.min_stock, i.max_stock, i.created_at
            FROM items i
            JOIN categories c ON i.category_id = c.category_id
            ORDER BY i.item_id
        ''')
        return [{
            'item_id': row[0],
            'item_code': row[1],
            'item_name': row[2],
            'category_name': row[3],
            'specification': row[4],
            'unit': row[5],
            'supplier': row[6],
            'purchase_price': row[7],
            'selling_price': row[8],
            'min_stock': row[9],
            'max_stock': row[10],
            'created_at': row[11]
        } for row in result]

    def search_items(self, keyword: str) -> List[Dict]:
        """按物资代码或名称搜索物资"""
        result = self.execute_query('''
            SELECT i.item_id, i.item_code, i.item_name, c.category_name, 
                   i.specification, i.unit, i.supplier, i.purchase_price, 
                   i.selling_price, i.min_stock, i.max_stock, i.created_at
            FROM items i
            JOIN categories c ON i.category_id = c.category_id
            WHERE i.item_code LIKE ? OR i.item_name LIKE ?
            ORDER BY i.item_id
        ''', (f'%{keyword}%', f'%{keyword}%'))
        return [{
            'item_id': row[0],
            'item_code': row[1],
            'item_name': row[2],
            'category_name': row[3],
            'specification': row[4],
            'unit': row[5],
            'supplier': row[6],
            'purchase_price': row[7],
            'selling_price': row[8],
            'min_stock': row[9],
            'max_stock': row[10],
            'created_at': row[11]
        } for row in result]

    def search_inventory_status(self, keyword: str) -> List[Dict]:
        """按物资代码或名称搜索库存状态"""
        result = self.execute_query('''
            SELECT i.item_id, i.item_code, i.item_name, c.category_name, 
                   i.unit, i.min_stock, i.max_stock,
                   COALESCE(SUM(inv.quantity), 0) as current_stock,
                   CASE 
                       WHEN COALESCE(SUM(inv.quantity), 0) <= i.min_stock THEN '库存不足'
                       WHEN COALESCE(SUM(inv.quantity), 0) >= i.max_stock THEN '库存过高'
                       ELSE '正常'
                   END as status
            FROM items i
            JOIN categories c ON i.category_id = c.category_id
            LEFT JOIN inventory inv ON i.item_id = inv.item_id
            WHERE i.item_code LIKE ? OR i.item_name LIKE ?
            GROUP BY i.item_id
            ORDER BY i.item_id
        ''', (f'%{keyword}%', f'%{keyword}%'))
        
        return [{
            'item_id': row[0],
            'item_code': row[1],
            'item_name': row[2],
            'category_name': row[3],
            'unit': row[4],
            'min_stock': row[5],
            'max_stock': row[6],
            'current_stock': row[7],
            'status': row[8]
        } for row in result]
    
    # 库存管理相关方法
    def stock_in(self, item_id: int, quantity: int, unit_price: float, 
                 supplier: str = "", batch_number: str = "", 
                 production_date: str = None, expiry_date: str = None,
                 operator_id: int = 1, notes: str = "") -> bool:
        """物资入库"""
        try:
            total_amount = quantity * unit_price
            
            # 添加入库记录
            self.execute_update('''
                INSERT INTO stock_in (item_id, quantity, unit_price, total_amount,
                                    supplier, batch_number, production_date, expiry_date,
                                    operator_id, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (item_id, quantity, unit_price, total_amount, supplier, 
                  batch_number, production_date, expiry_date, operator_id, notes))
            
            # 更新库存
            self._update_inventory(item_id, quantity, batch_number, 
                                 production_date, expiry_date)
            
            return True
        except Exception as e:
            print(f"入库失败: {e}")
            return False
    
    def stock_out(self, item_id: int, quantity: int, unit_price: float,
                  recipient: str = "", purpose: str = "", 
                  operator_id: int = 1, notes: str = "") -> bool:
        """物资出库"""
        try:
            # 检查库存是否足够
            current_stock = self.get_current_stock(item_id)
            if current_stock < quantity:
                return False
            
            total_amount = quantity * unit_price
            
            # 添加出库记录
            self.execute_update('''
                INSERT INTO stock_out (item_id, quantity, unit_price, total_amount,
                                     recipient, purpose, operator_id, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (item_id, quantity, unit_price, total_amount, 
                  recipient, purpose, operator_id, notes))
            
            # 更新库存
            self._update_inventory(item_id, -quantity)
            
            return True
        except Exception as e:
            print(f"出库失败: {e}")
            return False
    
    def _update_inventory(self, item_id: int, quantity: int, 
                         batch_number: str = "", production_date: str = None,
                         expiry_date: str = None):
        """更新库存"""
        # 检查是否已存在该批次库存
        if batch_number:
            result = self.execute_query('''
                SELECT inventory_id, quantity FROM inventory 
                WHERE item_id = ? AND batch_number = ?
            ''', (item_id, batch_number))
            
            if result:
                # 更新现有批次库存
                inventory_id, current_quantity = result[0]
                new_quantity = current_quantity + quantity
                
                if new_quantity > 0:
                    self.execute_update('''
                        UPDATE inventory SET quantity = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE inventory_id = ?
                    ''', (new_quantity, inventory_id))
                else:
                    self.execute_update('DELETE FROM inventory WHERE inventory_id = ?', (inventory_id,))
            else:
                # 添加新批次库存
                self.execute_update('''
                    INSERT INTO inventory (item_id, quantity, batch_number, 
                                         production_date, expiry_date)
                    VALUES (?, ?, ?, ?, ?)
                ''', (item_id, quantity, batch_number, production_date, expiry_date))
        else:
            # 无批次管理，直接更新总库存
            result = self.execute_query('''
                SELECT inventory_id, quantity FROM inventory 
                WHERE item_id = ? AND batch_number = ''
            ''', (item_id,))
            
            if result:
                inventory_id, current_quantity = result[0]
                new_quantity = current_quantity + quantity
                
                if new_quantity > 0:
                    self.execute_update('''
                        UPDATE inventory SET quantity = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE inventory_id = ?
                    ''', (new_quantity, inventory_id))
                else:
                    self.execute_update('DELETE FROM inventory WHERE inventory_id = ?', (inventory_id,))
            else:
                self.execute_update('''
                    INSERT INTO inventory (item_id, quantity)
                    VALUES (?, ?)
                ''', (item_id, quantity))
    
    def get_current_stock(self, item_id: int) -> int:
        """获取当前库存数量"""
        result = self.execute_query('''
            SELECT SUM(quantity) FROM inventory WHERE item_id = ?
        ''', (item_id,))
        
        return result[0][0] or 0
    
    def get_inventory_status(self) -> List[Dict]:
        """获取库存状态"""
        result = self.execute_query('''
            SELECT i.item_id, i.item_code, i.item_name, c.category_name, 
                   i.unit, i.min_stock, i.max_stock,
                   COALESCE(SUM(inv.quantity), 0) as current_stock,
                   CASE 
                       WHEN COALESCE(SUM(inv.quantity), 0) <= i.min_stock THEN '库存不足'
                       WHEN COALESCE(SUM(inv.quantity), 0) >= i.max_stock THEN '库存过高'
                       ELSE '正常'
                   END as status
            FROM items i
            JOIN categories c ON i.category_id = c.category_id
            LEFT JOIN inventory inv ON i.item_id = inv.item_id
            GROUP BY i.item_id
            ORDER BY i.item_id
        ''')
        
        return [{
            'item_id': row[0],
            'item_code': row[1],
            'item_name': row[2],
            'category_name': row[3],
            'unit': row[4],
            'min_stock': row[5],
            'max_stock': row[6],
            'current_stock': row[7],
            'status': row[8]
        } for row in result]
    
    def get_stock_in_records(self) -> List[Dict]:
        """获取入库记录"""
        result = self.execute_query('''
            SELECT s.stock_in_id, i.item_name, s.quantity, i.unit, s.unit_price, 
                   s.total_amount, s.supplier, s.batch_number, s.operation_time,
                   u.full_name as operator
            FROM stock_in s
            JOIN items i ON s.item_id = i.item_id
            JOIN users u ON s.operator_id = u.user_id
            ORDER BY s.operation_time DESC
        ''')
        
        return [{
            'stock_in_id': row[0],
            'item_name': row[1],
            'quantity': row[2],
            'unit': row[3],
            'unit_price': row[4],
            'total_amount': row[5],
            'supplier': row[6],
            'batch_number': row[7],
            'operation_time': row[8],
            'operator': row[9]
        } for row in result]
    
    def get_stock_out_records(self) -> List[Dict]:
        """获取出库记录"""
        result = self.execute_query('''
            SELECT s.stock_out_id, i.item_name, s.quantity, i.unit, s.unit_price, 
                   s.total_amount, s.recipient, s.purpose, s.operation_time,
                   u.full_name as operator
            FROM stock_out s
            JOIN items i ON s.item_id = i.item_id
            JOIN users u ON s.operator_id = u.user_id
            ORDER BY s.operation_time DESC
        ''')
        
        return [{
            'stock_out_id': row[0],
            'item_name': row[1],
            'quantity': row[2],
            'unit': row[3],
            'unit_price': row[4],
            'total_amount': row[5],
            'recipient': row[6],
            'purpose': row[7],
            'operation_time': row[8],
            'operator': row[9]
        } for row in result]