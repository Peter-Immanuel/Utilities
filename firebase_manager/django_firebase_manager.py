from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice

class FireBasePushNotificationManager:
    
    def __init__(self):
        pass
    
    def get_user_device(self, user: object) -> FCMDevice:
        return FCMDevice.objects.filter(
            user=user).all()
        
    def send_data_push_notification(self, user: object, record: dict):
        devices: FCMDevice = self.get_user_device(user)
        
        result = {
            "successful_push":list(),
            "unsuccessful_push":list()
        }
        for device in devices:
            message = Message(
                notification=Notification(
                    title=record.get("school_name", "SVAA"), 
                    body=record.get("details"),
                ),
                data=record
            )

            try:
                response = device.send_message(message)
                _dict = response.__dict__
                _dict["device"] = device.registration_id
                result["successful_push"].append(_dict)
            except Exception as e:
                result["unsuccessful_push"].append({
                    "device":device.registration_id,
                    "error":str(e)}
                )
                continue
            
        return result
            
    def send_push_notification(self, user: object, title: str, body: str):
        devices: FCMDevice = self.get_user_device(user)
        
        result = {
            "successful_push":list(),
            "unsuccessful_push":list()
        }
        for device in devices:
            message = Message(
                notification=Notification(title=title,body=body),
            )
            try:
                response = device.send_message(message)
                _dict = response.__dict__
                _dict["device"] = device.registration_id
                result["successful_push"].append(_dict)
            except Exception as e:
                result["unsuccessful_push"].append({
                    "device":device.registration_id,
                    "error":str(e)}
                )
                continue
            
        return result
    
    
    
    
    