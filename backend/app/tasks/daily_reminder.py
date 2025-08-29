# app/tasks/daily_reminder.py
from app.tasks.celery_config import celery
from app.models import db, User, Reservation, ParkingLot, ParkingSpot
from datetime import datetime, timedelta
import logging
import sys
import os

# Add the app directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery.task
def send_daily_reminders():
    """Send daily reminders to users who haven't booked parking recently"""
    try:
        logger.info("Starting daily reminder task...")
        
        users = User.query.filter_by(role='user').all()
        yesterday = datetime.utcnow() - timedelta(days=1)
        reminder_count = 0

        for user in users:
            # Get the user's most recent reservation
            last_res = Reservation.query.filter_by(user_id=user.id).order_by(Reservation.start_time.desc()).first()
            
            # Send reminder if user has no reservations or last reservation was more than 1 day ago
            if not last_res or (last_res and last_res.start_time < yesterday):
                reminder_count += 1
                send_reminder_to_user(user)
        
        logger.info(f"Daily reminder task completed. Sent {reminder_count} reminders.")
        return f"Sent {reminder_count} reminders"
        
    except Exception as e:
        logger.error(f"Error in daily reminder task: {e}")
        raise

def send_reminder_to_user(user):
    """Send a reminder to a specific user via WhatsApp"""
    try:
        # Get available parking lots count
        available_lots = 0
        try:
            lots = ParkingLot.query.all()
            for lot in lots:
                available_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
                if available_spots > 0:
                    available_lots += 1
        except Exception as e:
            logger.warning(f"Could not get available lots count: {e}")
            available_lots = 3  # Default fallback
        
        # Send WhatsApp message if phone number is available
        if user.phone_number and user.phone_number.strip() and user.phone_number.strip() != 'None':
            try:
                from app.services.whatsapp_service import WhatsAppService
                whatsapp = WhatsAppService()
                
                result = whatsapp.send_daily_reminder(
                    phone_number=user.phone_number,
                    username=user.username,
                    available_lots=available_lots
                )
                
                if result['success']:
                    logger.info(f"✅ WhatsApp reminder sent to {user.username} ({user.phone_number})")
                    print(f"📱 WhatsApp reminder sent to {user.username}: {result['message']}")
                else:
                    logger.error(f"❌ WhatsApp reminder failed for {user.username}: {result.get('error', 'Unknown error')}")
                    print(f"❌ WhatsApp reminder failed for {user.username}: {result.get('error', 'Unknown error')}")
                    
            except ImportError as e:
                logger.error(f"Could not import WhatsApp service: {e}")
                print(f"⚠️ WhatsApp service not available for {user.username}")
            except Exception as e:
                logger.error(f"Error sending WhatsApp reminder to {user.username}: {e}")
                print(f"❌ Error sending WhatsApp reminder to {user.username}: {e}")
        else:
            # Fallback to console logging if no phone number
            message = f"[DAILY REMINDER] Hello {user.username}, don't forget to book your parking spot today!"
            logger.info(message)
            print(f"📧 Console reminder for {user.username} ({user.email}): No WhatsApp number available")
        
    except Exception as e:
        logger.error(f"Error sending reminder to user {user.username}: {e}")

@celery.task
def send_weekly_summary():
    """Send weekly summary to all users"""
    try:
        logger.info("Starting weekly summary task...")
        
        users = User.query.filter_by(role='user').all()
        summary_count = 0

        for user in users:
            # Get user's reservations from the last week
            week_ago = datetime.utcnow() - timedelta(days=7)
            recent_reservations = Reservation.query.filter(
                Reservation.user_id == user.id,
                Reservation.start_time >= week_ago
            ).all()
            
            if recent_reservations:
                send_weekly_summary_to_user(user, recent_reservations)
                summary_count += 1
        
        logger.info(f"Weekly summary task completed. Sent {summary_count} summaries.")
        return f"Sent {summary_count} weekly summaries"
        
    except Exception as e:
        logger.error(f"Error in weekly summary task: {e}")
        raise

def send_weekly_summary_to_user(user, reservations):
    """Send weekly summary to a specific user via WhatsApp"""
    try:
        total_cost = sum(r.cost or 0 for r in reservations)
        
        # Calculate total hours from reservations
        total_hours = 0
        for res in reservations:
            if res.end_time and res.start_time:
                duration = (res.end_time - res.start_time).total_seconds() / 3600
                total_hours += duration
        
        # Send WhatsApp message if phone number is available
        if user.phone_number and user.phone_number.strip() and user.phone_number.strip() != 'None':
            try:
                from app.services.whatsapp_service import WhatsAppService
                whatsapp = WhatsAppService()
                
                result = whatsapp.send_weekly_summary(
                    phone_number=user.phone_number,
                    username=user.username,
                    total_reservations=len(reservations),
                    total_hours=total_hours,
                    total_cost=total_cost
                )
                
                if result['success']:
                    logger.info(f"✅ WhatsApp weekly summary sent to {user.username} ({user.phone_number})")
                    print(f"📱 WhatsApp weekly summary sent to {user.username}: {len(reservations)} reservations, ₹{total_cost:.2f}")
                else:
                    logger.error(f"❌ WhatsApp weekly summary failed for {user.username}: {result.get('error', 'Unknown error')}")
                    print(f"❌ WhatsApp weekly summary failed for {user.username}: {result.get('error', 'Unknown error')}")
                    
            except ImportError as e:
                logger.error(f"Could not import WhatsApp service: {e}")
                print(f"⚠️ WhatsApp service not available for {user.username}")
            except Exception as e:
                logger.error(f"Error sending WhatsApp weekly summary to {user.username}: {e}")
                print(f"❌ Error sending WhatsApp weekly summary to {user.username}: {e}")
        else:
            # Fallback to console logging if no phone number
            message = f"""
            [WEEKLY SUMMARY] Hello {user.username}!
            
            Your parking activity this week:
            - Reservations: {len(reservations)}
            - Total hours: {total_hours:.1f}h
            - Total cost: ₹{total_cost:.2f}
            
            Keep up the great parking habits!
            """
            
            logger.info(f"Weekly summary for {user.username}: {len(reservations)} reservations, ₹{total_cost:.2f}")
            print(f"📊 Console weekly summary for {user.username}: No WhatsApp number available")
        
    except Exception as e:
        logger.error(f"Error sending weekly summary to user {user.username}: {e}")

# Schedule tasks
@celery.task
def schedule_daily_reminders():
    """Schedule daily reminders at 9 AM every day"""
    from celery.schedules import crontab
    
    # This will be called by the scheduler
    send_daily_reminders.delay()

@celery.task
def schedule_weekly_summaries():
    """Schedule weekly summaries every Sunday at 10 AM"""
    from celery.schedules import crontab
    
    # This will be called by the scheduler
    send_weekly_summary.delay()
