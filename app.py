# import pickle
# import pandas as pd
# from flask import Flask, request, render_template
# from sklearn.preprocessing import StandardScaler

# app = Flask(__name__)

# # Load the trained model and preprocessing objects
# with open("fraud_detection_model.pkl", "rb") as model_file:
#     model, ohe, ordinal_encoder, scaler, label_encoder = pickle.load(model_file)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     # Get input data from form
#     input_data = {
#         'ASSURED_AGE': int(request.form['age']),
#         'OCCUPATION': request.form['occupation'],
#         'POLICY SUMASSURED': float(request.form['policy_sum_assured'].replace(',', '')),
#         'Premium': float(request.form['premium']),
#         'PREMIUMPAYMENTMODE': request.form['premium_payment_mode'],
#         'Annual Income': float(request.form['annual_income']),
#         'HOLDERMARITALSTATUS': request.form['marital_status'],
#         'INDIV_REQUIREMENTFLAG': request.form['requirement_flag'],
#         'CORRESPONDENCEPOSTCODE': request.form['postcode'],
#         'Product Type': request.form['product_type'],
#         'CHANNEL': request.form['channel'],
#         'STATUS': request.form['status'],
#         'SUB_STATUS': request.form['sub_status']
#     }
    
#     # Convert to DataFrame
#     df = pd.DataFrame([input_data])
    
#     # Feature engineering
#     df['Debt_to_Income_Ratio'] = df['Premium'] / df['Annual Income']
#     df.drop(columns=['Premium', 'Annual Income'], inplace=True)
    
#     # Apply encodings
#     categorical_cols_ohe = ['OCCUPATION', 'Product Type', 'CHANNEL', 'CORRESPONDENCEPOSTCODE']
#     categorical_cols_ordinal = ['PREMIUMPAYMENTMODE', 'HOLDERMARITALSTATUS', 'INDIV_REQUIREMENTFLAG', 'STATUS', 'SUB_STATUS']
    
#     ohe_data = pd.DataFrame(ohe.transform(df[categorical_cols_ohe]), 
#                             columns=ohe.get_feature_names_out(categorical_cols_ohe))
#     df[categorical_cols_ordinal] = ordinal_encoder.transform(df[categorical_cols_ordinal])
    
#     df = df.drop(columns=categorical_cols_ohe)
#     df = pd.concat([df, ohe_data], axis=1)
    
#     # Scale numerical features
#     numerical_cols = ['ASSURED_AGE', 'POLICY SUMASSURED', 'Debt_to_Income_Ratio']
#     df[numerical_cols] = scaler.transform(df[numerical_cols])
    
#     # Make prediction
#     prediction = model.predict(df)
#     fraud_status = label_encoder.inverse_transform(prediction)[0]
    
#     return render_template('result.html', prediction=fraud_status)

# if __name__ == '__main__':
#     app.run(debug=True)




# from flask import Flask, request, render_template, redirect, url_for, session, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# import pickle
# import pandas as pd

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# # Database configuration for user authentication
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # User model for the database
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)

# # Load the trained model and preprocessing objects
# with open("fraud_detection_model.pkl", "rb") as model_file:
#     model, ohe, ordinal_encoder, scaler, label_encoder = pickle.load(model_file)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             session['user'] = user.username
#             return redirect(url_for('dashboard'))
#         else:
#             return render_template('login.html', error="Invalid credentials")
#     return render_template('login.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = generate_password_hash(request.form['password'], method='sha256')
        
#         if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
#             return render_template('signup.html', error="User already exists")
        
#         new_user = User(username=username, email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('login'))
#     return render_template('signup.html')

# @app.route('/dashboard')
# def dashboard():
#     if 'user' in session:
#         return render_template('index.html', user=session['user'])
#     return redirect(url_for('login'))

# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect(url_for('home'))

