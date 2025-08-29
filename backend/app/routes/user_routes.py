# app/routes/user_routes.py
from flask import Blueprint, request, jsonify
from app.models import db, ParkingLot, ParkingSpot, Reservation, User
from datetime import datetime

user_bp = Blueprint('user', __name__)

# View available parking lots with at least 1 free spot
@user_bp.route('/available-lots', methods=['GET'])
def available_lots():
    lots = ParkingLot.query.all()
    available = []
    for lot in lots:
        spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').all()
        if spots:
            available.append({
                'id': lot.id,
                'name': lot.name,
                'address': lot.address,
                'price_per_hour': lot.price_per_hour,
                'available_spots': len(spots)
            })
    return jsonify(available)

# Book the first available spot from selected lot
@user_bp.route('/book', methods=['POST'])
def book_spot():
    data = request.get_json()
    lot_id = data['lot_id']
    user_id = data['user_id']

    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not spot:
        return jsonify({'message': 'No available spots in this lot'}), 404

    # Get user and lot information for notification
    user = User.query.get(user_id)
    lot = ParkingLot.query.get(lot_id)

    # Mark as occupied
    spot.status = 'O'
    reservation = Reservation(
        spot_id=spot.id,
        user_id=user_id,
        start_time=datetime.utcnow()
    )
    db.session.add(reservation)
    db.session.commit()
    
    # Send WhatsApp notification if user has phone number
    if user and user.phone_number and user.phone_number.strip() and user.phone_number.strip() != 'None' and lot:
        try:
            from app.services.whatsapp_service import WhatsAppService
            whatsapp = WhatsAppService()
            
            result = whatsapp.send_booking_confirmation(
                phone_number=user.phone_number,
                username=user.username,
                lot_name=lot.name,
                spot_id=spot.id,
                start_time=reservation.start_time.strftime('%Y-%m-%d %H:%M:%S')
            )
            
            if result['success']:
                print(f"📱 WhatsApp booking confirmation sent to {user.username}")
            else:
                print(f"❌ WhatsApp booking confirmation failed for {user.username}: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"⚠️ Could not send WhatsApp booking confirmation: {e}")
    elif user and not user.phone_number:
        print(f"📧 Booking confirmation for {user.username}: No WhatsApp number available")
    
    return jsonify({'message': 'Spot booked', 'spot_id': spot.id}), 200

# Release a spot and calculate cost
@user_bp.route('/release', methods=['POST'])
def release_spot():
    data = request.get_json()
    user_id = data['user_id']
    
    # Get ongoing reservation
    reservation = Reservation.query.filter_by(user_id=user_id, end_time=None).first()
    if not reservation:
        return jsonify({'message': 'No active reservation found'}), 404

    reservation.end_time = datetime.utcnow()
    
    # Calculate cost
    duration = (reservation.end_time - reservation.start_time).total_seconds() / 3600
    spot = ParkingSpot.query.get(reservation.spot_id)
    lot = ParkingLot.query.get(spot.lot_id)
    reservation.cost = round(duration * lot.price_per_hour, 2)

    # Mark spot as available
    spot.status = 'A'
    db.session.commit()
    
    # Send WhatsApp notification if user has phone number
    user = User.query.get(user_id)
    if user and user.phone_number and user.phone_number.strip() and user.phone_number.strip() != 'None' and lot:
        try:
            from app.services.whatsapp_service import WhatsAppService
            whatsapp = WhatsAppService()
            
            result = whatsapp.send_spot_released(
                phone_number=user.phone_number,
                username=user.username,
                lot_name=lot.name,
                spot_id=spot.id,
                cost=reservation.cost,
                duration=duration
            )
            
            if result['success']:
                print(f"📱 WhatsApp spot release notification sent to {user.username}")
            else:
                print(f"❌ WhatsApp spot release notification failed for {user.username}: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"⚠️ Could not send WhatsApp spot release notification: {e}")
    elif user and not user.phone_number:
        print(f"📧 Spot release notification for {user.username}: No WhatsApp number available")

    return jsonify({'message': 'Spot released', 'cost': reservation.cost}), 200

# View user's past reservations
@user_bp.route('/history/<int:user_id>', methods=['GET'])
def reservation_history(user_id):
    history = Reservation.query.filter_by(user_id=user_id).all()
    data = []
    for res in history:
        lot = ParkingLot.query.get(ParkingSpot.query.get(res.spot_id).lot_id)
        data.append({
            'spot_id': res.spot_id,
            'lot_name': lot.name,
            'start_time': res.start_time.isoformat() if res.start_time else None,
            'end_time': res.end_time.isoformat() if res.end_time else None,
            'cost': res.cost
        })
    return jsonify(data)

# Get user's active reservation
@user_bp.route('/active-reservation/<int:user_id>', methods=['GET'])
def get_active_reservation(user_id):
    active_reservation = Reservation.query.filter_by(user_id=user_id, end_time=None).first()
    
    if not active_reservation:
        return jsonify({'message': 'No active reservation found'}), 404
    
    spot = ParkingSpot.query.get(active_reservation.spot_id)
    lot = ParkingLot.query.get(spot.lot_id)
    
    data = {
        'reservation_id': active_reservation.id,
        'spot_id': active_reservation.spot_id,
        'lot_name': lot.name,
        'start_time': active_reservation.start_time.isoformat(),
        'cost': active_reservation.cost
    }
    
    return jsonify(data)

# Export user's reservation history as CSV
@user_bp.route('/export-csv', methods=['POST', 'OPTIONS'])
def export_csv():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    try:
        # Get user's reservation history
        reservations = Reservation.query.filter_by(user_id=user_id).all()
        
        if not reservations:
            return jsonify({'message': 'No reservations found to export'}), 404
        
        # Create CSV data
        csv_data = []
        for res in reservations:
            spot = ParkingSpot.query.get(res.spot_id)
            lot = ParkingLot.query.get(spot.lot_id) if spot else None
            
            csv_data.append({
                'reservation_id': res.id,
                'lot_name': lot.name if lot else 'Unknown',
                'spot_id': res.spot_id,
                'start_time': res.start_time.strftime('%Y-%m-%d %H:%M:%S') if res.start_time else '',
                'end_time': res.end_time.strftime('%Y-%m-%d %H:%M:%S') if res.end_time else '',
                'cost': res.cost if res.cost else 0,
                'status': 'Completed' if res.end_time else 'Active'
            })
        
        return jsonify({
            'message': 'CSV export data prepared',
            'data': csv_data,
            'count': len(csv_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500
