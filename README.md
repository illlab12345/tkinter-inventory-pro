# Inventory Management System

A fully functional, modern Python-based inventory management system. Built with a tkinter graphical interface, it supports end-to-end material lifecycle management—from category maintenance to stock-in/out operations—providing comprehensive inventory monitoring and management capabilities. 

## 🚀 System Features

### Core Function Highlights
- **📦 End-to-End Material Management** - Complete closed-loop process from category establishment to inventory monitoring
- **🔍 Intelligent Inventory Alerts** - Automatically identifies low/overstock statuses with manual/automatic check support
- **🔎 Advanced Search Function** - Multi-condition combined search + real-time keyword search
- **📊 Real-Time Data Statistics** - Dynamically updated inventory status and operation records
- **💾 Data Persistence** - SQLite database ensures secure and reliable data storage

### Technical Advantages
- **Modern GUI Interface** - Intuitive user experience based on tkinter
- **Responsive Design** - Horizontal and vertical scrolling support for large datasets
- **Modular Architecture** - Clear code structure and maintainable design
- **Comprehensive Error Handling** - Robust system exception handling mechanism
- **Intelligent Notification System** - Smart display control for alert notifications

## 📋 Function Module Details

### 1. Inventory Status Monitoring 📈
- **Real-Time Inventory Display** - Shows current stock levels of all materials
- **Intelligent Status Identification** - Automatically marks insufficient stock (red), overstock (orange), and normal stock (green)
- **Inventory Alert System** - Intelligent warnings based on preset minimum/maximum stock limits
- **Manual Alert Check** - Supports users to actively click the "Check Inventory Alerts" button for real-time checks
- **Intelligent Notification Control** - Automatic check on system startup; forced notification display for manual checks
- **Real-Time Statistical Updates** - Alert statistics label dynamically reflects inventory status changes
- **Data Visualization** - Clear presentation of key inventory metrics in tabular format

### 2. Material Category Management 🗂️
- **Category System Construction** - Supports multi-level category structure to establish a complete material classification system
- **Category Information Maintenance** - Includes complete details such as category name, description, and parent category
- **Flexible Management** - Add, view, and adjust categories as needed
- **Relationship Management** - Maintains hierarchical relationships between categories

### 3. Material Information Management 📝
- **Comprehensive Information Fields**:
  - Basic Information: Material code, name, specification, unit
  - Supplier Information: Supplier name, contact details
  - Price Information: Purchase price, sales price
  - Inventory Settings: Minimum stock limit, maximum stock limit
- **Bulk Management** - Supports centralized management of large volumes of material information
- **Advanced Search Function**:
  - **Multi-Condition Combined Search** - Supports flexible combined queries by keyword, category, and supplier
  - **Real-Time Keyword Search** - Instant filtering during input to improve search efficiency
  - **Intelligent Search Interface** - Clear search condition selection and result display

### 4. Stock-In Management ➕
- **Stock-In Process**:
  1. Select materials to stock in
  2. Enter quantity and unit price
  3. Record supplier and batch information
  4. System automatically updates inventory
- **Batch Tracking** - Supports batch number management for quality traceability
- **Amount Calculation** - Automatically calculates total stock-in amount
- **History Records** - Complete logs of all stock-in operations

### 5. Stock-Out Management ➖
- **Stock-Out Process**:
  1. Select materials to stock out
  2. Enter quantity and unit price
  3. Record recipient and usage purpose
  4. System verifies stock availability and deducts accordingly
- **Stock Verification** - Automatically checks stock availability to prevent over-issuance
- **Usage Recording** - Detailed recipient and usage information for each stock-out
- **Security Control** - Ensures accuracy and security of stock-out operations

### 6. Record Query 🔍
- **Stock-In Record Query** - View detailed information of all stock-in operations
- **Stock-Out Record Query** - Track material issuance history
- **Operation Traceability** - Filter by time, operator, and other conditions
- **Data Export** - Facilitates subsequent data analysis and report generation

### 7. User Management 👤
- **User Roles**:
  - Administrator: Full access to all functions
- **User Information** - Maintains basic user details such as username, password, and full name
- **Permission Control** - Role-based function access control

## 🏗️ System Architecture

### File Structure
```
Inventory Management System/
├── main.py              # Main program entry, system startup and initialization
├── database.py          # Core database management module
├── gui.py               # Graphical user interface implementation
├── sample_data.py       # Sample data generator
├── check_database.py    # Database checking tool
├── inventory.db         # SQLite database file (generated after first run)
└── README.md            # System documentation
```

### Database Design
The system uses 6 core data tables to ensure data integrity and consistency:

| Table Name | Function Description | Key Fields |
|------------|----------------------|------------|
| **users** | User information management | User ID, username, password, role, creation time |
| **categories** | Material category management | Category ID, category name, description, parent category ID |
| **items** | Basic material information | Material ID, code, name, category, specification, supplier, price |
| **inventory** | Inventory management | Inventory ID, material ID, quantity, batch number, expiration date |
| **stock_in** | Stock-in records | Stock-in ID, material ID, quantity, unit price, supplier, operator |
| **stock_out** | Stock-out records | Stock-out ID, material ID, quantity, unit price, recipient, purpose |

## 🚀 Quick Start

### Environment Requirements
- **Python Version**: 3.6+
- **Required Modules**: tkinter (usually included in Python standard library)
- **Operating Systems**: Windows 7+/macOS 10.9+/Linux

