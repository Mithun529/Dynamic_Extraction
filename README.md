# Dynamic_Extraction
This project is a Data Extraction Tool that supports Web Scraping and Database Interaction through an intuitive interface. The frontend is built with HTML, CSS, and JavaScript for a clean and simple design, offering two primary functionalities:
## Features:
1. <b>Web Scraping:</b>
Allows users to input a URL and an optional search term to extract tabular data from websites.
Displays the extracted data in a structured table format with the option to download it as a CSV file.
2. <b>Database Interaction:</b>
Enables dynamic MySQL database connections by providing credentials (host, user, password, database name).
Fetches data from a user-specified table and renders it on the page.
Allows downloading the table data as a CSV file.
## How It Works:
1. <b>Choose an option:</b>
Select either "Web Scraping" or "Database Interaction."
2. <b> Fill in the form:</b>
Provide the required details based on the selected option.
3. <b>Submit:</b>
Click the button to display the extracted data and download it as needed.
<br><br>
The backend uses FastAPI to handle API requests, and the frontend interacts with it via AJAX.

