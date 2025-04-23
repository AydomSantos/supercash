from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QSpinBox, QDoubleSpinBox, QMessageBox, QFormLayout)
from PySide6.QtCore import Qt
from models.produto import Produto

class ProductsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_products()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Product Form
        form_group = QWidget()
        form_layout = QFormLayout(form_group)
        
        self.name_input = QLineEdit()
        form_layout.addRow('Nome:', self.name_input)
        
        self.barcode_input = QLineEdit()
        form_layout.addRow('Código de Barras:', self.barcode_input)
        
        self.cost_input = QDoubleSpinBox()
        self.cost_input.setMaximum(9999.99)
        self.cost_input.setPrefix('R$ ')
        form_layout.addRow('Preço de Custo:', self.cost_input)
        
        self.price_input = QDoubleSpinBox()
        self.price_input.setMaximum(9999.99)
        self.price_input.setPrefix('R$ ')
        form_layout.addRow('Preço de Venda:', self.price_input)
        
        self.stock_input = QSpinBox()
        self.stock_input.setMaximum(9999)
        form_layout.addRow('Estoque Atual:', self.stock_input)
        
        self.min_stock_input = QSpinBox()
        self.min_stock_input.setMaximum(999)
        form_layout.addRow('Estoque Mínimo:', self.min_stock_input)
        
        self.supplier_input = QLineEdit()
        form_layout.addRow('Fornecedor:', self.supplier_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton('Salvar')
        self.save_btn.clicked.connect(self.save_product)
        button_layout.addWidget(self.save_btn)
        
        self.clear_btn = QPushButton('Limpar')
        self.clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(self.clear_btn)
        
        form_layout.addRow(button_layout)
        
        # Search Bar
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Buscar por nome, código ou fornecedor')
        search_layout.addWidget(self.search_input)
        
        self.search_btn = QPushButton('Buscar')
        self.search_btn.clicked.connect(self.search_products)
        search_layout.addWidget(self.search_btn)
        
        layout.addLayout(search_layout)
        
        layout.addWidget(form_group)
        
        # Products Table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(8)
        self.products_table.setHorizontalHeaderLabels([
            'ID', 'Nome', 'Código', 'Custo', 'Preço',
            'Estoque', 'Est. Mín', 'Fornecedor'
        ])
        self.products_table.horizontalHeader().setStretchLastSection(True)
        self.products_table.itemClicked.connect(self.load_product_to_form)
        layout.addWidget(self.products_table)
        
        # Apply dark theme styling
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox {
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
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3d3d3d;
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
    
    def clear_form(self):
        self.name_input.clear()
        self.barcode_input.clear()
        self.cost_input.setValue(0)
        self.price_input.setValue(0)
        self.stock_input.setValue(0)
        self.min_stock_input.setValue(0)
        self.supplier_input.clear()
        self.save_btn.setText('Atualizar')
        
    def save_product(self):
        try:
            product = Produto(
                nome=self.name_input.text(),
                codigo_barras=self.barcode_input.text(),
                preco_custo=self.cost_input.value(),
                preco_venda=self.price_input.value(),
                estoque_atual=self.stock_input.value(),
                estoque_minimo=self.min_stock_input.value(),
                fornecedor=self.supplier_input.text()
            )
            
            if product.save():
                QMessageBox.information(self, 'Sucesso',
                                      'Produto salvo com sucesso!')
                self.clear_form()
                self.load_products()
            else:
                QMessageBox.critical(self, 'Erro',
                                    'Erro ao salvar produto.')
        except Exception as e:
            QMessageBox.critical(self, 'Erro',
                                f'Erro ao salvar produto: {str(e)}')
    
    def load_products(self):
        try:
            products = Produto.get_all()
            self.products_table.setRowCount(len(products))
            
            for row, product in enumerate(products):
                self.products_table.setItem(row, 0, QTableWidgetItem(str(product.id)))
                self.products_table.setItem(row, 1, QTableWidgetItem(product.nome))
                self.products_table.setItem(row, 2, QTableWidgetItem(product.codigo_barras))
                self.products_table.setItem(row, 3, QTableWidgetItem(f'R$ {product.preco_custo:.2f}'))
                self.products_table.setItem(row, 4, QTableWidgetItem(f'R$ {product.preco_venda:.2f}'))
                self.products_table.setItem(row, 5, QTableWidgetItem(str(product.estoque_atual)))
                self.products_table.setItem(row, 6, QTableWidgetItem(str(product.estoque_minimo)))
                self.products_table.setItem(row, 7, QTableWidgetItem(product.fornecedor))
                
                # Highlight low stock
                if product.estoque_atual <= product.estoque_minimo:
                    for col in range(self.products_table.columnCount()):
                        self.products_table.item(row, col).setBackground(Qt.red)
                        self.products_table.item(row, col).setForeground(Qt.white)
        
        except Exception as e:
            QMessageBox.critical(self, 'Erro',
                                f'Erro ao carregar produtos: {str(e)}')
    
    def load_product_to_form(self, item):
        row = item.row()
        product_id = int(self.products_table.item(row, 0).text())
        
        try:
            product = Produto.get_by_id(product_id)
            if product:
                self.name_input.setText(product.nome)
                self.barcode_input.setText(product.codigo_barras)
                self.cost_input.setValue(product.preco_custo)
                self.price_input.setValue(product.preco_venda)
                self.stock_input.setValue(product.estoque_atual)
                self.min_stock_input.setValue(product.estoque_minimo)
                self.supplier_input.setText(product.fornecedor)
                self.save_btn.setText('Atualizar')
        except Exception as e:
            QMessageBox.critical(self, 'Erro',
                                f'Erro ao carregar produto: {str(e)}')
    
    def search_products(self):
        search_text = self.search_input.text().strip().lower()
        
        for row in range(self.products_table.rowCount()):
            name = self.products_table.item(row, 1).text().lower()
            code = self.products_table.item(row, 2).text().lower()
            supplier = self.products_table.item(row, 7).text().lower()
            
            if search_text in name or search_text in code or search_text in supplier:
                self.products_table.setRowHidden(row, False)
            else:
                self.products_table.setRowHidden(row, True)