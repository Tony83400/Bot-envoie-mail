import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATEGORIES_DIR = os.path.join(BASE_DIR, 'data', 'categories')

def init_category_folder(category_name):
    """Crée le dossier pour une nouvelle catégorie et retourne le chemin relatif."""
    # Nettoyer le nom pour le dossier (pas de caractères spéciaux)
    safe_name = "".join([c for c in category_name if c.isalpha() or c.isdigit() or c==' ']).rstrip().replace(" ", "_")
    
    path = os.path.join(CATEGORIES_DIR, safe_name)
    if not os.path.exists(path):
        os.makedirs(path)
    
    return os.path.join('data', 'categories', safe_name)

def save_document(file_obj, category_folder_path, filename):
    """Sauvegarde un document PDF (CV ou LM) dans le dossier de la catégorie."""
    full_path = os.path.join(BASE_DIR, category_folder_path, filename)
    file_obj.save(full_path)
    return full_path

def get_category_documents(category_folder_path):
    """Retourne la liste des documents présents dans le dossier de la catégorie."""
    full_path = os.path.join(BASE_DIR, category_folder_path)
    if not os.path.exists(full_path):
        return []
    return os.listdir(full_path)
