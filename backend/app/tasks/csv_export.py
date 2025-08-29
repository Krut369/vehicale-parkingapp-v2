# app/tasks/csv_export.py
import csv
from datetime import datetime
from app.tasks.celery_config import celery
from app import db
from app.models import Reservation, ParkingSpot, ParkingLot, User
import os

@celery.task
def export_reservations_csv(user_id):
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    user = User.query.get(user_id)

    filename = f"reservation_export_user_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    file_path = os.path.join('exports', filename)

    os.makedirs('exports', exist_ok=True)

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Spot ID', 'Lot Name', 'Start Time', 'End Time', 'Cost'])

        for res in reservations:
            spot = ParkingSpot.query.get(res.spot_id)
            lot = ParkingLot.query.get(spot.lot_id)
            writer.writerow([
                res.spot_id,
                lot.name,
                res.start_time,
                res.end_time,
                res.cost
            ])

    return {'message': 'CSV export completed', 'file_path': file_path}
