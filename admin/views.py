# flask関連のパッケージを取得
from flask import render_template, request, url_for, session, redirect, flash

# 「__init__.py」で宣言した変数appを取得
from admin import app

# Itemモデルを取得
from lib.models import Item, Category, Test_item, Test_categories

# SQLAlchemyを取得
from lib.db import db

# デコレーターに使用
from functools import wraps


# 商品一覧を表示
@app.route('/items')
def index():
  items = Item.query.order_by(Item.id.desc()).all()
  return render_template('items/index.html', items=items)

# 商品詳細を表示
@app.route('/items/<int:id>')
def show(id):
  item = Item.query.get(id)
  return render_template('items/show.html', item=item)

# 商品作成画面を表示
@app.route('/items/new')
def new():
  categories = Category.query.all()
  return render_template('items/new.html', categories=categories)

# 商品作成処理
@app.route('/items/create', methods=['POST'])
def create():
  item = Item(
    name=request.form.get('name'),
    category_id=request.form.get('category_id'),
    price=request.form.get('price'),
  )
  try:
    db.session.add(item)
    db.session.commit()
  except: 
    flash('入力した値を再度確認してください', 'error')
    return redirect(url_for('new'))
  flash('商品が作成されました', 'success')
  return redirect(url_for('index'))

# 商品更新画面を表示
@app.route('/<int:id>/edit')
def edit(id):
  item = Item.query.get(id)
  categories = Category.query.all()
  return render_template('items/edit.html', item=item, categories=categories)

# 商品更新処理
@app.route('/<int:id>/update', methods=['POST'])
def update(id):
  item = Item.query.get(id)
  item.name = request.form.get('name')
  item.category_id = request.form.get('category_id')
  item.price = request.form.get('price')
  try:
    db.session.merge(item)
    db.session.commit()
  except: 
    flash('入力した値を再度確認してください', 'danger')
    return redirect(url_for('new'))
  flash('商品が更新されました', 'success')
  return redirect(url_for('index'))

# 商品削除処理
@app.route('/<int:id>/delete', methods=['POST'])
def delete(id):
  item = Item.query.get(id)
  db.session.delete(item)
  db.session.commit()
  flash('商品が削除されました', 'success')
  return redirect(url_for('index'))

#test_item の表のデータ全て表示する画面
@app.route('/test_item')
def index_2():
  test_item = Test_item.query.all() 
  fassion_table = []
  for item in test_item: 
    fassion_table.append(f'{item.id}, {item.name}, {item.price}')
  return fassion_table

#test_item の表の指定したIDのみを記載した画面
@app.route('/test_item/<int:id>')
def show_2(id):
  test_items = Test_item.query.get(id)
  dict = {}
  dict["id"] = test_items.id
  dict["name"] = test_items.name
  dict["price"] = test_items.price
  return dict


#test_categoriesの表のデータ全て表示する画面
@app.route('/test_categories')
def index_3():
  test_categories = Test_categories.query.all() 
  gender_category = []
  for gender in test_categories: 
    gender_category.append(f'{gender.id}, {gender.name}')
  return gender_category