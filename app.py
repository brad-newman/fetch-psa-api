
import requests
import os
import csv
import json
from collections import OrderedDict

# Load the config file containing the authorization token you generated at https://www.psacard.com/publicapi/documentation
def load_config():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config
config = load_config()
authorization_token = config['authorization_token']

# Use 'authorization_token' in your headers
headers = {
    "authorization": f"bearer {authorization_token}"
}

# Open the file containing the cert numbers (one per line)
with open('certs.txt', 'r') as file:
    cert_numbers = [int(line.strip()) for line in file if line.strip()]

def download_images(cert_numbers):
    # Ensure the 'card-images' subfolder exists
    if not os.path.exists('card-images'):
        os.makedirs('card-images')
    for cert_number in cert_numbers:
        cert_url = "https://api.psacard.com/publicapi/cert/GetImagesByCertNumber/{cert_number}"
        print(cert_url.format(cert_number=cert_number))
        json_response = requests.get(cert_url.format(cert_number=cert_number), headers=headers)
        print(json_response)
        if json_response.status_code == 200:
            json_response = json_response.json()
            for item in json_response:
                image_url = item['ImageURL']
                print
                isFront = item['IsFrontImage']
                if isFront:
                    image_name = os.path.join('card-images', str(cert_number) + '-FRONT.jpg')
                else:
                    image_name = os.path.join('card-images', str(cert_number) + '-BACK.jpg')
                # Download and save the image
                json_response = requests.get(image_url)
                with open(image_name, 'wb') as file:
                    file.write(json_response.content)
        else:
            print(f"Error: {json_response.status_code}")

def fetch_details(cert_numbers):
    for cert_number in cert_numbers:
        certDetails_url = f"https://api.psacard.com/publicapi/cert/GetByCertNumber/{cert_number}"
        response = requests.get(certDetails_url.format(cert_number=cert_number), headers=headers)
        print(response)
        if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type', ''):
            response = response.json()
            parse_and_save_to_csv(response)       
            print(response)
        else:
            print(f"Error: {response.status_code}")
        
def parse_and_save_to_csv(response):
    # Ensure the 'card-details' subfolder exists
    if not os.path.exists('card-details'):
        os.makedirs('card-details')
    # Define the CSV file name
    csv_file = 'card-details/cert_details.csv'
    # Extract the 'PSACert' dictionary
    psa_cert = response.get('PSACert', {})
    # If 'IsDualCert' is False, add the additional keys with value "N/A"
    if not psa_cert.get('IsDualCert', False):
        psa_cert['CardGrade'] = "N/A"
        psa_cert['PrimarySigners'] = "N/A"
        psa_cert['AutographGrade'] = "N/A"
    # Create an ordered dictionary with the keys in the desired order
    ordered_keys = list(psa_cert.keys())
    for key in ['PrimarySigners', 'AutographGrade']:
        ordered_keys.remove(key)
        ordered_keys.insert(ordered_keys.index('CardGrade') + 1, key)
    ordered_psa_cert = OrderedDict((k, psa_cert[k]) for k in ordered_keys)
    # Check if the CSV file already exists
    file_exists = os.path.isfile(csv_file)
    # Open the CSV file in append mode
    with open(csv_file, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=ordered_psa_cert.keys())
        # If the file didn't exist before, write the header
        if not file_exists:
            writer.writeheader()
        # Write the data
        writer.writerow(ordered_psa_cert)
        
if __name__ == '__main__':
    download_images(cert_numbers)
    fetch_details(cert_numbers)