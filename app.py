from flask import Flask, render_template, redirect, request, flash, session, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, login_required
from forms import PasswordChangeForm
from models import User, Message, Like, Block, DirectMessage
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Routes
@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@app.route('/users/<int:user_id>')
def show_user_profile(user_id):
    """Show user's profile."""
    user = User.query.get_or_404(user_id)
    if user.is_private and current_user not in user.followers:
        flash("This account is private.", "danger")
        return redirect("/")
    return render_template('users/profile.html', user=user)

@app.route('/profile/change_password', methods=["GET", "POST"])
@login_required
def change_password():
    """Change password."""
    form = PasswordChangeForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.password, form.old_password.data):
            current_user.password = generate_password_hash(form.new_password.data).decode('utf-8')
            db.session.commit()
            flash("Password changed successfully!", "success")
            return redirect(f"/users/{current_user.id}")
        else:
            flash("Wrong password, please try again.", "danger")
    return render_template('users/change_password.html', form=form)

@app.route('/profile/toggle_privacy', methods=["POST"])
@login_required
def toggle_privacy():
    """Toggle privacy setting."""
    current_user.is_private = not current_user.is_private
    db.session.commit()
    return redirect(f"/users/{current_user.id}")

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard."""
    return render_template('admin/dashboard.html')

@app.route('/messages/send', methods=['POST'])
@login_required
def send_message():
    """Send a direct message."""
    receiver_id = request.form.get('receiver_id')
    content = request.form.get('content')
    if not receiver_id or not content:
        return jsonify({'error': 'Invalid input.'}), 400
    message = DirectMessage(sender_id=current_user.id, receiver_id=receiver_id, content=content)
    db.session.add(message)
    db.session.commit()
    return jsonify({'success': 'Message sent!', 'message': message.content}), 200

@app.route('/messages/<int:user_id>')
@login_required
def view_messages(user_id):
    """View messages between users."""
    messages = DirectMessage.query.filter(
        ((DirectMessage.sender_id == current_user.id) & (DirectMessage.receiver_id == user_id)) |
        ((DirectMessage.sender_id == user_id) & (DirectMessage.receiver_id == current_user.id))
    ).order_by(DirectMessage.timestamp.asc()).all()
    return render_template('messages/view.html', messages=messages, receiver_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)
