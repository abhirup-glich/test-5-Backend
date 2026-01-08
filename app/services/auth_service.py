from ..extensions import bcrypt
from ..models.user import UserModel
from flask_jwt_extended import create_access_token
from flask import abort
import random
import string

class AuthService:
    otp_store = {}

    @staticmethod
    def register_user(data):
        # Check if email exists
        if UserModel.get_by_email(data['email']):
            abort(409, message="Email already exists")
            
        # Check if unique_id exists
        if UserModel.get_by_unique_id(data['unique_id']):
            abort(409, message="Unique ID already exists")

        # Hash password
        password = data.pop('password')
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        data['password_hash'] = password_hash
        
        # Create user
        user = UserModel.create(data)
        if not user:
            abort(500, message="Failed to create user")
            
        return user

    @staticmethod
    def login_user(email, password):
        user = UserModel.get_by_email(email)
        if not user or not bcrypt.check_password_hash(user['password_hash'], password):
            abort(401, message="Invalid credentials")
            
        access_token = create_access_token(identity=user['id'])
        return {
            'access_token': access_token,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'course': user['course'],
                'unique_id': user['unique_id']
            }
        }

    @staticmethod
    def init_admin_login(email):
        # Generate 6-digit OTP
        otp = ''.join(random.choices(string.digits, k=6))
        
        # Store it
        AuthService.otp_store[email] = otp
        
        # Send it (Simulated log)
        print(f"============================================")
        print(f"OTP for {email} (sent to frostbyteserviceandco@gmail.com): {otp}")
        print(f"============================================")
        
        return {"message": "OTP sent"}

    @staticmethod
    def verify_admin_login(email, password, otp):
        stored_otp = AuthService.otp_store.get(email)
        if not stored_otp or stored_otp != otp:
            abort(401, message="Invalid OTP")
            
        # Clear OTP
        if email in AuthService.otp_store:
            del AuthService.otp_store[email]
            
        # Verify Password
        user = UserModel.get_by_email(email)
        if not user or not bcrypt.check_password_hash(user['password_hash'], password):
             abort(401, message="Invalid credentials")

        access_token = create_access_token(identity=user['id'])
        return {
            'access_token': access_token,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'course': user['course'],
                'unique_id': user['unique_id']
            }
        }

    @staticmethod
    def change_password(user_id, old_password, new_password):
        user = UserModel.get_by_id(user_id)
        if not user:
            abort(404, message="User not found")
            
        if not bcrypt.check_password_hash(user['password_hash'], old_password):
            abort(401, message="Invalid old password")
            
        new_password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        UserModel.update_password(user_id, new_password_hash)
        return {"message": "Password updated successfully"}
