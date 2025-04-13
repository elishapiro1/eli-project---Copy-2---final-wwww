class User:
    """Base User class for all users in the system"""
    
    def __init__(self, uid, name, email, created_at=None):
        self.uid = uid
        self.name = name
        self.email = email
        self.created_at = created_at
        self._type = 'user'
    
    @property
    def is_admin(self):
        """Check if user is an admin"""
        return False
    
    def to_dict(self):
        """Convert user object to dictionary for session storage"""
        return {
            'uid': self.uid,
            'name': self.name,
            'email': self.email,
            'type': self._type,
            'is_admin': self.is_admin
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create user object from dictionary"""
        if data.get('type') == 'admin':
            return Admin(
                uid=data.get('uid'),
                name=data.get('name'),
                email=data.get('email'),
                created_at=data.get('created_at')
            )
        return User(
            uid=data.get('uid'),
            name=data.get('name'),
            email=data.get('email'),
            created_at=data.get('created_at')
        )
    
    @classmethod
    def from_firebase_user(cls, firebase_user, firestore_data=None):
        """Create user object from Firebase user and Firestore data"""
        if firestore_data and firestore_data.get('is_admin') is True:
            return Admin(
                uid=firebase_user.uid,
                name=firebase_user.display_name or firestore_data.get('name', ''),
                email=firebase_user.email,
                created_at=firestore_data.get('created_at')
            )
        
        return User(
            uid=firebase_user.uid,
            name=firebase_user.display_name or firestore_data.get('name', ''),
            email=firebase_user.email,
            created_at=firestore_data.get('created_at')
        )


class Admin(User):
    """Admin user with elevated privileges"""
    
    def __init__(self, uid, name, email, created_at=None):
        super().__init__(uid, name, email, created_at)
        self._type = 'admin'
    
    @property
    def is_admin(self):
        """Admin users always return True for is_admin"""
        return True
    
    # Admin-specific methods
    def can_manage_users(self):
        """Check if admin can manage users"""
        return True
    
    def can_manage_products(self):
        """Check if admin can manage products"""
        return True 