from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QComboBox, QSpinBox, QDoubleSpinBox, QMessageBox)
from PySide6.QtCore import Qt
from models.produto import Produto
from models.cliente import Cliente
from models.venda import Venda
from datetime import datetime

class SalesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.current_sale = None
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header section
        header_layout = QHBoxLayout()
        self.client_search = QLineEdit()
        self.client_search.setPlaceholderText('Buscar cliente (CPF/CNPJ)')
        self.client_search.returnPressed.connect(self.search_client)
        header_layout.addWidget(self.client_search)
        
        self.product_search = QLineEdit()
        self.product_search.setPlaceholderText('Buscar produto (código/nome)')
        self.product_search.returnPressed.connect(self.search_product)
        header_layout.addWidget(self.product_search)
        
        layout.addLayout(header_layout)
        
        # Cart section
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(6)  # Added one more column for manual price
        self.cart_table.setHorizontalHeaderLabels(['Produto', 'Quantidade', 'Preço Unit.', 'Preço Manual', 'Subtotal', 'Ações'])
        self.cart_table.horizontalHeader().setStretchLastSection(True)
        self.cart_table.setStyleSheet("""
            QTableWidget::item {
                padding: 4px;
                border-bottom: 1px solid #3d3d3d;
            }
            QSpinBox, QDoubleSpinBox {
                min-width: 100px;
                padding: 4px;
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
            }
            QPushButton {
                min-width: 80px;
                padding: 4px 8px;
                background-color: #d32f2f;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #ef5350;
            }
        """)
        layout.addWidget(self.cart_table)
        
        # Totals section
        totals_layout = QHBoxLayout()
        
        self.subtotal_label = QLabel('Subtotal: R$ 0,00')
        totals_layout.addWidget(self.subtotal_label)
        
        self.discount_spin = QDoubleSpinBox()
        self.discount_spin.setPrefix('Desconto: R$ ')
        self.discount_spin.setMaximum(9999.99)
        self.discount_spin.valueChanged.connect(self.update_total)
        totals_layout.addWidget(self.discount_spin)
        
        self.total_label = QLabel('Total: R$ 0,00')
        totals_layout.addWidget(self.total_label)
        
        layout.addLayout(totals_layout)
        
        # Payment section
        payment_layout = QHBoxLayout()
        
        self.payment_method = QComboBox()
        self.payment_method.addItems(['Dinheiro', 'Cartão de Crédito', 'Cartão de Débito', 'PIX'])
        payment_layout.addWidget(self.payment_method)
        
        self.finish_sale_btn = QPushButton('Finalizar Venda')
        self.finish_sale_btn.clicked.connect(self.finish_sale)
        payment_layout.addWidget(self.finish_sale_btn)
        
        layout.addLayout(payment_layout)
        
        # Initialize new sale
        self.new_sale()
        # Apply dark theme styling
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #333333;
                border-radius: 5px;
                background-color: #2d2d2d;
                color: #ffffff;
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
            QComboBox {
                padding: 8px;
                border: 2px solid #333333;
                border-radius: 5px;
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QSpinBox, QDoubleSpinBox {
                padding: 8px;
                border: 2px solid #333333;
                border-radius: 5px;
                background-color: #2d2d2d;
                color: #ffffff;
            }
        """)
    
    def new_sale(self):
        self.current_sale = Venda()
        self.cart_table.setRowCount(0)
        self.discount_spin.setValue(0)
        self.update_total()
    
    def search_client(self):
        cpf_cnpj = self.client_search.text().strip()
        if cpf_cnpj:
            client = Cliente.get_by_cpf_cnpj(cpf_cnpj)
            if client:
                self.current_sale.cliente_id = client.id
                QMessageBox.information(self, 'Cliente Encontrado', f'Cliente: {client.nome}')
            else:
                QMessageBox.warning(self, 'Cliente não Encontrado', 'Cliente não cadastrado no sistema.')
    
    def search_product(self):
        code = self.product_search.text().strip()
        if code:
            product = Produto.get_by_barcode(code)
            if product:
                self.add_product_to_cart(product)
                self.product_search.clear()
            else:
                QMessageBox.warning(self, 'Produto não Encontrado', 'Produto não cadastrado no sistema.')
    
    def add_product_to_cart(self, product):
        row = self.cart_table.rowCount()
        self.cart_table.insertRow(row)
        
        # Store product ID for later use
        self.cart_table.setItem(row, 0, QTableWidgetItem(product.nome))
        self.cart_table.item(row, 0).setData(Qt.UserRole, product.id)
        
        qty_spin = QSpinBox()
        qty_spin.setMinimum(1)
        qty_spin.setMaximum(min(9999, product.estoque_atual))  # Limit by available stock
        qty_spin.valueChanged.connect(lambda: self.update_item_total(row))
        self.cart_table.setCellWidget(row, 1, qty_spin)
        
        price_item = QTableWidgetItem(f'R$ {product.preco_venda:.2f}')
        self.cart_table.setItem(row, 2, price_item)
        
        manual_price = QDoubleSpinBox()
        manual_price.setPrefix('R$ ')
        manual_price.setMaximum(9999.99)
        manual_price.setValue(product.preco_venda)
        manual_price.valueChanged.connect(lambda: self.update_item_total(row))
        self.cart_table.setCellWidget(row, 3, manual_price)
        
        subtotal_item = QTableWidgetItem('R$ 0,00')
        self.cart_table.setItem(row, 4, subtotal_item)
        
        remove_btn = QPushButton('Remover')
        remove_btn.clicked.connect(lambda: self.remove_item(row))
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #ef5350;
            }
            QPushButton:pressed {
                background-color: #c62828;
            }
        """)
        self.cart_table.setCellWidget(row, 5, remove_btn)
        
        # Update sale model
        self.current_sale.add_item(product.id, 1, product.preco_venda)
        self.update_item_total(row)
    
    def update_item_total(self, row):
        qty = self.cart_table.cellWidget(row, 1).value()
        manual_price = self.cart_table.cellWidget(row, 3).value()
        subtotal = qty * manual_price
        
        self.cart_table.item(row, 4).setText(f'R$ {subtotal:.2f}')
        self.update_total()
    
    def remove_item(self, row):
        self.cart_table.removeRow(row)
        self.update_total()
    
    def update_total(self):
        subtotal = sum(float(self.cart_table.item(row, 4).text().replace('R$ ', ''))
                      for row in range(self.cart_table.rowCount()))
        
        discount = self.discount_spin.value()
        total = subtotal - discount
        
        self.subtotal_label.setText(f'Subtotal: R$ {subtotal:.2f}')
        self.total_label.setText(f'Total: R$ {total:.2f}')
    
    def finish_sale(self):
        if self.cart_table.rowCount() == 0:
            QMessageBox.warning(self, 'Venda Vazia',
                               'Adicione produtos antes de finalizar a venda.')
            return
        
        self.current_sale.forma_pagamento = self.payment_method.currentText()
        self.current_sale.desconto = self.discount_spin.value()
        
        if self.current_sale.save():
            QMessageBox.information(self, 'Sucesso',
                                   'Venda finalizada com sucesso!')
            self.new_sale()
        else:
            QMessageBox.critical(self, 'Erro',
                                'Erro ao finalizar a venda. Tente novamente.')