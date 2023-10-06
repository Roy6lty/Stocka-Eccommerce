
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
├── instance                         -Contains the  dbms system
├── invoice                          -Generatered invoice for purchases.
├── src                             - contains files required by the application to run the flask code and blueprints
    ├──checkout_app                  - starting point of the application blueprint
    |   ├──checkout_templates         - contains html files for checkout 
    |   ├──static                    - contains static files for checkout page
    |   
    |   
    ├──login_app                      - contains pythons for login and user authentication
    |   ├──login_templates            -contains html files for Login
    |   ├──static                      -contains static files for login page 
    |     
    |
    ├──market_app                      - contains pythons for product and shopping page
    |   ├──market_templates            -contains html files for shoppping page
    |    ├──static                      -contains static files for shopping page 
    |
    |
    ├──Product_app                      -contains pythons for product page and  products added
    |   ├──product_templates            -contains html files for produuct page
    |    ├──static                      -contains static files for product page 
    |
    |
    ├── Templates                       -contains html base html files
    ├──uploads                          -contains uploaded profile pics for users

    ├──User_profile                      -contains pythons for user profile
    |   ├──user_templates               -contains html files for userprofile page
    |    ├──static                      -contains static files for product page 
    |
    ├──init.py                          -intialization 
    ├──cart.py                          -cart funitionalities
    ├──extentions.py                     -contains commonly used file imports
    ├──forms.py                          -contains forms
    ├── models.py                        -database table models   
    ├──MongoCrud.py                      -MongoDb CRUD operations
    |   
    | 
├── static                                -static images
├──run.py                                 -entry point


#### Requirements
- install dependencies in the requirements.txt
- configure the redis database uri
- configure the mongo base uri
-