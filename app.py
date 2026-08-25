import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Category, Application
from dotenv import load_dotenv
from services.file_service import init_category_folder, save_document, get_category_documents
from services.email_service import send_application_email, check_for_replies

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'cle_secrete_pour_le_developpement')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def dashboard():
    applications = Application.query.order_by(Application.date_sent.desc()).all()
    return render_template('dashboard.html', applications=applications)

@app.route('/refresh_replies', methods=['POST'])
def refresh_replies():
    try:
        count = check_for_replies(app)
        flash(f"{count} nouvelle(s) réponse(s) détectée(s).", "success")
    except Exception as e:
        flash(f"Erreur lors de la vérification : {str(e)}", "warning")
    return redirect(url_for('dashboard'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form.get('name')
        email_body = request.form.get('email_body')
        
        if name:
            folder_path = init_category_folder(name)
            new_cat = Category(name=name, folder_path=folder_path, email_body=email_body)
            db.session.add(new_cat)
            db.session.commit()
            
            cv_file = request.files.get('cv_file')
            lm_file = request.files.get('lm_file')
            
            if cv_file and cv_file.filename:
                save_document(cv_file, folder_path, "CV.pdf")
            if lm_file and lm_file.filename:
                save_document(lm_file, folder_path, "Lettre_Motivation.pdf")
                
            flash(f"Catégorie '{name}' créée avec succès.", "success")
            
        return redirect(url_for('admin'))
        
    categories = Category.query.all()
    for cat in categories:
        cat.files = get_category_documents(cat.folder_path)
        
    return render_template('admin.html', categories=categories)

@app.route('/edit_category/<int:category_id>', methods=['POST'])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    new_name = request.form.get('name')
    new_email_body = request.form.get('email_body')
    
    if new_name:
        category.name = new_name
    if new_email_body:
        category.email_body = new_email_body
        
    cv_file = request.files.get('cv_file')
    lm_file = request.files.get('lm_file')
    
    if cv_file and cv_file.filename:
        save_document(cv_file, category.folder_path, "CV.pdf")
    if lm_file and lm_file.filename:
        save_document(lm_file, category.folder_path, "Lettre_Motivation.pdf")
        
    db.session.commit()
    flash(f"Catégorie '{category.name}' mise à jour avec succès.", "success")
    return redirect(url_for('admin'))

@app.route('/apply', methods=['GET', 'POST'])
def new_application():
    categories = Category.query.all()
    
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        custom_body = request.form.get('custom_email_body')
        subject = request.form.get('email_subject')
        
        companies = request.form.getlist('company_name[]')
        contacts = request.form.getlist('contact_name[]')
        emails = request.form.getlist('contact_email[]')
        
        category = Category.query.get(category_id)
        
        if not category:
            flash("Catégorie introuvable.", "error")
            return redirect(url_for('new_application'))
            
        file_names = get_category_documents(category.folder_path)
        attachment_paths = [os.path.join(os.path.dirname(os.path.abspath(__file__)), category.folder_path, fn) for fn in file_names]
        
        success_count = 0
        for i in range(len(companies)):
            comp = companies[i]
            cont = contacts[i] if contacts[i] else ""
            mail = emails[i]
            
            if comp and mail:
                body_formatted = custom_body.replace('{company_name}', comp).replace('{contact_name}', cont)
                
                try:
                    send_application_email(mail, subject, body_formatted, attachment_paths)
                    
                    app_entry = Application(
                        company_name=comp,
                        contact_email=mail,
                        contact_name=cont,
                        category_id=category.id,
                        email_subject=subject
                    )
                    db.session.add(app_entry)
                    success_count += 1
                except Exception as e:
                    flash(f"Erreur lors de l'envoi à {comp} ({mail}) : {str(e)}", "warning")
        
        if success_count > 0:
            db.session.commit()
            flash(f"{success_count} candidature(s) envoyée(s) avec succès.", "success")
            
        return redirect(url_for('dashboard'))
        
    return render_template('new_application.html', categories=categories)

if __name__ == '__main__':
    app.run(debug=True)
