from pymongo import MongoClient
def check_account_credentials(username, password):
    uri = "mongodb+srv://vohoanglam2211:22112004@cluster0.ju9rk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    db = client['chatbot']
    collection = db['account']
    user_document = collection.find_one({"user": username})
    client.close()
    if user_document and user_document.get("pass") == password:
        return True 

def account_exists(username):
    uri = "mongodb+srv://vohoanglam2211:22112004@cluster0.ju9rk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    db = client['chatbot']
    collection = db['account']
    existing_user = collection.find_one({"user": username})
    client.close()
    return existing_user is not None

def add_account(username,password):
    uri = "mongodb+srv://vohoanglam2211:22112004@cluster0.ju9rk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    db = client['chatbot']
    collection = db['account']  
    new_account = {
        "user": username,
        "pass": password,
    }
    insert_result = collection.insert_one(new_account)
    client.close()
