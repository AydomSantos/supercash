from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QFrame, QPushButton, QStackedWidget, QTableWidget, QTableWidgetItem,
                               QHeaderView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class DashboardWindow(QMainWindow):
    def __init__(self, user=None):
        super().__init__()
        self.user = user
        self.setWindowTitle('Supercash - Dashboard')
        self.setMinimumSize(1200, 800)
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        
        # Create and setup the menu frame
        self.setup_menu()
        
        # Create and setup the content area
        self.setup_content_area()
        
        # Set the initial page
        self.show_overview()
    
    def setup_menu(self):
        # Create menu frame
        menu_frame = QFrame()
        menu_frame.setObjectName('menuFrame')
        menu_frame.setMinimumWidth(200)
        menu_frame.setMaximumWidth(200)
        menu_layout = QVBoxLayout(menu_frame)
        
        # Add logo
        logo_label = QLabel('SUPERCASH')
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet('font-size: 20px; font-weight: bold; color: #0078d4; padding: 20px 0;')
        menu_layout.addWidget(logo_label)
        
        # Add welcome message
        welcome_label = QLabel(f'Bem-vindo,\n{self.user.nome if self.user else "Usuário"}!')
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet('font-size: 14px; padding: 10px; color: #ffffff;')
        welcome_label.setWordWrap(True)
        menu_layout.addWidget(welcome_label)
        
        # Add menu buttons
        self.menu_buttons = {}
        for text in ['Visão Geral', 'Vendas', 'Produtos', 'Clientes', 'Relatórios']:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-size: 14px;
                    text-align: left;
                    margin: 2px 0;
                }
                QPushButton:hover {
                    background-color: #3d3d3d;
                }
                QPushButton:pressed {
                    background-color: #0078d4;
                }
            """)
            menu_layout.addWidget(btn)
            self.menu_buttons[text] = btn
        
        # Connect button signals
        self.menu_buttons['Visão Geral'].clicked.connect(self.show_overview)
        self.menu_buttons['Vendas'].clicked.connect(self.show_sales)
        self.menu_buttons['Produtos'].clicked.connect(self.show_products)
        self.menu_buttons['Clientes'].clicked.connect(self.show_clients)
        self.menu_buttons['Relatórios'].clicked.connect(self.show_reports)
        
        # Add stretch to push buttons to the top
        menu_layout.addStretch()
        
        # Add to main layout
        self.main_layout.addWidget(menu_frame)
    
    def setup_content_area(self):
        # Create stacked widget for different pages
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet('background-color: #1e1e1e;')
        
        # Create pages
        self.overview_page = self.create_overview_page()
        self.sales_page = self.create_page('Vendas')
        self.products_page = self.create_page('Produtos')
        self.clients_page = self.create_page('Clientes')
        self.reports_page = self.create_page('Relatórios')
        
        # Add pages to stack
        self.content_stack.addWidget(self.overview_page)
        self.content_stack.addWidget(self.sales_page)
        self.content_stack.addWidget(self.products_page)
        self.content_stack.addWidget(self.clients_page)
        self.content_stack.addWidget(self.reports_page)
        
        # Add to main layout
        self.main_layout.addWidget(self.content_stack)
    
    def create_overview_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Add title
        title = QLabel('Visão Geral')
        title.setStyleSheet('font-size: 24px; color: #ffffff; margin-bottom: 20px;')
        layout.addWidget(title)
        
        # Create grid for statistics
        stats_layout = QHBoxLayout()
        
        # Add statistic cards
        stats = [
            {'title': 'Vendas Hoje', 'value': 'R$ 0,00'},
            {'title': 'Produtos em Estoque', 'value': '0'},
            {'title': 'Clientes Ativos', 'value': '0'},
            {'title': 'Vendas no Mês', 'value': 'R$ 0,00'}
        ]
        
        self.stat_values = {}
        
        for stat in stats:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #252526;
                    border-radius: 8px;
                    padding: 20px;
                }
            """)
            card_layout = QVBoxLayout(card)
            
            # Add stat title
            title = QLabel(stat['title'])
            title.setStyleSheet('color: #888888; font-size: 14px;')
            card_layout.addWidget(title)
            
            # Add stat value as a clickable label
            value = QLabel(stat['value'])
            value.setStyleSheet('color: #ffffff; font-size: 24px; font-weight: bold; cursor: pointer;')
            value.mousePressEvent = lambda _, t=stat['title'], v=value: self.edit_stat_value(t, v)
            card_layout.addWidget(value)
            
            self.stat_values[stat['title']] = value
            stats_layout.addWidget(card)
        
        layout.addLayout(stats_layout)
        
        # Add recent sales table
        sales_title = QLabel('Vendas Recentes')
        sales_title.setStyleSheet('font-size: 18px; color: #ffffff; margin: 20px 0;')
        layout.addWidget(sales_title)
        
        self.sales_table = QTableWidget()
        self.sales_table.setStyleSheet("""
            QTableWidget {
                background-color: #252526;
                border: none;
                border-radius: 8px;
                gridline-color: #3d3d3d;
            }
            QHeaderView::section {
                background-color: #252526;
                color: #888888;
                border: none;
                padding: 8px;
            }
        """)
        self.sales_table.setColumnCount(4)
        self.sales_table.setHorizontalHeaderLabels(['Data', 'Cliente', 'Valor', 'Status'])
        self.sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Add button to add new sale
        add_sale_btn = QPushButton('Adicionar Venda')
        add_sale_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0086ef;
            }
            QPushButton:pressed {
                background-color: #006abc;
            }
        """)
        add_sale_btn.clicked.connect(self.add_new_sale)
        layout.addWidget(add_sale_btn)
        layout.addWidget(self.sales_table)
        
        return page
    
    def edit_stat_value(self, title, label):
        from PySide6.QtWidgets import QInputDialog
        new_value, ok = QInputDialog.getText(
            self, f'Editar {title}',
            'Digite o novo valor:',
            text=label.text()
        )
        if ok and new_value:
            if title in ['Vendas Hoje', 'Vendas no Mês']:
                if not new_value.startswith('R$ '):
                    new_value = 'R$ ' + new_value
            label.setText(new_value)
    
    def add_new_sale(self):
        from PySide6.QtWidgets import QInputDialog
        
        # Get sale details
        date, ok1 = QInputDialog.getText(self, 'Nova Venda', 'Data (AAAA-MM-DD):')
        if not ok1: return
        
        client, ok2 = QInputDialog.getText(self, 'Nova Venda', 'Nome do Cliente:')
        if not ok2: return
        
        value, ok3 = QInputDialog.getText(self, 'Nova Venda', 'Valor (R$):')
        if not ok3: return
        
        status, ok4 = QInputDialog.getItem(
            self, 'Nova Venda', 'Status:',
            ['Concluída', 'Pendente'], 0, False
        )
        if not ok4: return
        
        # Add new row to table
        row = self.sales_table.rowCount()
        self.sales_table.insertRow(row)
        
        # Add sale data
        items = [date, client, f'R$ {value}', status]
        for col, value in enumerate(items):
            item = QTableWidgetItem(value)
            item.setForeground(Qt.white)
            self.sales_table.setItem(row, col, item)
    
    def create_page(self, title):
        if title == 'Vendas':
            from ui.sales import SalesWindow
            return SalesWindow()
        elif title == 'Produtos':
            from ui.products import ProductsWindow
            return ProductsWindow()
        elif title == 'Clientes':
            from ui.customers import CustomersWindow
            return CustomersWindow()
        else:
            # Default page for Reports (to be implemented)
            page = QWidget()
            layout = QVBoxLayout(page)
            title_label = QLabel(title)
            title_label.setStyleSheet('font-size: 24px; color: #ffffff; margin-bottom: 20px;')
            layout.addWidget(title_label)
            content = QLabel(f'Conteúdo da página {title} em desenvolvimento')
            content.setStyleSheet('color: #888888; font-size: 16px;')
            content.setAlignment(Qt.AlignCenter)
            layout.addWidget(content)
            return page
    
    def show_overview(self):
        self.content_stack.setCurrentWidget(self.overview_page)
    
    def show_sales(self):
        self.content_stack.setCurrentWidget(self.sales_page)
    
    def show_products(self):
        self.content_stack.setCurrentWidget(self.products_page)
    
    def show_clients(self):
        self.content_stack.setCurrentWidget(self.clients_page)
    
    def show_reports(self):
        self.content_stack.setCurrentWidget(self.reports_page)