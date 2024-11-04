from pymongo import MongoClient

# uri = "mongodb+srv://laphv494:oS4tGn8sR9v5oKqh@agrichatbot.c2z5m.mongodb.net/?retryWrites=true&w=majority&appName=AgriChatbot"
# mongodb+srv://vohoanglam2211:22112004@cluster0.ju9rk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
def check_account_credentials(username, password):
    uri = "mongodb+srv://laphv494:oS4tGn8sR9v5oKqh@agrichatbot.c2z5m.mongodb.net/?retryWrites=true&w=majority&appName=AgriChatbot"
    client = MongoClient(uri)
    db = client['chatbot']
    collection = db['account']
    user_document = collection.find_one({"user": username})
    client.close()
    if user_document and user_document.get("pass") == password:
        return True 

def account_exists(username):
    uri = "mongodb+srv://laphv494:oS4tGn8sR9v5oKqh@agrichatbot.c2z5m.mongodb.net/?retryWrites=true&w=majority&appName=AgriChatbot"
    client = MongoClient(uri)
    db = client['chatbot']
    collection = db['account']
    existing_user = collection.find_one({"user": username})
    client.close()
    return existing_user is not None

def add_account(username,password):
    uri = "mongodb+srv://laphv494:oS4tGn8sR9v5oKqh@agrichatbot.c2z5m.mongodb.net/?retryWrites=true&w=majority&appName=AgriChatbot"
    client = MongoClient(uri)
    db = client['chatbot']
    collection = db['account']  
    new_document = {
        "user": username,
        "pass": password,
    }
    insert_result = collection.insert_one(new_document)
    print("Inserted document ID:", insert_result.inserted_id)
    client.close()
