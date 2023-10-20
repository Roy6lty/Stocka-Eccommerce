
#### Description
 This is a project is aimed at building a flask Ecoomerce Fullstack web_app

#### Features
- Role Based User Authentication 
- Carting System
- Reciept Generator
- Product Inventory and Management
- Email Notification 
- User profile and data management

#### App Navigation

```bash
├── Readme.md
├── __init__.py
├── __pycache__
│   ├── app.cpython-311.pyc
│   ├── app.cpython-39.pyc
│   ├── config.cpython-39.pyc
│   ├── flas.cpython-39.pyc
│   └── main.cpython-39.pyc
├── config.py
├── instance
│   └── database.db
├── invoice
│   ├── a9f062f0f6264b32.docx
│   ├── report.docx
│   ├── stockinvoice.docx
│   └── ~$ockinvoice.docx
├── requirements.txt
├── run.py
├── src
│   ├── MongoCRUD.py
│   ├── __init__.py
│   ├── cart.py
│   ├── checkout_app
│   │   ├── checkout_templates
│   │   │   └── complete_checkout.html
│   │   ├── static
│   │   │   └── checkout.css
│   │   ├── tasks.py
│   │   └── view_checkout.py
│   ├── extentions.py
│   ├── forms.py
│   ├── login_app
│   │   ├── __init__.py
│   │   ├── login_templates
│   │   │   ├── home.html
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   ├── resetpassword.html
│   │   │   └── verify_password.html
│   │   ├── static
│   │   │   └── images
│   │   │       └── Registration.png
│   │   └── view_login.py
│   ├── market_app
│   │   ├── __init__.py
│   │   ├── market_templates
│   │   │   ├── includes
│   │   │   │   └── items_modals.html
│   │   │   └── market.html
│   │   └── view_market.py
│   ├── merchant_app
│   │   ├── __init__.py
│   │   ├── merchant_templates
│   │   │   ├── includes
│   │   │   │   └── products_modal.html
│   │   │   ├── products.html
│   │   │   └── update_product.html
│   │   ├── static
│   │   │   └── product.css
│   │   └── view_merchant.py
│   ├── models.py
│   ├── product_app
│   │   ├── __init__.py
│   │   ├── product_templates
│   │   │   ├── add_product.html
│   │   │   ├── product_page.html
│   │   │   └── shopping.html
│   │   ├── static
│   │   │   ├── icons/
│   │   │   ├── product.css
│   │   │   ├── product_page.css
│   │   │   ├── product_pic/
│   │   │   │   ├── icons/
│   │   │   └── shopping_page.css
│   │   └── view_products.py
│   ├── static
│   │   ├── LOGO alt 3.png
│   │   ├── base.css
│   │   ├── cart.css
│   │   ├── cart.png
│   │   └── cart.png:Zone.Identifier
│   ├── templates
│   │   ├── base copy.html
│   │   ├── base.html
│   │   └── includes
│   │       ├── carts-modal.html
│   │       └── items_modals.html
│   ├── uploads
│   │   └── profile_pics/
│   ├── user_profile
│   │   ├── __init__.py
│   │   ├── static
│   │   │   └── profile_pic/
│   │   │       
│   │   ├── user_templates
│   │   │   ├── account.html
│   │   │   └── bckup.html
│   │   └── view_profile.py
│   └── utils.py
└── static
    └── images
```
#### Requirements
- install dependencies in the requirements.txt
- configure the redis database uri
- configure the mongo base uri
