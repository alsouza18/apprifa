import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QStyleFactory
from PyQt6.QtGui import QIcon

# Configuração de paths
sys.path.append(str(Path(__file__).parent))

# Importações Core
from core.repositories.rifa_repository import JSONRifaRepository
from core.services.rifa_service import RifaService
from core.services.sorteio_service import SorteioService

# Importações UI
from ui.views.main_window import MainWindow

def configure_application(app: QApplication):
    """Configurações globais da aplicação"""
    # Estilo visual
    app.setStyle(QStyleFactory.create('Fusion'))
    
    # Ícone da aplicação
    app_icon = QIcon(str(Path(__file__).parent / 'assets' / 'app_icon.png'))
    app.setWindowIcon(app_icon)
    
    # Nome da aplicação
    app.setApplicationName("Sistema de Rifas")
    app.setApplicationDisplayName("Sistema de Rifas v1.0")

def create_services():
    """Factory para inicialização dos serviços"""
    try:
        repository = JSONRifaRepository()
        rifa_service = RifaService(repository)
        sorteio_service = SorteioService(rifa_service)
        return rifa_service, sorteio_service
    except Exception as e:
        print(f"Falha na inicialização dos serviços: {e}")
        raise

def main():
    app = QApplication(sys.argv)
    
    repository = JSONRifaRepository()
    rifa_service = RifaService(repository)
    sorteio_service = SorteioService(rifa_service)  # ← Correto!
    
    window = MainWindow(rifa_service, sorteio_service)
    window.show()
    
    sys.exit(app.exec())
    # Configuração da aplicação
    configure_application(app)
    
    try:
        # Inicialização dos serviços
        rifa_service, sorteio_service = create_services()
        
        # Janela principal
        window = MainWindow(
            rifa_service=rifa_service,
            sorteio_service=sorteio_service
        )
        window.show()
        
        # Verificação inicial
        if not rifa_service.listar_todas():
            print("Nenhuma rifa cadastrada. O sistema está pronto para novas rifas.")
        
        return app.exec()
    
    except Exception as e:
        print(f"Erro fatal: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())