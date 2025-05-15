
import cloudinary
import cloudinary.uploader
import cloudinary.api

def test_upload():
    # Configure Cloudinary with your credentials
    cloudinary.config(
        cloud_name='dlapbhavc',  # Replace with your cloud name
        api_key='837941825354552',  # Replace with your API key
        api_secret='SnwE8QAwc_LE-jz5hDlS922DrXM'  # Replace with your API secret
    )

    # Upload a sample file (a small text file)
    try:
        response = cloudinary.uploader.upload("sample.txt", resource_type="raw")
        print("Upload successful!")
        print("URL:", response.get("secure_url"))
    except Exception as e:
        print("Upload failed:", e)

if __name__ == "__main__":
    # Create a sample file to upload
    with open("sample.txt", "w") as f:
        f.write("This is a test file for Cloudinary upload.")

    test_upload()
