# import os
# import requests

# # API credentials
# subscription_key = 'a1829fc096764059943acc4867cb6300'
# endpoint = 'https://sayali.cognitiveservices.azure.com/'

# # Define the OCR URL
# ocr_url = endpoint + "vision/v3.1/ocr"

# # Define directories (update these paths according to your actual directory structure)
# image_dir = "c:/Users/Shivani Malviya/API_Evaluation/images"
# groundtruth_dir = "c:/Users/Shivani Malviya/API_Evaluation/groundtruth"
# output_file = "c:/Users/Shivani Malviya/API_Evaluation/output.csv"

# # Function to call OCR API
# def extract_text_from_image(image_path):
#     try:
#         with open(image_path, "rb") as image_file:
#             image_data = image_file.read()
#         headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
#         params = {'language': 'unk', 'detectOrientation': 'true'}
#         response = requests.post(ocr_url, headers=headers, params=params, data=image_data)
#         response.raise_for_status()
#         analysis = response.json()
#         word_infos = [word["text"] for region in analysis["regions"] for line in region["lines"] for word in line["words"]]
#         return " ".join(word_infos)
#     except Exception as e:
#         print(f"Error extracting text from {image_path}: {e}")
#         return ""

# # Function to read ground truth text
# def extract_text_from_file(text_file):
#     try:
#         with open(text_file, 'r', encoding='utf-8') as file:
#             return file.read().strip()
#     except Exception as e:
#         print(f"Error reading ground truth from {text_file}: {e}")
#         return ""

# # Normalize text function (removes spaces)
# def normalize_text(text):
#     return ''.join(text.split())

# # List all image and text files
# try:
#     image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
#     text_files = sorted([f for f in os.listdir(groundtruth_dir) if f.lower().endswith('.txt')])

#     if len(image_files) != len(text_files):
#         raise Exception("The number of images and text files do not match.")

#     # Process each image and compare with ground truth
#     results = []
#     correct_count = 0
#     total_count = len(image_files)

#     for image_file in image_files:
#         image_path = os.path.join(image_dir, image_file)
#         text_file = os.path.join(groundtruth_dir, os.path.splitext(image_file)[0] + ".txt")
        
#         extracted_text_image = extract_text_from_image(image_path)
#         extracted_text_textfile = extract_text_from_file(text_file)
        
#         normalized_extracted_image = normalize_text(extracted_text_image)
#         normalized_extracted_textfile = normalize_text(extracted_text_textfile)
        
#         match_status = "correct" if normalized_extracted_image == normalized_extracted_textfile else "wrong"
#         if match_status == "correct":
#             correct_count += 1
        
#         results.append(f"{image_file},{extracted_text_textfile},{extracted_text_image},{match_status}")

#     # Write results to the output file
#     with open(output_file, 'w', encoding='utf-8') as f:
#         f.write("filename,expected,predicted,correct/wrong\n")
#         f.write("\n".join(results))

#     # Calculate accuracy
#     accuracy = correct_count / total_count * 100 

#     # Print summary
#     print(f"Total images: {total_count}")
#     print(f"Correctly recognized: {correct_count}")
#     print(f"Wrongly recognized: {total_count - correct_count}")
#     print(f"Accuracy: {accuracy:.2f}%")

# except Exception as ex:
#     print(f"An error occurred: {ex}")

import os
import requests

# API credentials
subscription_key = 'a1829fc096764059943acc4867cb6300'
endpoint = 'https://sayali.cognitiveservices.azure.com/'
ocr_url = endpoint + "vision/v3.1/ocr"

# Directories
image_dir = "c:/Users/Shivani Malviya/API_Evaluation/images"
groundtruth_dir = "c:/Users/Shivani Malviya/API_Evaluation/groundtruth"
output_file = "c:/Users/Shivani Malviya/API_Evaluation/output.csv"

# Function to call OCR API
def extract_text_from_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
        params = {'language': 'unk', 'detectOrientation': 'true'}
        response = requests.post(ocr_url, headers=headers, params=params, data=image_data)
        response.raise_for_status()
        analysis = response.json()
        word_infos = [word["text"] for region in analysis["regions"] for line in region["lines"] for word in line["words"]]
        return " ".join(word_infos)
    except Exception as e:
        print(f"Error extracting text from {image_path}: {e}")
        return ""

# Function to read ground truth text
def extract_text_from_file(text_file):
    try:
        with open(text_file, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading ground truth from {text_file}: {e}")
        return ""

# Normalize text function
def normalize_text(text):
    return ''.join(text.split())

try:
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    text_files = sorted([f for f in os.listdir(groundtruth_dir) if f.lower().endswith('.txt')])

    if len(image_files) != len(text_files):
        raise Exception("The number of images and text files do not match.")

    correct_count = 0
    total_count = len(image_files)

    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        text_file = os.path.join(groundtruth_dir, os.path.splitext(image_file)[0] + ".txt")
        
        extracted_text_image = extract_text_from_image(image_path)
        extracted_text_textfile = extract_text_from_file(text_file)
        
        normalized_extracted_image = normalize_text(extracted_text_image)
        normalized_extracted_textfile = normalize_text(extracted_text_textfile)
        
        if normalized_extracted_image == normalized_extracted_textfile:
            correct_count += 1

    accuracy = (correct_count / total_count) * 100 

    # Print summary
    print(f"Total images: {total_count}")
    print(f"Correctly recognized: {correct_count}")
    print(f"Wrongly recognized: {total_count - correct_count}")
    print(f"Accuracy: {accuracy:.2f}%")

except Exception as ex:
    print(f"An error occurred: {ex}")
