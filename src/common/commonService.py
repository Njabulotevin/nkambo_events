from supabase import create_client, Client
import os

# Initialize Supabase client
url = os.getenv("SUPABASE_URL")  # Replace with your Supabase URL
key = os.getenv("SUPABASE_KEY")  # Replace with your Supabase API Key
supabase: Client = create_client(url, key)





def upload_to_supabase(file, filename:str, type:str ):
    try:
        bucket_name = os.getenv("BUCKET_NAME")
        file_name = filename.replace(" ", "_").lower() +"_cover_image"

        # Upload the file to Supabase Storage
        storage = supabase.storage
        response = storage.from_(bucket_name).upload(file_name, file, {"content-type": type, "x-upsert": "true"})
        print(response)
        return response
    except Exception as e:
        print(e)
        return None

def get_file_from_supabase(filename):
    try:
        bucket_name = os.getenv("BUCKET_NAME")
        storage = supabase.storage
        public_url = storage.from_(bucket_name).get_public_url(filename)
        return public_url
    except Exception as e:
        print(e)
        return None





