from flask import Blueprint, render_template, request, url_for, redirect

products_bp = Blueprint('products', __name__, template_folder='templates')

@products_bp.route('/')
def index():
    products = [
        {'id': 1, 'name': 'Яблоко'},
        {'id': 2, 'name': 'Банан'},
        {'id': 3, 'name': 'Груша'}
    ]
    return render_template('products/product.html', products=products)

@products_bp.route('/item/<int:product_id>')
def show(product_id):
    product = {'id': product_id, 'name': f'Продукт #{product_id}', 'price': f'{product_id * 50} грн'} 
    return render_template('products/item.html', product=product)

@products_bp.route('/redirect-to-first')
def redirect_first():
    return redirect(url_for('products.show', product_id=1))
