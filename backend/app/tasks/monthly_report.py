# app/tasks/monthly_report.py
from app.tasks.celery_config import celery
from app.models import db, User, Reservation, ParkingSpot, ParkingLot
from datetime import datetime, timedelta
from flask import render_template_string

@celery.task
def send_monthly_report():
    users = User.query.filter_by(role='user').all()
    now = datetime.utcnow()
    start_of_month = datetime(now.year, now.month, 1)

    for user in users:
        reservations = Reservation.query.filter(
            Reservation.user_id == user.id,
            Reservation.start_time >= start_of_month
        ).all()

        total_cost = sum(r.cost or 0 for r in reservations)
        most_visited = {}
        for r in reservations:
            spot = ParkingSpot.query.get(r.spot_id)
            lot = ParkingLot.query.get(spot.lot_id)
            most_visited[lot.name] = most_visited.get(lot.name, 0) + 1

        most_used_lot = max(most_visited, key=most_visited.get) if most_visited else "N/A"

        html = render_template_string("""
            <h2>Monthly Parking Report</h2>
            <p>User: {{ user.username }}</p>
            <p>Total Reservations: {{ count }}</p>
            <p>Most Used Lot: {{ lot }}</p>
            <p>Total Spent: ₹{{ cost }}</p>
        """, user=user, count=len(reservations), lot=most_used_lot, cost=round(total_cost, 2))

        print(f"\n--- Monthly Report for {user.username} ---\n{html}\n")
        # TODO: Send this via email using Flask-Mail or SMTP
