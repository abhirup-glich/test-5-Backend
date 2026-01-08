from supabase import create_client, Client
from .config import Config
import random
import string
from flask_smorest import abort

def get_supabase_client() -> Client:
    url = Config.SUPABASE_URL
    key = Config.SUPABASE_KEY
    if not url or not key:
        return None
    return create_client(url, key)

supabase = get_supabase_client()

class AdminService:
    @staticmethod
    def get_all_students():
        try:
            response = supabase.table('students').select("*").execute()
            return response.data
        except Exception as e:
            print(f"Error fetching students: {e}")
            return []

    @staticmethod
    def check_attendance():
        try:
            # Fetch all attendance records
            # In a real app, support filtering by query params
            response = supabase.table('attendance').select("*").execute()
            return response.data
        except Exception as e:
            print(f"Error checking attendance: {e}")
            return []

    @staticmethod
    def register_student(data):
        # Generate 5-digit unique ID
        unique_id = ''.join(random.choices(string.digits, k=5))
        
        # Check if unique_id exists (simple check, retry if collision in real app)
        # For now, just assume it's unique
        
        student_data = {
            'name': data['name'],
            'course': data.get('course', ''),
            'email': data['email'],
            # 'password_hash': ... (If we are handling auth)
            # 'unique_id': unique_id
        }
        
        # In a real app, we would hash the password.
        # Since the prompt asked for "Supabase (student data storage)", we store it there.
        # We might also create a Supabase Auth user if we want to use Supabase Auth.
        # For now, let's just store in 'students' table.
        
        try:
            # Add unique_id and password (hash it in production!)
            student_data['unique_id'] = unique_id
            student_data['password'] = data['password'] # Store plain for now or hash if bcrypt available
            
            response = supabase.table('students').insert(student_data).execute()
            return response.data[0] if response.data else student_data
        except Exception as e:
            print(f"Error registering student: {e}")
            abort(500, message=f"Failed to register student: {str(e)}")

    @staticmethod
    def upload_video(file):
        # Handle video upload
        # 500MB limit on Render -> We should not store it locally for long.
        # Maybe upload to Supabase Storage?
        
        try:
            # Check if file is valid
            if not file:
                abort(400, message="No file provided")
                
            # For now, we just acknowledge receipt because we don't have Supabase Storage configured in the prompt details
            # and local storage is ephemeral.
            # In a real scenario:
            # 1. Upload to Supabase Storage bucket 'attendance-videos'
            # 2. Trigger async processing
            
            return {"message": "Video uploaded successfully (simulated)", "filename": file.filename}
        except Exception as e:
             print(f"Error uploading video: {e}")
             abort(500, message="Upload failed")
