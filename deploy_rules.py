import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

def deploy_rules():
    """Deploy Firebase security rules from firebase.json file."""
    print("Deploying Firebase security rules...")
    
    # Check if already initialized
    try:
        app = firebase_admin.get_app()
    except ValueError:
        # Initialize Firebase Admin with service account
        cred = credentials.Certificate('serviceAccount.json')
        app = firebase_admin.initialize_app(cred)
    
    # Load rules from firebase.json
    try:
        with open('firebase.json', 'r') as f:
            firebase_config = json.load(f)
        
        rules = firebase_config.get('rules', {})
        
        # Construct rules string
        rules_string = 'rules_version = \'2\';\n\n'
        rules_string += 'service cloud.firestore {\n'
        
        # Add database rules
        if 'match /databases/{database}/documents' in str(rules):
            rules_string += '  ' + json.dumps(rules, indent=2)[1:-1].replace('\n', '\n  ')
        
        rules_string += '\n}'
        
        # Write rules to a temporary file
        with open('firestore.rules', 'w') as f:
            f.write(rules_string)
        
        # Deploy rules using Firebase CLI
        os.system('firebase deploy --only firestore:rules')
        
        print("✅ Security rules deployed successfully!")
        
    except Exception as e:
        print(f"❌ Error deploying rules: {str(e)}")

if __name__ == "__main__":
    deploy_rules() 