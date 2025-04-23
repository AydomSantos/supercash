from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QFormLayout, QDateEdit)
from PySide6.QtCore import Qt, QDate
from models.cliente import Cliente

class CustomersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_customers()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Customer Form
        form_group = QWidget()
        form_layout = QFormLayout(form_group)
        
        self.name_input = QLineEdit()
        form_layout.addRow('Nome:', self.name_input)
        
        self.cpf_cnpj_input = QLineEdit()
        form_layout.addRow('CPF/CNPJ:', self.cpf_cnpj_input)
        
        self.phone_input = QLineEdit()
        form_layout.addRow('Telefone:', self.phone_input)
        
        self.address_input = QLineEdit()
        form_layout.addRow('Endereço:', self.address_input)
        
        self.pet_name_input = QLineEdit()
        form_layout.addRow('Nome do Pet:', self.pet_name_input)
        
        self.pet_birth_input = QDateEdit()
        self.pet_birth_input.setCalendarPopup(True)
        self.pet_birth_input.setDate(QDate.currentDate())
        form_layout.addRow('Nascimento do Pet:', self.pet_birth_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton('Salvar')
        self.save_btn.clicked.connect(self.save_customer)
        button_layout.addWidget(self.save_btn)
        
        self.clear_btn = QPushButton('Limpar')
        self.clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(self.clear_btn)
        
        form_layout.addRow(button_layout)
        
        layout.addWidget(form_group)
        
        # Search Bar
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Buscar por nome ou CPF/CNPJ')
        search_layout.addWidget(self.search_input)
        
        self.search_btn = QPushButton('Buscar')
        self.search_btn.clicked.connect(self.search_customers)
        search_layout.addWidget(self.search_btn)
        
        layout.addLayout(search_layout)
        
        # Customers Table
        self.customers_table = QTableWidget()
        self.customers_table.setColumnCount(6)
        self.customers_table.setHorizontalHeaderLabels([
            'Nome', 'CPF/CNPJ', 'Telefone', 'Endereço',
            'Nome do Pet', 'Nasc. do Pet'
        ])
        self.customers_table.horizontalHeader().setStretchLastSection(True)
        self.customers_table.itemClicked.connect(self.load_customer_to_form)
        layout.addWidget(self.customers_table)
        
    def clear_form(self):
        self.name_input.clear()
        self.cpf_cnpj_input.clear()
        self.phone_input.clear()
        self.address_input.clear()
        self.pet_name_input.clear()
        self.pet_birth_input.setDate(QDate.currentDate())
        self.save_btn.setText('Atualizar')
        
    def save_customer(self):
        try:
            customer = Cliente(
                nome=self.name_input.text(),
                cpf_cnpj=self.cpf_cnpj_input.text(),
                telefone=self.phone_input.text(),
                endereco=self.address_input.text(),
                pet_nome=self.pet_name_input.text(),
                pet_nascimento=self.pet_birth_input.date().toPython()
            )
            
            if customer.save():
                QMessageBox.information(self, 'Sucesso',
                                      'Cliente salvo com sucesso!')
                self.clear_form()
                self.load_customers()
            else:
                QMessageBox.critical(self, 'Erro',
                                    'Erro ao salvar cliente.')
        except Exception as e:
            QMessageBox.critical(self, 'Erro',
                                f'Erro ao salvar cliente: {str(e)}')
    
    def load_customers(self):
        try:
            customers = Cliente.get_all()
            self.customers_table.setRowCount(len(customers))
            
            for row, customer in enumerate(customers):
                self.customers_table.setItem(row, 0, QTableWidgetItem(customer.nome))
                self.customers_table.setItem(row, 1, QTableWidgetItem(customer.cpf_cnpj))
                self.customers_table.setItem(row, 2, QTableWidgetItem(customer.telefone))
                self.customers_table.setItem(row, 3, QTableWidgetItem(customer.endereco))
                self.customers_table.setItem(row, 4, QTableWidgetItem(customer.pet_nome))
                
                if customer.pet_nascimento:
                    birth_date = customer.pet_nascimento.strftime('%d/%m/%Y')
                    self.customers_table.setItem(row, 5, QTableWidgetItem(birth_date))
                else:
                    self.customers_table.setItem(row, 5, QTableWidgetItem(''))
        
        except Exception as e:
            QMessageBox.critical(self, 'Erro',
                                f'Erro ao carregar clientes: {str(e)}')
    
    def load_customer_to_form(self, item):
        row = item.row()
        
        try:
            customer = Cliente.get_by_cpf_cnpj(
                self.customers_table.item(row, 1).text()
            )
            if customer:
                self.name_input.setText(customer.nome)
                self.cpf_cnpj_input.setText(customer.cpf_cnpj)
                self.phone_input.setText(customer.telefone)
                self.address_input.setText(customer.endereco)
                self.pet_name_input.setText(customer.pet_nome)
                
                if customer.pet_nascimento:
                    self.pet_birth_input.setDate(
                        QDate.fromString(
                            customer.pet_nascimento.strftime('%Y-%m-%d'),
                            'yyyy-MM-dd'
                        )
                    )
                
                self.save_btn.setText('Atualizar')
        except Exception as e:
            QMessageBox.critical(self, 'Erro',
                                f'Erro ao carregar cliente: {str(e)}')
    
    def search_customers(self):
        search_text = self.search_input.text().strip().lower()
        
        for row in range(self.customers_table.rowCount()):
            name = self.customers_table.item(row, 0).text().lower()
            cpf_cnpj = self.customers_table.item(row, 1).text().lower()
            
            if search_text in name or search_text in cpf_cnpj:
                self.customers_table.setRowHidden(row, False)
            else:
                self.customers_table.setRowHidden(row, True)