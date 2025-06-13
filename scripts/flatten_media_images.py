import os
import shutil

def flatten_media_images(media_root):
    """
    Move all image files from subdirectories in media_root to media_root directly.
    If a file with the same name exists, append a number suffix to avoid overwriting.
    """
    for root, dirs, files in os.walk(media_root, topdown=False):
        if root == media_root:
            # Skip the root directory itself
            continue
        for filename in files:
            src_path = os.path.join(root, filename)
            dest_path = os.path.join(media_root, filename)
            if os.path.exists(dest_path):
                # Find a new filename with suffix
                name, ext = os.path.splitext(filename)
                counter = 1
                while True:
                    new_filename = f"{name}_{counter}{ext}"
                    new_dest_path = os.path.join(media_root, new_filename)
                    if not os.path.exists(new_dest_path):
                        dest_path = new_dest_path
                        break
                    counter += 1
            shutil.move(src_path, dest_path)
        # After moving files, remove empty directories
        if not os.listdir(root):
            os.rmdir(root)

if __name__ == "__main__":
    # Adjust the media_root path as per your project setup
    media_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media')
    flatten_media_images(media_root)
    print(f"Flattened images in media directory: {media_root}")
