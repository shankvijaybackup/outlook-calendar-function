import requests
import datetime

def create_out_of_office_event(email, start_time, end_time, subject, access_token):
    # Parse and adjust start and end times for all-day events (midnight time)
    start_datetime = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")  # Include time parsing
    end_datetime = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")  # Include time parsing
    
    # Adjust start time to midnight UTC on the start date
    start_time_adjusted = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Adjust end time to midnight UTC on the next day (end of the day)
    end_time_adjusted = (end_datetime + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    # Format to ISO 8601 string (date only for all-day events)
    start_time_str = start_time_adjusted.isoformat()
    end_time_str = end_time_adjusted.isoformat()

    # Define the event payload
    event_data = {
        "subject": subject,
        "start": {
            "dateTime": start_time_str,
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": end_time_str,
            "timeZone": "UTC"
        },
        "isAllDay": True
    }

    # Create the event using Microsoft Graph API
    url = f"https://graph.microsoft.com/v1.0/users/{email}/events"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=event_data, headers=headers)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create out-of-office event: {response.text}")
    
    return response.json()

import requests
import datetime

def set_automatic_replies(email, start_time, end_time, access_token):
    url = f"https://graph.microsoft.com/v1.0/users/{email}/mailboxSettings/automaticRepliesSetting"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Format the start and end times in ISO 8601 format
    start_time_adjusted = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S").isoformat()
    end_time_adjusted = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S").isoformat()

    # Payload to set automatic replies
    data = {
        "status": "alwaysEnabled",  # Set as alwaysEnabled for out-of-office
        "externalAudience": "all",  # Or "none" or "limited"
        "internalReplyMessage": "I am currently out of the office. I will return on [Date].",
        "externalReplyMessage": "I am currently out of the office and will not be available until [Date].",
        "scheduledStartDateTime": {
            "dateTime": start_time_adjusted,
            "timeZone": "UTC"
        },
        "scheduledEndDateTime": {
            "dateTime": end_time_adjusted,
            "timeZone": "UTC"
        }
    }

    # Send the PATCH request
    response = requests.patch(url, json=data, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to set automatic replies: {response.text}")
    
    return response.json()