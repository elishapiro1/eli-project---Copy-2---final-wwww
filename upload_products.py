import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# Initialize Firebase Admin with your service account
cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# Products from the user's store
products = [
    # Soccer Balls
    {
        "name": "Adidas Pro Ball",
        "description": "Official match ball for professional leagues, top performance",
        "price": 29.99,
        "category": "Soccer Balls",
        "image_url": "https://example.com/adidas-pro-ball.jpg",
        "stock": 35,
        "brand": "Adidas",
        "created_at": firestore.SERVER_TIMESTAMP
    },
    {
        "name": "Nike Lal",
        "description": "Professional training soccer ball with enhanced durability",
        "price": 19.99,
        "category": "Soccer Balls",
        "image_url": "https://example.com/nike-lal.jpg",
        "stock": 42,
        "brand": "Nike",
        "created_at": firestore.SERVER_TIMESTAMP
    },
    
    # Clothing
    {
        "name": "GO-FC Academy Jersey",
        "description": "Youth training jersey with moisture wicking material",
        "price": 24.99,
        "category": "Clothing",
        "image_url": "https://example.com/gofc-jersey.jpg",
        "stock": 50,
        "brand": "GO-FC",
        "created_at": firestore.SERVER_TIMESTAMP
    },
    {
        "name": "Tec-22 Jersey",
        "description": "Professional match jersey with advanced cooling technology",
        "price": 34.99,
        "category": "Clothing",
        "image_url": "https://example.com/tec22-jersey.jpg",
        "stock": 30,
        "brand": "Tec-22",
        "created_at": firestore.SERVER_TIMESTAMP
    },
    
    # Protective Gear
    {
        "name": "Nike/Adidas Shin Guards",
        "description": "Professional grade shin guards for maximum protection",
        "price": 19.99,
        "category": "Protective Gear",
        "image_url": "https://example.com/shin-guards.jpg",
        "stock": 65,
        "brand": "Nike/Adidas",
        "created_at": firestore.SERVER_TIMESTAMP
    },
    {
        "name": "Predator Pro Gloves",
        "description": "Professional goalkeeper gloves with grip control",
        "price": 29.99,
        "category": "Protective Gear",
        "image_url": "https://example.com/predator-gloves.jpg",
        "stock": 40,
        "brand": "Predator",
        "created_at": firestore.SERVER_TIMESTAMP
    },
    
    # Shoes
    {
        "name": "Nike/Adlid Superfly",
        "description": "Speed optimized cleats for explosive performance",
        "price": 99.99,
        "category": "Shoes",
        "image_url": "https://example.com/superfly.jpg",
        "stock": 25,
        "brand": "Nike",
        "created_at": firestore.SERVER_TIMESTAMP
    },
    {
        "name": "Predator Accuracy",
        "description": "Professional cleats with enhanced ball control and touch",
        "price": 109.99,
        "category": "Shoes",
        "image_url": "https://example.com/predator-accuracy.jpg",
        "stock": 20,
        "brand": "Predator",
        "created_at": firestore.SERVER_TIMESTAMP
    },
    
    # Accessories
    {
        "name": "Ball Pump",
        "description": "Durable hand pump with needle for quick ball inflation",
        "price": 9.99,
        "category": "Accessories",
        "image_url": "https://example.com/ball-pump.jpg",
        "stock": 100,
        "brand": "Generic",
        "created_at": firestore.SERVER_TIMESTAMP
    },
    {
        "name": "Shoe Bag",
        "description": "Water-resistant bag for storing cleats and equipment",
        "price": 14.99,
        "category": "Accessories",
        "image_url": "https://example.com/shoe-bag.jpg",
        "stock": 85,
        "brand": "Generic",
        "created_at": firestore.SERVER_TIMESTAMP
    },
    
    # Team Merchandise
    {
        "name": "Club Scarf",
        "description": "Official team supporter scarf with club colors",
        "price": 19.99,
        "category": "Team Merchandise",
        "image_url": "https://example.com/club-scarf.jpg",
        "stock": 60,
        "brand": "Club Official",
        "created_at": firestore.SERVER_TIMESTAMP
    },
    {
        "name": "Team Backpack",
        "description": "Official club backpack for storing gear and equipment",
        "price": 39.99,
        "category": "Team Merchandise",
        "image_url": "https://example.com/team-backpack.jpg",
        "stock": 45,
        "brand": "Club Official",
        "created_at": firestore.SERVER_TIMESTAMP
    },
    
    # Training Equipment
    {
        "name": "Agility Ladder",
        "description": "Training ladder for footwork and agility drills",
        "price": 24.99,
        "category": "Training Equipment",
        "image_url": "https://example.com/agility-ladder.jpg",
        "stock": 30,
        "brand": "Training Pro",
        "created_at": firestore.SERVER_TIMESTAMP
    },
    {
        "name": "Resistance Bands",
        "description": "Set of progressive resistance bands for strength training",
        "price": 19.99,
        "category": "Training Equipment",
        "image_url": "https://example.com/resistance-bands.jpg",
        "stock": 50,
        "brand": "Training Pro",
        "created_at": firestore.SERVER_TIMESTAMP
    }
]

def upload_products():
    # Reference to products collection
    products_ref = db.collection('products')
    
    # Upload each product
    for product in products:
        try:
            # Add product to Firestore
            doc_ref = products_ref.add(product)
            print(f"Added product: {product['name']} with ID: {doc_ref[1].id}")
        except Exception as e:
            print(f"Error adding product {product['name']}: {e}")

if __name__ == "__main__":
    print("Starting product upload...")
    upload_products()
    print("Product upload completed!") 