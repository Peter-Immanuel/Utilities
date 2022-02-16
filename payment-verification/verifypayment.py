import requests


class PaystackApiCall:
        def __init__(self):
                self.__base_url = f'https://api.paystack.co/'                   #paystack verification endpoint
                self.__secret_key = <paystack secret key>
                print("object instantiated....")

        def verify_payment(self, ref, *args, **kwargs):
                path = f'transaction/verify/{ref}'     #Url with transaction ref for verification
                verify_header = {
                        "Authorization": f"Bearer {self.__secret_key}",
                        "Content-Type":"application/json",
                }

                url = self.__base_url + path
                response = requests.get(url, headers=verify_header)

                if response.status_code == 200:
                        response_data=response.json()
                        # print(response_data)
                        return response_data['status'], response_data['data']
                
                response_data=response.json()
                return response_data['status'], response_data['data']

        
