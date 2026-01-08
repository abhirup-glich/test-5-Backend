from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import sys
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from ..services.audit_service import AuditService

# Add root directory to path to import Logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from Logic import logic
except ImportError:
    logic = None

legacy_bp = Blueprint('legacy', __name__)

ALLOWED_EXTENSIONS = {'webm', 'mp4', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    if logic:
        return logic.connect_db()
    return None, None

@legacy_bp.route('/api/identify', methods=['POST'])
def identify_student():
    try:
        data = request.json
        image_data = data.get('image')
        if not image_data:
            return jsonify({'status': 'error', 'message': 'No image data provided'}), 400
            
        conn, cur = logic.connect_db()
        result = logic.identify_student_web(cur, image_data)
        conn.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@legacy_bp.route('/api/students', methods=['GET'])
@jwt_required()
def get_students():
    if not logic:
        return jsonify({'error': 'Logic module not available'}), 500
    try:
        conn, cur = logic.connect_db()
        cur.execute("SELECT roll, name, course FROM students ORDER BY roll;")
        rows = cur.fetchall()
        students = [dict(row) for row in rows]
        conn.close()
        return jsonify({'students': students})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@legacy_bp.route('/api/check_attendance', methods=['GET'])
@jwt_required()
def check_attendance():
    if not logic:
        return jsonify({'error': 'Logic module not available'}), 500
    try:
        conn, cur = logic.connect_db()
        cur.execute("""
            SELECT s.roll, s.name, s.course, a.time, a.confidence 
            FROM attendance a
            JOIN students s ON a.roll = s.roll
            ORDER BY a.time DESC
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        attendance_list = []
        for row in rows:
            row_dict = dict(row)
            row_dict['time'] = row_dict['time'].isoformat() if row_dict['time'] else None
            attendance_list.append(row_dict)
            
        return jsonify({'attendance': attendance_list, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@legacy_bp.route('/api/upload', methods=['POST'])
@jwt_required()
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"attendance_{timestamp}.webm"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            conn, cur = logic.connect_db()
            result = logic.mark_attendance(cur, video_path=filepath)
            cur.close()
            conn.close()
            
            # Audit Log
            AuditService.log_action(get_jwt_identity(), "MARK_ATTENDANCE", {"status": result.get('status')})

            if result.get('status') == 'success':
                return jsonify({
                    'message': 'Attendance marked successfully',
                    'data': {
                        'name': result['name'],
                        'roll': result['roll'],
                        'time': result['time'],
                        'confidence': result['confidence']
                    }
                })
            else:
                return jsonify({
                    'status': result.get('status', 'error'),
                    'message': 'No students found' if result.get('status') == 'no_student' else result.get('error', 'Attendance not marked'),
                    'time': result.get('time')
                }), 200 if result.get('status') in ['no_student', 'no_face'] else 400
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'File type not allowed'}), 400

@legacy_bp.route('/api/register_student', methods=['POST'])
@jwt_required()
def register_student():
    try:
        data = request.json
        roll = data.get('roll')
        name = data.get('name')
        course = data.get('course')
        images = data.get('images')
        
        if not all([roll, name, course, images]):
            return jsonify({'error': 'Missing required fields'}), 400
            
        conn, cur = logic.connect_db()
        result = logic.register_student_web(cur, roll, name, course, images)
        conn.close()
        
        # Audit Log
        AuditService.log_action(get_jwt_identity(), "REGISTER_STUDENT", {"roll": roll, "name": name})

        if result['status'] == 'success':
            return jsonify(result)
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@legacy_bp.route('/api/students/<roll>', methods=['PUT'])
@jwt_required()
def update_student(roll):
    try:
        data = request.json
        conn, cur = logic.connect_db()
        success = logic.update_student_record(cur, roll, data.get('name'), data.get('course'))
        conn.close()
        
        AuditService.log_action(get_jwt_identity(), "UPDATE_STUDENT", {"roll": roll})

        if success:
            return jsonify({'status': 'success', 'message': 'Student updated'})
        else:
            return jsonify({'status': 'error', 'message': 'Update failed'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@legacy_bp.route('/api/students/<roll>', methods=['DELETE'])
@jwt_required()
def delete_student(roll):
    try:
        conn, cur = logic.connect_db()
        success = logic.delete_student_record(cur, roll)
        conn.close()
        
        AuditService.log_action(get_jwt_identity(), "DELETE_STUDENT", {"roll": roll})

        if success:
            return jsonify({'status': 'success', 'message': 'Student deleted'})
        else:
            return jsonify({'status': 'error', 'message': 'Delete failed'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
