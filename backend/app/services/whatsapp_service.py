# app/services/whatsapp_service.py
import requests
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class WhatsAppService:
    """WhatsApp messaging service using Fonnte API"""
    
    def __init__(self, api_token: str = "9cDHTvVYGQjqkKHMGCE1"):
        self.api_token = api_token
        self.base_url = "https://api.fonnte.com/send"
        self.headers = {
            'Authorization': api_token
        }
    
    def send_message(self, 
                    target_numbers: List[str], 
                    message: str, 
                    delay: str = "2",
                    country_code: str = "91") -> Dict:
        """
        Send WhatsApp message using Fonnte API
        
        Args:
            target_numbers: List of phone numbers (with or without country code)
            message: Message content
            delay: Delay in seconds (can be range like "1-5")
            country_code: Country code for phone numbers
            
        Returns:
            Dict containing API response
        """
        try:
            # Check if target_numbers is empty or contains None/empty values
            if not target_numbers:
                return {
                    'success': False,
                    'error': 'No phone numbers provided',
                    'message': 'WhatsApp message not sent - no phone number available'
                }
            
            # Filter out None, empty, or invalid phone numbers
            valid_numbers = []
            for number in target_numbers:
                if number and str(number).strip() and str(number).strip() != 'None':
                    valid_numbers.append(number)
            
            if not valid_numbers:
                return {
                    'success': False,
                    'error': 'No valid phone numbers provided',
                    'message': 'WhatsApp message not sent - no valid phone number available'
                }
            
            # Format target numbers
            formatted_targets = []
            for number in valid_numbers:
                # Remove any existing country code and add the specified one
                clean_number = str(number).lstrip('+').lstrip('62').lstrip('0')
                formatted_targets.append(f"{country_code}{clean_number}")
            
            target_string = ",".join(formatted_targets)
            
            # Prepare request data
            data = {
                'target': target_string,
                'message': message,
                'delay': delay,
                'countryCode': country_code,
                'typing': False
            }
            
            logger.info(f"Sending WhatsApp message to {len(target_numbers)} recipients")
            logger.debug(f"Target numbers: {target_string}")
            logger.debug(f"Message: {message}")
            
            # Make API request
            response = requests.post(
                self.base_url,
                data=data,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"WhatsApp message sent successfully. Response: {result}")
                return {
                    'success': True,
                    'response': result,
                    'message': 'WhatsApp message sent successfully'
                }
            else:
                logger.error(f"WhatsApp API error: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f"API Error: {response.status_code}",
                    'response': response.text
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error sending WhatsApp message: {e}")
            return {
                'success': False,
                'error': f"Network error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error sending WhatsApp message: {e}")
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}"
            }
    
    def send_daily_reminder(self, 
                           phone_number: str, 
                           username: str,
                           available_lots: int = 0) -> Dict:
        """
        Send daily parking reminder to a specific user
        
        Args:
            phone_number: User's phone number
            username: User's name
            available_lots: Number of available parking lots
            
        Returns:
            Dict containing send result
        """
        # Check if phone number is valid
        if not phone_number or not str(phone_number).strip() or str(phone_number).strip() == 'None':
            return {
                'success': False,
                'error': 'No phone number provided',
                'message': f'WhatsApp daily reminder not sent to {username} - no phone number available'
            }
        
        message = f"""🚗 *Daily Parking Reminder*

Hello {username}! 👋

Don't forget to book your parking spot today! 

📍 *Available parking lots:* {available_lots}
⏰ *Best time to book:* Morning hours
💰 *Save money:* Book early for better rates

Book now and enjoy hassle-free parking! 🎯

*Vehicle Parking App* 🚀"""

        return self.send_message([phone_number], message)
    
    def send_weekly_summary(self, 
                           phone_number: str, 
                           username: str,
                           total_reservations: int,
                           total_hours: float,
                           total_cost: float) -> Dict:
        """
        Send weekly parking summary to a user
        
        Args:
            phone_number: User's phone number
            username: User's name
            total_reservations: Number of reservations this week
            total_hours: Total hours parked
            total_cost: Total cost spent
            
        Returns:
            Dict containing send result
        """
        # Check if phone number is valid
        if not phone_number or not str(phone_number).strip() or str(phone_number).strip() == 'None':
            return {
                'success': False,
                'error': 'No phone number provided',
                'message': f'WhatsApp weekly summary not sent to {username} - no phone number available'
            }
        
        message = f"""📊 *Weekly Parking Summary*

Hello {username}! 👋

Here's your parking activity this week:

📅 *Reservations:* {total_reservations}
⏱️ *Total Hours:* {total_hours:.1f}h
💰 *Total Spent:* ₹{total_cost:.2f}

Keep up the great parking habits! 🎯

*Vehicle Parking App* 🚀"""

        return self.send_message([phone_number], message)
    
    def send_booking_confirmation(self, 
                                 phone_number: str,
                                 username: str,
                                 lot_name: str,
                                 spot_id: int,
                                 start_time: str) -> Dict:
        """
        Send booking confirmation message
        
        Args:
            phone_number: User's phone number
            username: User's name
            lot_name: Name of parking lot
            spot_id: Parking spot ID
            start_time: Booking start time
            
        Returns:
            Dict containing send result
        """
        # Check if phone number is valid
        if not phone_number or not str(phone_number).strip() or str(phone_number).strip() == 'None':
            return {
                'success': False,
                'error': 'No phone number provided',
                'message': f'WhatsApp booking confirmation not sent to {username} - no phone number available'
            }
        
        message = f"""✅ *Booking Confirmed!*

Hello {username}! 👋

Your parking spot has been successfully booked:

📍 *Location:* {lot_name}
🅿️ *Spot ID:* {spot_id}
⏰ *Start Time:* {start_time}

Enjoy your parking experience! 🚗

*Vehicle Parking App* 🚀"""

        return self.send_message([phone_number], message)
    
    def send_spot_released(self, 
                          phone_number: str,
                          username: str,
                          lot_name: str,
                          spot_id: int,
                          cost: float,
                          duration: float) -> Dict:
        """
        Send spot release confirmation with cost details
        
        Args:
            phone_number: User's phone number
            username: User's name
            lot_name: Name of parking lot
            spot_id: Parking spot ID
            cost: Total cost
            duration: Duration in hours
            
        Returns:
            Dict containing send result
        """
        # Check if phone number is valid
        if not phone_number or not str(phone_number).strip() or str(phone_number).strip() == 'None':
            return {
                'success': False,
                'error': 'No phone number provided',
                'message': f'WhatsApp spot release notification not sent to {username} - no phone number available'
            }
        
        message = f"""🔓 *Spot Released*

Hello {username}! 👋

Your parking session has ended:

📍 *Location:* {lot_name}
🅿️ *Spot ID:* {spot_id}
⏱️ *Duration:* {duration:.1f} hours
💰 *Total Cost:* ₹{cost:.2f}

Thank you for using our service! 🙏

*Vehicle Parking App* 🚀"""

        return self.send_message([phone_number], message) 