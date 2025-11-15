"""
Script para crear un archivo ZIP del proyecto
"""
import os
import zipfile
from pathlib import Path

def create_project_zip():
    """Crea un archivo ZIP del proyecto excluyendo archivos innecesarios"""
    base_dir = Path(__file__).parent
    zip_path = base_dir.parent / 'steam_library_project.zip'
    
    # Archivos y directorios a excluir
    exclude_patterns = [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '.git',
        'venv',
        'env',
        '.venv',
        'db.sqlite3',
        '*.log',
        '.DS_Store',
        'media',
        'staticfiles',
        'htmlcov',
        '.coverage',
    ]
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            # Excluir directorios
            dirs[:] = [d for d in dirs if not any(
                pattern in d for pattern in exclude_patterns
            )]
            
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(base_dir.parent)
                
                # Excluir archivos
                if any(pattern in str(relative_path) for pattern in exclude_patterns):
                    continue
                
                zipf.write(file_path, relative_path)
                print(f'Agregado: {relative_path}')
    
    print(f'\n¡ZIP creado exitosamente en: {zip_path}')
    print(f'Tamaño: {zip_path.stat().st_size / 1024 / 1024:.2f} MB')

if __name__ == '__main__':
    create_project_zip()

