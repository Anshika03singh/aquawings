import cv2
import os

def images_to_video(image_folder, output_video, fps=30):
    images = [img for img in os.listdir(image_folder) if img.endswith((".png", ".jpg", ".jpeg"))]
    images.sort()  # Ensure images are in the correct order
    
    if not images:
        print("No images found in the specified folder.")
        return
    
    # Read the first image to get dimensions
    first_image = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = first_image.shape
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)
    
    video.release()
    print(f"Video saved as {output_video}")

# Example usage
image_folder = "imgtovideo"  # Replace with your folder path
output_video = "output_video.mp4"
images_to_video(image_folder, output_video, fps=1)
