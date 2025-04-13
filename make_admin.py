import firebase_admin
from firebase_admin import credentials, firestore, auth
import sys
from models import User, Admin

def make_user_admin(email):
    """
    Makes a user with the given email an admin.
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
    
    try:
        # Find user by email
        firebase_user = auth.get_user_by_email(email)
        user_id = firebase_user.uid
        
        print(f"Found user: {firebase_user.display_name} ({firebase_user.email})")
        
        # Get user data from Firestore
        user_ref = db.collection('users').document(user_id)
        doc = user_ref.get()
        
        if doc.exists:
            # Create User object
            firestore_data = doc.to_dict()
            user = User.from_firebase_user(firebase_user, firestore_data)
            
            # Elevate to Admin
            admin = Admin(
                uid=user.uid,
                name=user.name,
                email=user.email,
                created_at=user.created_at
            )
            
            # Update Firestore
            user_ref.update({
                'is_admin': True
            })
            
            print(f"✅ User {email} is now an admin!")
            print(f"   Type: {admin._type}")
            print(f"   Is Admin: {admin.is_admin}")
        else:
            print(f"⚠️ Warning: User exists in Authentication but not in Firestore.")
            print(f"   Creating user document in Firestore...")
            
            # Create admin document
            user_ref.set({
                'name': firebase_user.display_name or email.split('@')[0],
                'email': email,
                'is_admin': True,
                'created_at': firestore.SERVER_TIMESTAMP
            })
            
            print(f"✅ Created admin user in Firestore!")
            
    except auth.UserNotFoundError:
        print(f"❌ Error: User with email {email} not found.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python make_admin.py <user_email>")
        sys.exit(1)
    
    email = sys.argv[1]
    make_user_admin(email) 