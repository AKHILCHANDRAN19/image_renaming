import os
import shutil

# --- Configuration ---
# The script will use these folder paths. They match your request.
SOURCE_FOLDER = "/storage/emulated/0/Datasets"
DESTINATION_FOLDER = "/storage/emulated/0/Datasets/sketch"

# --- Main Script Logic ---

def rename_and_move_images():
    """
    Finds all images in the source folder, asks the user for renaming
    parameters, and then renames and moves the images to the destination folder.
    """
    print("--- Image Renaming and Moving Script ---")

    # 1. Check if the source folder exists
    if not os.path.isdir(SOURCE_FOLDER):
        print(f"\n[ERROR] Source folder not found: {SOURCE_FOLDER}")
        print("Please make sure the 'core' folder exists and you have granted storage permissions.")
        return

    # 2. Find all image files in the source folder
    # You can add more extensions here if needed (e.g., '.gif', '.webp')
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
    try:
        all_files = os.listdir(SOURCE_FOLDER)
        image_files = [f for f in all_files if f.lower().endswith(image_extensions)]
    except PermissionError:
        print(f"\n[ERROR] Permission denied to read from {SOURCE_FOLDER}.")
        print("Please ensure your script has storage access permissions.")
        return

    if not image_files:
        print(f"\n[INFO] No image files found in {SOURCE_FOLDER}. Nothing to do.")
        return

    print(f"\nFound {len(image_files)} image(s) in the '{os.path.basename(SOURCE_FOLDER)}' folder.")

    # 3. Get valid user input for start and end names
    while True:
        try:
            start_name = input("Enter the start name of the image (e.g., 1.png): ")
            end_name = input("Enter the end name of the image (e.g., 10.png): ")

            # Extract number and extension from the start name
            start_num_str, extension = os.path.splitext(start_name)
            start_num = int(start_num_str)

            # Extract number from the end name
            end_num_str, _ = os.path.splitext(end_name)
            end_num = int(end_num_str)

            if start_num > end_num:
                print("[ERROR] The start number cannot be greater than the end number. Please try again.")
                continue
            
            if not extension:
                print("[ERROR] You must provide a file extension in the start name (e.g., '.png' or '.jpg').")
                continue

            break # Exit the loop if input is valid

        except ValueError:
            print("[ERROR] Invalid input. Please enter names in the format 'number.extension' (e.g., 1.png).")
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred during input: {e}")

    # 4. Check if we have enough images to rename
    num_requested = end_num - start_num + 1
    num_available = len(image_files)

    if num_requested > num_available:
        print(f"\n[WARNING] You requested to rename {num_requested} images, but only {num_available} are available.")
        # Adjust the end number to only rename the available files
        end_num = start_num + num_available - 1
        print(f"The script will rename the {num_available} available images from {start_num}{extension} to {end_num}{extension}.")
    
    # 5. Create the destination directory if it doesn't exist
    try:
        os.makedirs(DESTINATION_FOLDER, exist_ok=True)
        print(f"\nFiles will be saved in: {DESTINATION_FOLDER}")
    except OSError as e:
        print(f"\n[ERROR] Could not create destination folder. Reason: {e}")
        return

    # 6. Rename and move the files
    print("\nStarting the renaming process...")
    processed_count = 0
    current_number = start_num

    # We iterate through the available image files, renaming them sequentially
    for i in range(num_available):
        # Stop if we've processed all the files up to the (possibly adjusted) end number
        if current_number > end_num:
            break

        old_filename = image_files[i]
        new_filename = f"{current_number}{extension}"

        source_path = os.path.join(SOURCE_FOLDER, old_filename)
        destination_path = os.path.join(DESTINATION_FOLDER, new_filename)

        try:
            # shutil.move() renames and moves the file in one step
            shutil.move(source_path, destination_path)
            print(f"  Moved and renamed '{old_filename}' -> '{new_filename}'")
            processed_count += 1
            current_number += 1
        except Exception as e:
            print(f"  [ERROR] Could not process '{old_filename}'. Reason: {e}")

    print(f"\n--- Process Complete ---")
    print(f"Successfully renamed and moved {processed_count} images.")

# This line ensures the script runs when you execute the file
if __name__ == "__main__":
    rename_and_move_images()