# @app.route('/predict', methods=['POST'])
# def predict():
#     input_data = {
#         'ASSURED_AGE': int(request.form['age']),
#         'OCCUPATION': request.form['occupation'],
#         'POLICY SUMASSURED': float(request.form['policy_sum_assured'].replace(',', '')),
#         'Premium': float(request.form['premium']),
#         'PREMIUMPAYMENTMODE': request.form['premium_payment_mode'],
#         'Annual Income': float(request.form['annual_income']),
#         'HOLDERMARITALSTATUS': request.form['marital_status'],
#         'INDIV_REQUIREMENTFLAG': request.form['requirement_flag'],
#         'CORRESPONDENCEPOSTCODE': request.form['postcode'],
#         'Product Type': request.form['product_type'],
#         'CHANNEL': request.form['channel'],
#         'STATUS': request.form['status'],
#         'SUB_STATUS': request.form['sub_status']
#     }
    
#     df = pd.DataFrame([input_data])
#     df['Debt_to_Income_Ratio'] = df['Premium'] / df['Annual Income']
#     df.drop(columns=['Premium', 'Annual Income'], inplace=True)
    
#     categorical_cols_ohe = ['OCCUPATION', 'Product Type', 'CHANNEL', 'CORRESPONDENCEPOSTCODE']
#     categorical_cols_ordinal = ['PREMIUMPAYMENTMODE', 'HOLDERMARITALSTATUS', 'INDIV_REQUIREMENTFLAG', 'STATUS', 'SUB_STATUS']
    
#     ohe_data = pd.DataFrame(ohe.transform(df[categorical_cols_ohe]), 
#                             columns=ohe.get_feature_names_out(categorical_cols_ohe))
#     df[categorical_cols_ordinal] = ordinal_encoder.transform(df[categorical_cols_ordinal])
    
#     df.drop(columns=categorical_cols_ohe, inplace=True)
#     df = pd.concat([df, ohe_data], axis=1)
    
#     numerical_cols = ['ASSURED_AGE', 'POLICY SUMASSURED', 'Debt_to_Income_Ratio']
#     df[numerical_cols] = scaler.transform(df[numerical_cols])
    
#     prediction = model.predict(df)
#     fraud_status = label_encoder.inverse_transform(prediction)[0]
    
#     return render_template('result.html', prediction=fraud_status)

# @app.route('/chatbot')
# def chatbot():
#     return render_template('chatbot.html')

# if __name__ == '__main__':
#     db.create_all()  # Create the database tables if they don't exist
#     app.run(debug=True)






# from flask import Flask, request, render_template, redirect, url_for, session
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# import pickle
# import pandas as pd

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# # Database configuration for user authentication
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # User model for the database
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)

# # Load the trained model and preprocessing objects
# with open("fraud_detection_model.pkl", "rb") as model_file:
#     model, ohe, ordinal_encoder, scaler, label_encoder = pickle.load(model_file)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             session['user'] = user.username
#             return redirect(url_for('dashboard'))
#         else:
#             return render_template('login.html', error="Invalid credentials")
#     return render_template('login.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = generate_password_hash(request.form['password'], method='sha256')
        
#         if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
#             return render_template('signup.html', error="User already exists")
        
#         new_user = User(username=username, email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('login'))
#     return render_template('signup.html')

# @app.route('/dashboard')
# def dashboard():
#     if 'user' in session:
#         return render_template('index.html', user=session['user'])
#     return redirect(url_for('login'))

# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect(url_for('home'))

# @app.route('/predict', methods=['POST'])
# def predict():
#     input_data = {
#         'ASSURED_AGE': int(request.form['age']),
#         'OCCUPATION': request.form['occupation'],
#         'POLICY SUMASSURED': float(request.form['policy_sum_assured'].replace(',', '')),
#         'Premium': float(request.form['premium']),
#         'PREMIUMPAYMENTMODE': request.form['premium_payment_mode'],
#         'Annual Income': float(request.form['annual_income']),
#         'HOLDERMARITALSTATUS': request.form['marital_status'],
#         'INDIV_REQUIREMENTFLAG': request.form['requirement_flag'],
#         'CORRESPONDENCEPOSTCODE': request.form['postcode'],
#         'Product Type': request.form['product_type'],
#         'CHANNEL': request.form['channel'],
#         'STATUS': request.form['status'],
#         'SUB_STATUS': request.form['sub_status']
#     }
    
#     df = pd.DataFrame([input_data])
#     df['Debt_to_Income_Ratio'] = df['Premium'] / df['Annual Income']
#     df.drop(columns=['Premium', 'Annual Income'], inplace=True)
    
