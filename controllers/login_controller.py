from PySide6.QtWidgets import QMessageBox
from ui.login import LoginWindow
from models.usuario import Usuario
from ui.dashboard import DashboardWindow
from ui.admin_dashboard import AdminDashboardWindow

class LoginController:
    def __init__(self):
        self.login_window = LoginWindow()
        self.setup_connections()
    
    def setup_connections(self):
        self.login_window.login_button.clicked.connect(self.handle_login)
    
    def show_login(self):
        self.login_window.show()
    
    def handle_login(self):
        username = self.login_window.username_input.text().strip()
        password = self.login_window.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self.login_window, 'Error', 'Please enter both username and password')
            return
        
        user = Usuario.authenticate(username, password)
        
        if user:
            QMessageBox.information(self.login_window, 'Success', f'Welcome {user.nome}!')
            self.login_window.hide()
            
            # Open appropriate dashboard based on user's access level
            if user.nivel_acesso == 'admin':
                self.dashboard = AdminDashboardWindow(user)
            else:
                self.dashboard = DashboardWindow(user)
                
            self.dashboard.show()
        else:
            QMessageBox.warning(self.login_window, 'Error', 'Invalid username or password')
            self.login_window.password_input.clear()