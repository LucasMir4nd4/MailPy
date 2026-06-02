import requests






# class ZendeskAPI:
#     def __init__(self, subdomain, email, api_token):
#         self.subdomain = subdomain
#         self.email = email
#         self.api_token = api_token
#         self.base_url = f"https://{subdomain}.zendesk.com/api/v2"

#     def _get_auth(self):
#         return (f"{self.email}/token", self.api_token)

#     def get_tickets(self):
#         url = f"{self.base_url}/tickets.json"
#         response = requests.get(url, auth=self._get_auth())
#         response.raise_for_status()
#         return response.json()

#     def create_ticket(self, subject, description):
#         url = f"{self.base_url}/tickets.json"
#         data = {
#             "ticket": {
#                 "subject": subject,
#                 "description": description
#             }
#         }
#         response = requests.post(url, json=data, auth=self._get_auth())
#         response.raise_for_status()
#         return response.json()