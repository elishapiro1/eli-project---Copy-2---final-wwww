from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO
import os
from datetime import datetime
import json
from models import User, Admin
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')

# Custom JSON encoder to handle User objects
class UserJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (User, Admin)):
            return obj.to_dict()
        return super().default(obj)

app.json_encoder = UserJSONEncoder

# Custom session interface helper
def get_user_from_session():
    """Get User object from session data"""
    if 'user' not in session:
        return None
    
    user_data = session['user']
    return User.from_dict(user_data)

def generate_receipt_pdf(cart_items, total):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Store Information
    p.setFont("Helvetica-Bold", 24)
    p.drawString(50, height - 50, "The Sport Store")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 70, "Receipt")
    p.drawString(50, height - 90, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Store Details Box
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 130, "Store Information:")
    
    p.setFont("Helvetica", 10)
    store_details = [
        "Address: Ugav 4, Rosh HaAyin, Israel",
        "Phone: 058-550-8955",
        "Email: eli.shapiro2007@gmail.com",
        "",
        "Business Hours:",
        "Sunday - Thursday: 9:00 AM - 8:00 PM",
        "Friday: 9:00 AM - 2:00 PM",
        "Saturday: Closed",
        "",
        "Pickup Hours:",
        "Sunday - Thursday: 10:00 AM - 7:00 PM",
        "Friday: 9:00 AM - 1:00 PM",
        "Saturday: Closed"
    ]

    y_position = height - 150
    for line in store_details:
        p.drawString(70, y_position, line)
        y_position -= 15

    # Draw a line to separate store details from items
    p.line(50, y_position - 10, width - 50, y_position - 10)
    
    # Table header
    data = [['Item', 'Price', 'Quantity', 'Subtotal']]
    
    # Add items to table
    for item in cart_items:
        subtotal = item['price'] * item['quantity']
        # Truncate long item names
        name = item['name'][:30] + '...' if len(item['name']) > 30 else item['name']
        data.append([
            name,
            f"₪{item['price']}",
            str(item['quantity']),
            f"₪{subtotal}"
        ])
    
    # Add total row
    data.append(['', '', 'Total:', f"₪{total}"])
    
    # Create table with adjusted column widths
    table = Table(data, colWidths=[250, 80, 80, 80])
    table.setStyle(TableStyle([
        # Header style
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        # Data style
        ('BACKGROUND', (0, 1), (-1, -2), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),  # Left align item names
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),  # Center align other columns
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -2), 10),
        # Total row style
        ('BACKGROUND', (0, -1), (-1, -1), colors.beige),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        # Grid style
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black)
    ]))
    
    # Calculate table height and check if new page is needed
    table_height = len(data) * 20 + 30  # Approximate height per row plus padding
    if y_position - table_height < 100:  # If less than 100 points from bottom
        p.showPage()  # Start new page
        y_position = height - 50  # Reset y position
    
    # Draw table
    table.wrapOn(p, width, height)
    table.drawOn(p, 50, y_position - table_height - 50)
    
    # Footer
    footer_y = 50 if y_position - table_height > 100 else height - 100
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, footer_y, "Thank you for shopping at The Sport Store!")
    p.setFont("Helvetica", 9)
    p.drawString(50, footer_y - 15, "Please keep this receipt for your records.")
    p.drawString(50, footer_y - 30, "For returns or exchanges, please contact us within 14 days of purchase.")
    p.setFont("Helvetica-Bold", 9)
    p.drawString(50, footer_y - 45, "Products must be collected from the store within 3 business days.")
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

@app.route('/')
@app.route('/home')
def home():
    user = get_user_from_session()
    return render_template('index.html', user=user)

@app.route('/location')
def location():
    user = get_user_from_session()
    return render_template('location.html', user=user)

@app.route('/products')
def products():
    user = get_user_from_session()
    return render_template('products.html', user=user)

@app.route('/about')
def about():
    user = get_user_from_session()
    return render_template('about.html', user=user)

@app.route('/field-rental')
def field_rental():
    user = get_user_from_session()
    return render_template('field_rental.html', user=user)

@app.route('/cart')
def cart():
    user = get_user_from_session()
    cart_items = []
    total = 0
    if 'cart' in session:
        for name, details in session['cart'].items():
            cart_items.append({
                'name': name,
                'price': details['price'],
                'quantity': details['quantity']
            })
            total += details['price'] * details['quantity']
    return render_template('cart.html', cart_items=cart_items, total=total, user=user)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    if 'cart' not in session:
        session['cart'] = {}
    
    name = data['name']
    if name in session['cart']:
        session['cart'][name]['quantity'] += 1
    else:
        session['cart'][name] = {
            'price': data['price'],
            'quantity': 1
        }
    session.modified = True
    return jsonify({'success': True, 'cartCount': len(session['cart'])})