#     categorical_cols_ohe = ['OCCUPATION', 'Product Type', 'CHANNEL', 'CORRESPONDENCEPOSTCODE']
#     categorical_cols_ordinal = ['PREMIUMPAYMENTMODE', 'HOLDERMARITALSTATUS', 'INDIV_REQUIREMENTFLAG', 'STATUS', 'SUB_STATUS']
    
#     ohe_data = pd.DataFrame(ohe.transform(df[categorical_cols_ohe]), 
#                             columns=ohe.get_feature_names_out(categorical_cols_ohe))
#     df[categorical_cols_ordinal] = ordinal_encoder.transform(df[categorical_cols_ordinal])
    
#     df.drop(columns=categorical_cols_ohe, inplace=True)
#     df = pd.concat([df, ohe_data], axis=1)
    
#     numerical_cols = ['ASSURED_AGE', 'POLICY SUMASSURED', 'Debt_to_Income_Ratio']
#     df[numerical_cols] = scaler.transform(df[numerical_cols])
    
#     prediction = model.predict(df)
#     fraud_status = label_encoder.inverse_transform(prediction)[0]
    
#     return render_template('result.html', prediction=fraud_status)

# @app.route('/chatbot')
# def chatbot():
#     return render_template('chatbot.html')

# if __name__ == '__main__':
#     db.create_all()  # Create the database tables if they don't exist
#     app.run(debug=True)




from flask import Flask, request, render_template, redirect, url_for, session
import pickle
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simple in-memory storage for users
users = {}

# Load the trained model and preprocessing objects
with open("fraud_detection_model.pkl", "rb") as model_file:
    model, ohe, ordinal_encoder, scaler, label_encoder = pickle.load(model_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if username in users:
            return render_template('signup.html', error="User already exists")
        
        users[username] = {
            'email': email,
            'password': password
        }
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('index.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/predict', methods=['POST'])
def predict():
    input_data = {
        'ASSURED_AGE': int(request.form['age']),
        'OCCUPATION': request.form['occupation'],
        'POLICY SUMASSURED': float(request.form['policy_sum_assured'].replace(',', '')),
        'Premium': float(request.form['premium']),
        'PREMIUMPAYMENTMODE': request.form['premium_payment_mode'],
        'Annual Income': float(request.form['annual_income']),
        'HOLDERMARITALSTATUS': request.form['marital_status'],
        'INDIV_REQUIREMENTFLAG': request.form['requirement_flag'],
        'CORRESPONDENCEPOSTCODE': request.form['postcode'],
        'Product Type': request.form['product_type'],
        'CHANNEL': request.form['channel'],
        'STATUS': request.form['status'],
        'SUB_STATUS': request.form['sub_status']
    }
    
    df = pd.DataFrame([input_data])
    df['Debt_to_Income_Ratio'] = df['Premium'] / df['Annual Income']
    df.drop(columns=['Premium', 'Annual Income'], inplace=True)
    
    categorical_cols_ohe = ['OCCUPATION', 'Product Type', 'CHANNEL', 'CORRESPONDENCEPOSTCODE']
    categorical_cols_ordinal = ['PREMIUMPAYMENTMODE', 'HOLDERMARITALSTATUS', 'INDIV_REQUIREMENTFLAG', 'STATUS', 'SUB_STATUS']
    
    ohe_data = pd.DataFrame(ohe.transform(df[categorical_cols_ohe]), 
                            columns=ohe.get_feature_names_out(categorical_cols_ohe))
    df[categorical_cols_ordinal] = ordinal_encoder.transform(df[categorical_cols_ordinal])
    
    df.drop(columns=categorical_cols_ohe, inplace=True)
    df = pd.concat([df, ohe_data], axis=1)
    
    numerical_cols = ['ASSURED_AGE', 'POLICY SUMASSURED', 'Debt_to_Income_Ratio']
    df[numerical_cols] = scaler.transform(df[numerical_cols])
    
    prediction = model.predict(df)
    fraud_status = label_encoder.inverse_transform(prediction)[0]
    
    return render_template('result.html', prediction=fraud_status)

if __name__ == '__main__':
    # Add warnings suppression for scikit-learn version mismatch
    import warnings
    warnings.filterwarnings('ignore', category=UserWarning)
    
    app.run(debug=True)
