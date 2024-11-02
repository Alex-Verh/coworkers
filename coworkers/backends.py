# from django.contrib.auth.backends import ModelBackend
# from .models import CustomUser 


# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             user = CustomUser.objects.get(email=username)
#             if user.check_password(password):
#                 print("Authentication successful")
#                 return user
#             else:
#                 print("Password mismatch")
#         except CustomUser.DoesNotExist:
#             print("User does not exist")
#         return None