@app.route('/update-cart', methods=['POST'])
def update_cart():
    data = request.get_json()
    name = data['name']
    change = data['change']
    
    if name in session['cart']:
        session['cart'][name]['quantity'] += change
        if session['cart'][name]['quantity'] <= 0:
            del session['cart'][name]
    
    session.modified = True
    return jsonify({'success': True})

@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    name = data['name']
    
    if name in session['cart']:
        del session['cart'][name]
    
    session.modified = True
    return jsonify({'success': True})

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'cart' not in session or not session['cart']:
        return jsonify({'success': False, 'message': 'Cart is empty'})
    
    # Prepare cart items for receipt
    cart_items = []
    total = 0
    for name, details in session['cart'].items():
        cart_items.append({
            'name': name,
            'price': details['price'],
            'quantity': details['quantity']
        })
        total += details['price'] * details['quantity']
    
    # Get user data if logged in
    user = get_user_from_session()
    user_data = {
        'customer_name': user.name if user else request.get_json().get('name', 'Guest'),
        'email': user.email if user else request.get_json().get('email', 'guest@example.com'),
        'user_id': user.uid if user else None
    }
    
    # Generate PDF
    pdf_buffer = generate_receipt_pdf(cart_items, total)
    
    # Save order to Firestore
    # Initialize Firebase Admin if not already initialized
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate('serviceAccount.json')
        initialize_app(cred)
    
    # Get Firestore client
    db = firestore.client()
    
    # Create order data
    order_data = {
        'customer_name': user_data['customer_name'],
        'email': user_data['email'],
        'user_id': user_data['user_id'],
        'items': cart_items,
        'total': total,
        'status': 'pending',
        'order_date': firestore.SERVER_TIMESTAMP,
        'created_at': firestore.SERVER_TIMESTAMP
    }
    
    # Save to Firestore
    db.collection('orders').add(order_data)
    
    # Clear the cart
    session['cart'] = {}
    session.modified = True
    
    # Send PDF file
    return send_file(
        pdf_buffer,
        download_name=f'receipt_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf',
        as_attachment=True,
        mimetype='application/pdf'
    )

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/set_user_session', methods=['POST'])
def set_user_session():
    data = request.get_json()
    
    # Create the appropriate user type
    if data.get('is_admin', False):
        user = Admin(
            uid=data.get('uid', ''),
            name=data.get('name', ''),
            email=data.get('email', ''),
            created_at=None
        )
    else:
        user = User(
            uid=data.get('uid', ''),
            name=data.get('name', ''),
            email=data.get('email', ''),
            created_at=None
        )
    
    # Store user in session
    session['user'] = user.to_dict()
    return jsonify({'status': 'success'})

@app.route('/logout', methods=['POST'])
def logout():
    # Clear the user session
    session.pop('user', None)
    return jsonify({'status': 'success'})

# Admin route with access control
@app.route('/admin')
def admin():
    # Get user from session
    user = get_user_from_session()
    
    # Check if user is logged in
    if user is None:
        # User is not logged in, redirect to login page
        return redirect(url_for('auth'))
    
    # Check if user is an admin
    if not user.is_admin:
        # User is not an admin, redirect to home
        return redirect(url_for('home'))
    
    # User is an admin, show admin page
    return render_template('admin.html')

@app.route('/admin/rentals')
def admin_rentals():
    # Get user from session
    user = get_user_from_session()
    
    # Check if user is logged in
    if user is None:
        # User is not logged in, redirect to login page
        return redirect(url_for('auth'))
    
    # Check if user is an admin
    if not user.is_admin:
        # User is not an admin, redirect to home
        return redirect(url_for('home'))
    
    # User is an admin, show rentals admin page
    return render_template('admin_rentals.html')

@app.route('/admin/orders')
def admin_orders():
    # Get user from session
    user = get_user_from_session()
    
    # Check if user is logged in
    if user is None:
        # User is not logged in, redirect to login page
        return redirect(url_for('auth'))
    
    # Check if user is an admin
    if not user.is_admin:
        # User is not an admin, redirect to home
        return redirect(url_for('home'))
    
    # User is an admin, show orders admin page
    return render_template('admin_orders.html')

if __name__ == '__main__':
    app.run(debug=True) 