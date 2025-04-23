import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QFont
from models.usuario import Usuario

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supercash - Login")
        self.setFixedSize(400, 500)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #333333;
                border-radius: 5px;
                background-color: #2d2d2d;
                color: #ffffff;
                font-size: 14px;
                margin-bottom: 10px;
            }
            QPushButton {
                padding: 10px;
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
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Add title
        title = QLabel("Supercash")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title)
        
        # Add subtitle
        subtitle = QLabel("Sistema de Gestão")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Arial", 14))
        layout.addWidget(subtitle)
        
        # Add spacing
        layout.addSpacing(40)
        
        # Username field
        self.username_label = QLabel("Usuário:")
        layout.addWidget(self.username_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Digite seu usuário")
        layout.addWidget(self.username_input)
        
        # Password field
        self.password_label = QLabel("Senha:")
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Digite sua senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        # Add spacing
        layout.addSpacing(20)
        
        # Login button
        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)
        
        # Add stretching space at the bottom
        layout.addStretch()
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return
        
        # Authenticate user
        user = Usuario.authenticate(username, password)
        if user:
            if user.nivel_acesso == 'admin':
                # Open admin dashboard
                from ui.admin_dashboard import AdminDashboard
                self.admin_dashboard = AdminDashboard(user)
                self.admin_dashboard.show()
            else:
                # Open regular dashboard
                from ui.dashboard import Dashboard
                self.dashboard = Dashboard(user)
                self.dashboard.show()
            self.close()
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha inválidos.")
            self.password_input.clear()

def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()