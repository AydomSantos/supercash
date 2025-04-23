import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                                QDialog, QLineEdit, QComboBox, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from models.usuario import Usuario

class UserDialog(QDialog):
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle("Adicionar Usuário" if not user else "Editar Usuário")
        self.setFixedSize(400, 300)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Username field
        self.username_label = QLabel("Usuário:")
        self.username_input = QLineEdit()
        if self.user:
            self.username_input.setText(self.user.username)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        
        # Password field
        self.password_label = QLabel("Senha:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        
        # Name field
        self.name_label = QLabel("Nome:")
        self.name_input = QLineEdit()
        if self.user:
            self.name_input.setText(self.user.nome)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        
        # Access level field
        self.access_label = QLabel("Nível de Acesso:")
        self.access_combo = QComboBox()
        self.access_combo.addItems(['admin', 'user'])
        if self.user:
            self.access_combo.setCurrentText(self.user.nivel_acesso)
        layout.addWidget(self.access_label)
        layout.addWidget(self.access_combo)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.save_user)
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
    
    def save_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        name = self.name_input.text()
        access_level = self.access_combo.currentText()
        
        if not all([username, name]):
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos obrigatórios.")
            return
        
        if not self.user:
            if not password:
                QMessageBox.warning(self, "Erro", "Por favor, defina uma senha.")
                return
            self.user = Usuario()
        
        self.user.username = username
        if password:
            self.user.password_hash = self.user.hash_password(password)
        self.user.nome = name
        self.user.nivel_acesso = access_level
        
        if self.user.save():
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", "Erro ao salvar usuário.")

class AdminDashboardWindow(QMainWindow):
    def __init__(self, user=None):
        super().__init__()
        self.user = user
        self.setWindowTitle("Supercash - Painel Administrativo")
        self.setMinimumSize(800, 600)
        self.setup_ui()
        self.load_users()
    
    def setup_ui(self):
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Gerenciamento de Usuários")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Add user button
        self.add_button = QPushButton("Adicionar Usuário")
        self.add_button.clicked.connect(self.add_user)
        header_layout.addWidget(self.add_button)
        layout.addLayout(header_layout)
        
        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(5)
        self.users_table.setHorizontalHeaderLabels(["ID", "Usuário", "Nome", "Nível de Acesso", "Ações"])
        self.users_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.users_table)
    
    def load_users(self):
        users = Usuario.get_all()
        self.users_table.setRowCount(len(users))
        
        for i, user in enumerate(users):
            self.users_table.setItem(i, 0, QTableWidgetItem(str(user.id)))
            self.users_table.setItem(i, 1, QTableWidgetItem(user.username))
            self.users_table.setItem(i, 2, QTableWidgetItem(user.nome))
            self.users_table.setItem(i, 3, QTableWidgetItem(user.nivel_acesso))
            
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_button = QPushButton("Editar")
            edit_button.clicked.connect(lambda checked, u=user: self.edit_user(u))
            delete_button = QPushButton("Excluir")
            delete_button.clicked.connect(lambda checked, u=user: self.delete_user(u))
            
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            
            self.users_table.setCellWidget(i, 4, actions_widget)
    
    def add_user(self):
        dialog = UserDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users()
    
    def edit_user(self, user):
        dialog = UserDialog(self, user)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users()
    
    def delete_user(self, user):
        if user.id == self.user.id:
            QMessageBox.warning(self, "Erro", "Você não pode excluir seu próprio usuário.")
            return
        
        reply = QMessageBox.question(self, "Confirmar", "Tem certeza que deseja excluir este usuário?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if user.delete():
                self.load_users()
            else:
                QMessageBox.warning(self, "Erro", "Erro ao excluir usuário.")