# jinka/api/main.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from common.py.webscrape_service import perform_search_with_selenium, scrape_and_parse_html, save_data_to_csv
from common.py.database_service import fetch_data_from_mysql
import os

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific URLs for security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scrape")
async def scrape_data(url: str, search_term: str = Query(None)):
    html_content = perform_search_with_selenium(url, search_term)

    if html_content:
        headers, data = scrape_and_parse_html(html_content)
        if data:
            # Save data to CSV file
            csv_filename = save_data_to_csv(headers, data)

            # Return the data and CSV filename to frontend
            return {
                "message": "Data scraped successfully",
                "headers": headers,
                "data": data,
                "csv_file": f"/download_csv/{csv_filename}"
            }
        else:
            raise HTTPException(status_code=404, detail="No data found in the table")
    else:
        raise HTTPException(status_code=500, detail="Failed to retrieve content")


@app.get("/mysql_data")
async def get_mysql_data(db_host: str, db_user: str, db_password: str, db_name: str, table_name: str):
    result = fetch_data_from_mysql(db_host, db_user, db_password, db_name, table_name)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@app.get("/download_csv/{csv_filename}")
async def download_csv(csv_filename: str):
    file_path = f"./{csv_filename}"
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=csv_filename, media_type="text/csv")
    else:
        raise HTTPException(status_code=404, detail="CSV file not found")
