# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    
    # Enhanced CORS configuration
    CORS(app, 
         origins=["http://localhost:5173", "http://localhost:5174"], 
         supports_credentials=True, 
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
         expose_headers=["Content-Type", "Authorization"])

    # Remove the manual CORS headers since Flask-CORS handles them
    # @app.after_request
    # def after_request(response):
    #     response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    #     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With')
    #     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    #     response.headers.add('Access-Control-Allow-Credentials', 'true')
    #     return response

    from .models import User, ParkingLot, ParkingSpot, Reservation

    with app.app_context():
        print("[INFO] Creating database tables if not exist...")
        db.create_all()
        print("[INFO] Database setup complete.")

        # Default admin credentials
        admin_username = 'anand'
        admin_password = 'anand123'
        admin_email = 'anand@admin.com'

        admin = User.query.filter_by(username=admin_username).first()
        hashed_password = generate_password_hash(admin_password, method='pbkdf2:sha256')

        if admin:
            # Update password/email if needed
            admin.password = hashed_password
            admin.email = admin_email
            db.session.commit()
            print(f"[INFO] Admin already exists. Password/Email updated for {admin.username}")
        else:
            try:
                admin = User(
                    username=admin_username,
                    password=hashed_password,
                    email=admin_email,
                    role='admin'
                )
                db.session.add(admin)
                db.session.commit()
                print(f"[INFO] Default admin user created: {admin_username} / {admin_password} (hashed)")
            except Exception as e:
                print(f"[ERROR] Failed to create admin user: {e}")

        # Create sample regular user
        user_username = 'user'
        user_password = 'user123'
        user_email = 'user@example.com'

        user = User.query.filter_by(username=user_username).first()
        user_hashed_password = generate_password_hash(user_password, method='pbkdf2:sha256')

        if user:
            # Update password/email if needed
            user.password = user_hashed_password
            user.email = user_email
            db.session.commit()
            print(f"[INFO] User already exists. Password/Email updated for {user.username}")
        else:
            try:
                user = User(
                    username=user_username,
                    password=user_hashed_password,
                    email=user_email,
                    role='user'
                )
                db.session.add(user)
                db.session.commit()
                print(f"[INFO] Default user created: {user_username} / {user_password} (hashed)")
            except Exception as e:
                print(f"[ERROR] Failed to create user: {e}")

        # Create sample parking lots and spots
        print("[INFO] Creating sample parking lots and spots...")
        
        # Check if lots already exist
        existing_lots = ParkingLot.query.all()
        if not existing_lots:
            try:
                # Create sample parking lots
                lot1 = ParkingLot(
                    name='Central Mall Parking',
                    address='123 Main Street, City Center',
                    pin_code='123456',
                    price_per_hour=50.0,
                    total_spots=20
                )
                lot2 = ParkingLot(
                    name='Downtown Plaza',
                    address='456 Oak Avenue, Downtown',
                    pin_code='654321',
                    price_per_hour=40.0,
                    total_spots=15
                )
                lot3 = ParkingLot(
                    name='Airport Parking',
                    address='789 Airport Road, Terminal 1',
                    pin_code='789012',
                    price_per_hour=80.0,
                    total_spots=30
                )
                
                db.session.add_all([lot1, lot2, lot3])
                db.session.commit()
                
                # Create parking spots for each lot
                lots = [lot1, lot2, lot3]
                for lot in lots:
                    for i in range(1, lot.total_spots + 1):
                        spot = ParkingSpot(
                            lot_id=lot.id,
                            status='A'  # Available
                        )
                        db.session.add(spot)
                
                db.session.commit()
                print(f"[INFO] Created {len(lots)} parking lots with spots")
            except Exception as e:
                print(f"[ERROR] Failed to create sample data: {e}")
        else:
            print(f"[INFO] {len(existing_lots)} parking lots already exist")

    # Register blueprints
    from .routes.auth_routes import auth_bp
    from .routes.admin_routes import admin_bp
    from .routes.user_routes import user_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(user_bp, url_prefix='/api/user')

    print("[INFO] Flask app setup complete.")
    return app
