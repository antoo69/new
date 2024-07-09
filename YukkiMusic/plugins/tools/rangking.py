from pyrogram import Client, filters
from pyrogram.types import Message
import pymongo
from YukkiMusic import app

# Initialize MongoDB client
mongo_client = pymongo.MongoClient("mongodb+srv://ExposUbot:fadhil123@cluster0.d9v1xru.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Update with your MongoDB connection URI
mongo_db = mongo_client["typing_data"]  # Replace 'typing_data' with your database name
collection = mongo_db["typing_counts"]  # Collection name for storing typing counts


# Function to handle the /rangking command
@app.on_message(filters.command("rangking", prefixes="/"))
def ranking_command(client, message):
    # Get the chat ID where the command was issued
    chat_id = message.chat.id
    # Get the group name
    group_name = message.chat.title
    
    # Retrieve typing counts from MongoDB
    typing_data = collection.find_one({"chat_id": chat_id})
    
    if typing_data:
        # Get the top 10 members with the highest typing counts
        top_members = sorted(typing_data['counts'].items(), key=lambda x: x[1], reverse=True)[:10]
        
        if top_members:
            response = f"<b>Top 10 members typing in {group_name}</b>:\n"
            for idx, (user_id, count) in enumerate(top_members, start=1):
                user_info = client.get_users(user_id)
                username = user_info.username if user_info.username else user_info.first_name
                response += f"{idx}. @{username} - {count} jumlah typing\n"
        else:
            response = "No typing data available for this group."
    else:
        response = "No typing data available for this group."
    
    # Send the response
    message.reply_text(response)


# Function to handle user typing events
@app.on_message(filters.group & filters.text)
def handle_typing(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Exclude bot's typing
    if message.from_user.is_bot:
        return
    
    # Check if chat_id exists in MongoDB, create if not
    if not collection.find_one({"chat_id": chat_id}):
        collection.insert_one({"chat_id": chat_id, "counts": {}})
    
    # Increment typing count for user_id in MongoDB
    collection.update_one({"chat_id": chat_id}, {"$inc": {f"counts.{user_id}": 1}})
