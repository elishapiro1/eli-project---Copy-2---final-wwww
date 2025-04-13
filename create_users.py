import firebase_admin
from firebase_admin import credentials, firestore, auth
import sys
from models import User, Admin

def create_test_users():
    """
    Creates test users of different types for demonstration
    """
    # Check if already initialized
    try:
        app = firebase_admin.get_app()
    except ValueError:
        # Initialize Firebase Admin with service account
        cred = credentials.Certificate('serviceAccount.json')
        app = firebase_admin.initialize_app(cred)
    
    # Get Firestore client
    db = firestore.client()
    
    # Test data
    users_data = [
        {
            "email": "regular@example.com",
            "password": "password123",
            "name": "Regular User",
            "is_admin": False
        },
        {
            "email": "admin@example.com",
            "password": "admin123",
            "name": "Admin User",
            "is_admin": True
        }
    ]
    
    created_users = []
    
    for user_data in users_data:
        try:
            # Check if user already exists
            try:
                existing_user = auth.get_user_by_email(user_data["email"])
                print(f"User {user_data['email']} already exists. Skipping creation.")
                continue
            except auth.UserNotFoundError:
                # User doesn't exist, create new one
                pass
            
            # Create user in Firebase Authentication
            user_record = auth.create_user(
                email=user_data["email"],
                password=user_data["password"],
                display_name=user_data["name"]
            )
            
            # Create user model object
            if user_data["is_admin"]:
                user_obj = Admin(
                    uid=user_record.uid,
                    name=user_data["name"],
                    email=user_data["email"]
                )
            else:
                user_obj = User(
                    uid=user_record.uid,
                    name=user_data["name"],
                    email=user_data["email"]
                )
            
            # Store in Firestore
            db.collection('users').document(user_record.uid).set({
                'name': user_data["name"],
                'email': user_data["email"],
                'is_admin': user_data["is_admin"],
                'created_at': firestore.SERVER_TIMESTAMP
            })
            
            created_users.append({
                'uid': user_record.uid,
                'email': user_data["email"],
                'name': user_data["name"],
                'is_admin': user_data["is_admin"],
                'type': user_obj._type
            })
            
            print(f"✅ Created {user_obj._type}: {user_data['name']} ({user_data['email']})")
            
        except Exception as e:
            print(f"❌ Error creating user {user_data['email']}: {str(e)}")
    
    print("\nCreated Users Summary:")
    for user in created_users:
        print(f"  - {user['name']} ({user['email']})")
        print(f"    UID: {user['uid']}")
        print(f"    Type: {user['type']}")
        print(f"    Admin: {user['is_admin']}")
        print()

if __name__ == "__main__":
    create_test_users() 