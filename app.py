from flask import Flask, render_template, request, jsonify
import pandas as pd
import openpyxl
import os
import uuid
import json

app = Flask(__name__)

# ---------------- HOME + SECTIONS ----------------

@app.route('/')
def home():
    return render_template('account.html')

@app.route('/save-profile')
def profile_form():  # ✅ renamed to avoid duplicate function name
    return render_template('account.html')

@app.route('/send-message')
def contact():
    return render_template('contact.html')

@app.route('/orders')
def orders():
    return render_template('orders.html')

@app.route('/payments')
def payments():
    return render_template('payment.html')

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

# ---------------- PROFILE SAVE ----------------

@app.route('/save-profile', methods=['POST'])
def save_profile():
    try:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        filename = 'users.xlsx'

        if not os.path.exists(filename):
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.append(["Name", "Email", "Phone", "Address"])
            workbook.save(filename)

        workbook = openpyxl.load_workbook(filename)
        sheet = workbook.active
        sheet.append([name, email, phone, address])
        workbook.save(filename)

        return jsonify({'status': 'success'})
    except Exception as e:
        print("Profile save error:", e)
        return jsonify({'status': 'error'})

# ---------------- CONTACT FORM ----------------

@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        data = {'Name': [name], 'Email': [email], 'Subject': [subject], 'Message': [message]}
        filename = 'contact_messages.xlsx'

        if os.path.exists(filename):
            df = pd.read_excel(filename)
            df = df._append(pd.DataFrame(data), ignore_index=True)
        else:
            df = pd.DataFrame(data)

        df.to_excel(filename, index=False)
        return render_template('contact.html', success=True)
    except Exception as e:
        print("Contact save error:", e)
        return "Something went wrong while saving contact message", 500

# ---------------- ADD ORDER ----------------

@app.route('/add-order', methods=['POST'])
def add_order():
    item = request.form['item']
    price = request.form['price']
    order_id = str(uuid.uuid4())[:8]
    status = 'Placed'
    data = {'ID': [order_id], 'Item': [item], 'Price': [price], 'Status': [status]}
    filename = 'orders_data.xlsx'
    df = pd.read_excel(filename) if os.path.exists(filename) else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    df.to_excel(filename, index=False)
    return render_template('orders.html', orders=df.to_dict(orient='records'))

@app.route('/get-orders')
def get_orders():
    filename = 'orders_data.xlsx'
    if os.path.exists(filename):
        df = pd.read_excel(filename)
        orders = df.to_dict(orient='records')
    else:
        orders = []
    return jsonify(orders)

# ---------------- PAYMENTS ----------------

@app.route('/save-payment', methods=['POST'])
def save_payment():
    item = request.form['item']
    bank = request.form['bank']
    upi = request.form['upi']
    data = {'Item': [item], 'Bank': [bank], 'UPI': [upi]}
    filename = 'payment_data.xlsx'
    df = pd.read_excel(filename) if os.path.exists(filename) else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    df.to_excel(filename, index=False)
    return render_template('payment.html', success=True)

# ---------------- WISHLIST ----------------

@app.route('/add-wishlist', methods=['POST'])
def add_wishlist():
    image_url = request.form['image']
    category = request.form['category']
    data = {'Image': [image_url], 'Category': [category]}
    filename = 'wishlist_data.xlsx'
    df = pd.read_excel(filename) if os.path.exists(filename) else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    df.to_excel(filename, index=False)
    return render_template('wishlist.html', message="Item added successfully.")

@app.route('/get-wishlist')
def get_wishlist():
    filename = 'wishlist_data.xlsx'
    if os.path.exists(filename):
        df = pd.read_excel(filename)
        data = df.groupby('Category')['Image'].apply(list).to_dict()
    else:
        data = {}
    return jsonify(data)

# ---------------- LIKE IMAGE ----------------

@app.route('/like-image', methods=['POST'])
def like_image():
    image_url = request.form['image']
    filename = 'likes_data.xlsx'

    if os.path.exists(filename):
        df = pd.read_excel(filename)
    else:
        df = pd.DataFrame(columns=['Image', 'Likes'])

    if image_url in df['Image'].values:
        df.loc[df['Image'] == image_url, 'Likes'] += 1
    else:
        new_data = {'Image': [image_url], 'Likes': [1]}
        df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)

    df.to_excel(filename, index=False)
    return jsonify({'message': 'Liked successfully'})

@app.route('/add-order-direct', methods=['POST'])
def add_order_direct():
    try:
        data = request.json
        item = data['item']
        price = data['price']
        image = data.get('image', '')
        
        order_id = str(uuid.uuid4())[:8]
        status = 'Placed'
        
        # Save to Excel
        filename = 'orders_data.xlsx'
        if os.path.exists(filename):
            df = pd.read_excel(filename)
        else:
            df = pd.DataFrame(columns=['ID', 'Item', 'Price', 'Status', 'Image'])
            
        new_order = pd.DataFrame([{
            'ID': order_id,
            'Item': item,
            'Price': price,
            'Status': status,
            'Image': image
        }])
        
        df = pd.concat([df, new_order], ignore_index=True)
        df.to_excel(filename, index=False)
        
        return jsonify({
            'status': 'success',
            'order_id': order_id,
            'message': 'Order placed successfully'
        })
        
    except Exception as e:
        print("Order error:", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
