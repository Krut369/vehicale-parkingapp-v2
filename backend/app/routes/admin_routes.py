from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.models import db, ParkingLot, ParkingSpot, User, Reservation

admin_bp = Blueprint('admin', __name__)

# Test endpoint to verify backend is working
@admin_bp.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({'message': 'Admin backend is working!', 'status': 'ok'})

# ------------------------ Parking Lot Routes ------------------------

@admin_bp.route('/create-lot', methods=['POST'])
def create_parking_lot():
    data = request.get_json()
    lot = ParkingLot(
        name=data['name'],
        address=data['address'],
        pin_code=data['pin_code'],
        price_per_hour=data['price_per_hour'],
        total_spots=data['total_spots']
    )
    db.session.add(lot)
    db.session.flush()

    for _ in range(lot.total_spots):
        spot = ParkingSpot(lot_id=lot.id)
        db.session.add(spot)

    db.session.commit()
    return jsonify({'message': 'Parking lot and spots created successfully'}), 201

@admin_bp.route('/lots', methods=['GET'])
def view_lots():
    lots = ParkingLot.query.all()
    result = []
    for lot in lots:
        result.append({
            'id': lot.id,
            'name': lot.name,
            'address': lot.address,
            'price_per_hour': lot.price_per_hour,
            'total_spots': lot.total_spots
        })
    return jsonify(result)

@admin_bp.route('/delete-lot/<int:lot_id>', methods=['DELETE'])
def delete_lot(lot_id):
    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({'message': 'Lot not found'}), 404

    occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').first()
    if occupied:
        return jsonify({'message': 'Cannot delete lot. Some spots are still occupied.'}), 400

    ParkingSpot.query.filter_by(lot_id=lot.id).delete()
    db.session.delete(lot)
    db.session.commit()
    return jsonify({'message': 'Lot deleted'}), 200

@admin_bp.route('/spot-status', methods=['GET'])
def view_all_spots_status():
    lots = ParkingLot.query.all()
    data = []
    for lot in lots:
        spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
        available = sum(1 for s in spots if s.status == 'A')
        occupied = sum(1 for s in spots if s.status == 'O')
        data.append({
            'lot_name': lot.name,
            'total_spots': lot.total_spots,
            'available': available,
            'occupied': occupied
        })
    return jsonify(data)

@admin_bp.route('/reservations', methods=['GET'])
def view_all_reservations():
    """Get all current and recent reservations with detailed information"""
    try:
        # Get all active reservations (ongoing)
        active_reservations = Reservation.query.filter_by(end_time=None).all()
        print(f"[DEBUG] Found {len(active_reservations)} active reservations")
        
        # Get recent completed reservations (last 24 hours)
        from datetime import datetime, timedelta
        yesterday = datetime.utcnow() - timedelta(hours=24)
        recent_reservations = Reservation.query.filter(
            Reservation.end_time >= yesterday
        ).all()
        print(f"[DEBUG] Found {len(recent_reservations)} recent reservations")
        
        # Combine and format data
        all_reservations = active_reservations + recent_reservations
        data = []
        
        for res in all_reservations:
            try:
                spot = ParkingSpot.query.get(res.spot_id)
                if not spot:
                    print(f"[WARNING] Spot {res.spot_id} not found for reservation {res.id}")
                    continue
                    
                lot = ParkingLot.query.get(spot.lot_id)
                if not lot:
                    print(f"[WARNING] Lot not found for spot {res.spot_id}")
                    continue
                    
                user = User.query.get(res.user_id)
                if not user:
                    print(f"[WARNING] User {res.user_id} not found for reservation {res.id}")
                    continue
                
                data.append({
                    'reservation_id': res.id,
                    'lot_name': lot.name,
                    'spot_id': res.spot_id,
                    'user_username': user.username,
                    'user_email': user.email,
                    'start_time': res.start_time.isoformat(),
                    'end_time': res.end_time.isoformat() if res.end_time else None,
                    'cost': res.cost,
                    'status': 'Active' if res.end_time is None else 'Completed',
                    'duration_hours': round((res.end_time - res.start_time).total_seconds() / 3600, 2) if res.end_time else None
                })
            except Exception as e:
                print(f"[ERROR] Error processing reservation {res.id}: {e}")
                continue
        
        print(f"[DEBUG] Returning {len(data)} formatted reservations")
        return jsonify(data)
        
    except Exception as e:
        print(f"[ERROR] Error in view_all_reservations: {e}")
        return jsonify({'error': str(e)}), 500

# ------------------------ User Management (Admin Only) ------------------------

@admin_bp.route('/users', methods=['GET'])
def view_users():
    users = User.query.filter_by(role='user').all()
    return jsonify([{'id': u.id, 'username': u.username, 'email': u.email} for u in users])

@admin_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409

    hashed_password = generate_password_hash(data['password'])

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        phone_number=data.get('phone_number'),  # Optional WhatsApp number
        role='user'
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user or user.role != 'user':
        return jsonify({'message': 'User not found'}), 404

    user.email = data.get('email', user.email)
    user.username = data.get('username', user.username)
    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user or user.role != 'user':
        return jsonify({'message': 'User not found or not deletable'}), 404

    Reservation.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200