### Installation Steps

#### Method 1: Direct Run (Recommended)
```bash
# Navigate to project directory
cd Inventory

# Run the system (sample data initialized automatically)
python main.py
```

#### Method 2: Step-by-Step Run
```bash
# 1. Generate sample data
python sample_data.py

# 2. Start the system
python main.py
```

### First-Time Use
1. **Direct System Startup**:
   - Run `python main.py` to enter the main interface directly
   - **No login required**—system automatically runs as administrator
   - Default administrator account: `admin` (password: `admin123`, not required for login)

2. **Sample Data Initialization** (Optional):
   - When the system runs for the first time, it automatically generates sample data if the database is empty
   - Includes 5 material categories, 15 material types, 3 system users, and initial inventory
   - Existing data will be used directly if available

## 💻 Interface Operation Guide

### Main Interface Layout
- **Left Navigation Bar** - Quick access to all functional modules
- **Top Title Bar** - System title and status display
- **Main Content Area** - Function operations and data display

### Scrolling Function Usage
All table interfaces support:
- **Vertical Scrolling** - Use mouse wheel or drag right scrollbar to browse up/down
- **Horizontal Scrolling** - Drag bottom scrollbar to view complete column information
- **Adaptive Display** - Scrollbars automatically adjust based on data volume

### Keyboard Shortcuts
- `Tab` - Switch between form fields
- `Enter` - Confirm operation or submit form
- `Esc` - Close dialog box or cancel operation

## 🔧 Advanced Features

### Batch Management
- Supports material batch number tracking
- Expiration date management
- Independent batch inventory statistics

### Inventory Alert System
- Intelligent alerts based on min_stock and max_stock settings
- Real-time status color coding
- Customizable alert thresholds

### Data Statistical Analysis
- Stock-in/out data summary
- Inventory turnover rate calculation
- Material usage frequency analysis

## 🛠️ Development and Expansion

### Code Structure Features
```python
# Clear object-oriented design
class DatabaseManager:    # Database operation encapsulation
class InventoryManagementSystem:  # Main interface controller

# Modular function separation
def show_inventory_status():   # Inventory status display
def show_category_management(): # Category management interface
```

## 🐛 Troubleshooting

### Common Problem Solutions

#### Startup Issues
1. **"No module named 'tkinter'"**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # CentOS/RHEL
   sudo yum install tkinter
   ```

2. **Interface Display Abnormalities**
   - Adjust system display scaling to 100%
   - Check system font installation

#### Runtime Issues
1. **Database Connection Failure**
   - Verify file read/write permissions
   - Ensure sufficient disk space
   - Validate database file integrity

2. **Data Operation Errors**
   - Try restarting the system
   - Check input data format
   - View system log information

### Performance Optimization Suggestions
- Regularly clean up historical record data
- Enable pagination for large datasets
- Consider database index optimization

## 📊 System Performance

### Data Processing Capabilities
- **Supported Material Quantity**: 10,000+
- **Concurrent Users**: 5-10
- **Response Time**: < 2 seconds (regular operations)

### Data Security
- Local database storage—no data uploaded to the cloud
- Encrypted user password storage
- Complete operation log records

## 🛠️ System Optimization Updates

### Latest Feature Enhancements

#### 🔍 Intelligent Search System Upgrade
- **Multi-Condition Combined Search**: Supports flexible combined queries by keyword, category, and supplier
- **Real-Time Search Experience**: Instant filtering during keyword input—no need to click search button
- **Search Interface Optimization**: Clear search condition selection and intuitive result display

#### ⚠️ Inventory Alert System Optimization
- **Manual Alert Check**: Added "Check Inventory Alerts" button to support active alert triggering by users
- **Intelligent Notification Control**:
  - Automatic check and alert notification display on system startup
  - Forced alert dialog display for manual checks to ensure critical information is not missed
  - Automatic notification status reset after operations to reflect inventory changes in real time
- **Real-Time Statistical Updates**: Alert statistics label dynamically shows the number of materials with insufficient/overstock status

#### 🎨 User Interface Improvements
- **Responsive Interaction**: Clear visual feedback for all button clicks
- **Real-Time Status Updates**: Interface elements refresh dynamically with data changes
- **Operation Process Optimization**: More intuitive operation guidance and error prompts

### Version History
- **v1.1** - Optimization Version (Current Version)
  - Added multi-condition combined search and real-time search functions
  - Optimized inventory alert system with manual check and intelligent notification support
  - Improved user interface interaction experience
  - Fixed known issues and optimized performance

- **v1.0** - Basic Function Version
  - Supports complete inventory management process
  - Modern GUI interface
  - Stable data persistence

## 📄 License and Support

### License
This project is open-source under the MIT License, allowing free use, modification, and distribution.

### Technical Support
- **Documentation Updates**: Regular maintenance of user documentation
- **Feature Suggestions**: Welcome to submit improvement suggestions

## 🤝 Contribution Guidelines

Contributions to the project are welcome:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Contact

For any questions or suggestions, please contact us via:
- 🌐 GitHub: https://github.com/illlab12345

---

## 🎯 Summary

This Inventory Management System is a fully functional, easy-to-use material management solution, specifically designed for daily inventory management needs of small and medium-sized enterprises. Combining a modern user interface with stable backend processing, it provides users with an efficient and reliable inventory management experience.

**Get Started Now**: Run `python main.py` to start using the system!
