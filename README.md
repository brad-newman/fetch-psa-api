
# PSA Card API Interaction Tool

## Overview
This Python application provides a convenient way to interact with the PSA Card API. It enables users to query the Professional Sports Authenticator (PSA) database via PSA Card's Public API for images and details of one or more certificate numbers.

## Features
- **User-friendly Image File Naming**: Renames fetched card images to the syntax "[Cert Number][-FRONT | -BACK].jpg", e.g. 79721014-FRONT.jpg.
- **Dual Grade Support**: Accommodates slabs with both card and auto grades.
- **API Integration with Token Authentication**: Facilitates seamless and secure communication with the PSA Card API.
- **CSV Ouput**: Stores retrieved card details in CSV format.

## Limitations
- **No DNA Certs Support**: The application only parses the PSACert object, not the DNACert object (which contains details for cards signed in-person or otherwise not in the original manufacturing process).
- **Only recent PSA cards have images**: PSA only started adding images to its certificate database in October 2021. I don't believe any cards graded before then will have images in the database. Any cert numbers that do not have corresponding images will still have its details populated into the `cert_details.csv` output file.

## Prerequisites
- Python 3.x installed on your machine.
- `requests` library installed (`pip install requests`).
- An active PSA Card API authorization token (details on obtaining this can be found in the [PSA Card API Documentation](https://www.psacard.com/publicapi/documentation)).

## Configuration
To configure the application, create a `config.json` file in the same directory as the script with your PSA API token:
```json
{
  "authorization_token": "YOUR_AUTH_TOKEN"
}
```
Replace `YOUR_AUTH_TOKEN` with your personal PSA Card API authorization token.

## Usage
Run the script using Python. Ensure the `config.json` file with your API token and a `certs.txt` file with the certificate number(s) are in place. The script will authenticate using your token and perform the operations on the certificate number(s).

## Contributing
If you're interested in contributing to this project, please fork the repository and submit your pull requests. We appreciate contributions that improve the functionality, add new features, or fix bugs. Make sure your code adheres to the project's coding standards.

## Disclaimer
This tool is an independent project and is not officially affiliated with PSA Card. It is developed to assist users in interacting with the PSA Card API more efficiently and in accordance with the [PSA API End User Agreement](https://www.psacard.com/publicapi).

## License
This project is licensed under the [MIT License](LICENSE).
