from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QComboBox, QDateEdit, QMessageBox)
from PySide6.QtCore import Qt, QDate
from models.venda import Venda
from models.produto import Produto
from models.cliente import Cliente
from datetime import datetime, timedelta

class ReportsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Report Type Selection with improved styling
        type_layout = QHBoxLayout()
        
        self.report_type = QComboBox()
        self.report_type.addItems([
            'Vendas por Período',
            'Produtos Mais Vendidos',
            'Clientes Mais Ativos',
            'Produtos com Estoque Baixo',
            'Análise de Lucro',
            'Tendências de Vendas'
        ])
        self.report_type.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #333333;
                border-radius: 5px;
                background-color: #2d2d2d;
                color: #ffffff;
                min-width: 200px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        self.report_type.currentIndexChanged.connect(self.change_report)
        type_layout.addWidget(QLabel('Tipo de Relatório:'))
        type_layout.addWidget(self.report_type)
        
        layout.addLayout(type_layout)
        
        # Date Range Selection with better visual feedback
        date_layout = QHBoxLayout()
        
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 2px solid #333333;
                border-radius: 5px;
                background-color: #2d2d2d;
                color: #ffffff;
            }
        """)
        date_layout.addWidget(QLabel('Data Inicial:'))
        date_layout.addWidget(self.start_date)
        
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 2px solid #333333;
                border-radius: 5px;
                background-color: #2d2d2d;
                color: #ffffff;
            }
        """)
        date_layout.addWidget(QLabel('Data Final:'))
        date_layout.addWidget(self.end_date)
        
        layout.addLayout(date_layout)
        
        # Generate Button with improved styling
        self.generate_btn = QPushButton('Gerar Relatório')
        self.generate_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0086ef;
            }
            QPushButton:pressed {
                background-color: #006abc;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_report)
        layout.addWidget(self.generate_btn)
        
        # Report Table with enhanced styling
        self.report_table = QTableWidget()
        # Apply dark theme styling
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QComboBox, QDateEdit {
                padding: 8px;
                border: 2px solid #333333;
                border-radius: 5px;
                background-color: #2d2d2d;
                color: #ffffff;
                min-width: 200px;
            }
            QComboBox::drop-down, QDateEdit::drop-down {
                border: none;
            }
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
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3d3d3d;
            }
            QTableWidget::item:selected {
                background-color: #0078d4;
                color: #ffffff;
            }
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
        self.report_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.report_table)
        
        # Set initial report type
        self.change_report(0)
    
    def change_report(self, index):
        self.start_date.setEnabled(index != 3)  # Disable dates for low stock report
        self.end_date.setEnabled(index != 3)
        
        # Configure table columns based on report type
        if index == 0:  # Sales by Period
            self.report_table.setColumnCount(5)
            self.report_table.setHorizontalHeaderLabels([
                'Data', 'Cliente', 'Produtos', 'Valor Total', 'Forma Pagamento'
            ])
        elif index == 1:  # Best Selling Products
            self.report_table.setColumnCount(4)
            self.report_table.setHorizontalHeaderLabels([
                'Produto', 'Quantidade Vendida', 'Valor Total', 'Lucro'
            ])
        elif index == 2:  # Most Active Customers
            self.report_table.setColumnCount(4)
            self.report_table.setHorizontalHeaderLabels([
                'Cliente', 'Total de Compras', 'Valor Total', 'Última Compra'
            ])
        else:  # Low Stock Products
            self.report_table.setColumnCount(4)
            self.report_table.setHorizontalHeaderLabels([
                'Produto', 'Estoque Atual', 'Estoque Mínimo', 'Fornecedor'
            ])
    
    def generate_report(self):
        try:
            report_type = self.report_type.currentIndex()
            
            if report_type == 0:
                self.generate_sales_report()
            elif report_type == 1:
                self.generate_best_sellers_report()
            elif report_type == 2:
                self.generate_customer_report()
            else:
                self.generate_low_stock_report()
                
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao gerar relatório: {str(e)}')
    
    def generate_sales_report(self):
        start = self.start_date.date().toPython()
        end = self.end_date.date().toPython()
        
        sales = Venda.get_by_date_range(start, end)
        self.report_table.setRowCount(len(sales))
        
        for row, sale in enumerate(sales):
            self.report_table.setItem(row, 0, 
                QTableWidgetItem(sale.data_venda.strftime('%d/%m/%Y')))
            
            client = Cliente.get_by_id(sale.cliente_id)
            self.report_table.setItem(row, 1,
                QTableWidgetItem(client.nome if client else 'N/A'))
            
            items = sale.get_items()
            products = [f'{item.quantidade}x {Produto.get_by_id(item.produto_id).nome}'
                       for item in items]
            self.report_table.setItem(row, 2,
                QTableWidgetItem('\n'.join(products)))
            
            self.report_table.setItem(row, 3,
                QTableWidgetItem(f'R$ {sale.valor_total:.2f}'))
            
            self.report_table.setItem(row, 4,
                QTableWidgetItem(sale.forma_pagamento))
    
    def generate_best_sellers_report(self):
        start = self.start_date.date().toPython()
        end = self.end_date.date().toPython()
        
        products = Produto.get_best_sellers(start, end)
        self.report_table.setRowCount(len(products))
        
        for row, data in enumerate(products):
            self.report_table.setItem(row, 0,
                QTableWidgetItem(data['produto'].nome))
            self.report_table.setItem(row, 1,
                QTableWidgetItem(str(data['quantidade'])))
            self.report_table.setItem(row, 2,
                QTableWidgetItem(f'R$ {data["valor_total"]:.2f}'))
            
            lucro = data['valor_total'] - (data['produto'].preco_custo * data['quantidade'])
            self.report_table.setItem(row, 3,
                QTableWidgetItem(f'R$ {lucro:.2f}'))
    
    def generate_customer_report(self):
        start = self.start_date.date().toPython()
        end = self.end_date.date().toPython()
        
        customers = Cliente.get_most_active(start, end)
        self.report_table.setRowCount(len(customers))
        
        for row, data in enumerate(customers):
            self.report_table.setItem(row, 0,
                QTableWidgetItem(data['cliente'].nome))
            self.report_table.setItem(row, 1,
                QTableWidgetItem(str(data['total_compras'])))
            self.report_table.setItem(row, 2,
                QTableWidgetItem(f'R$ {data["valor_total"]:.2f}'))
            self.report_table.setItem(row, 3,
                QTableWidgetItem(data['ultima_compra'].strftime('%d/%m/%Y')))
    
    def generate_low_stock_report(self):
        products = Produto.get_low_stock()
        self.report_table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            self.report_table.setItem(row, 0,
                QTableWidgetItem(product.nome))
            self.report_table.setItem(row, 1,
                QTableWidgetItem(str(product.estoque_atual)))
            self.report_table.setItem(row, 2,
                QTableWidgetItem(str(product.estoque_minimo)))
            self.report_table.setItem(row, 3,
                QTableWidgetItem(product.fornecedor))
            
            # Highlight critical stock levels
            if product.estoque_atual == 0:
                color = Qt.red
            elif product.estoque_atual <= product.estoque_minimo:
                color = Qt.yellow
            else:
                continue
                
            for col in range(self.report_table.columnCount()):
                self.report_table.item(row, col).setBackground(color)