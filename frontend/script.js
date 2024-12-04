// Handle option change
document.getElementById("option").addEventListener("change", function () {
    const option = this.value;
    document.getElementById("webscrapingForm").classList.add("hidden");
    document.getElementById("databaseForm").classList.add("hidden");
    if (option === "webscraping") {
        document.getElementById("webscrapingForm").classList.remove("hidden");
    } else if (option === "database") {
        document.getElementById("databaseForm").classList.remove("hidden");
    }
});

// Handle Web Scraping Form Submission
document.getElementById("scrapeForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    const url = document.getElementById("scrapeUrl").value;
    const searchTerm = document.getElementById("searchTerm").value;

    try {
        const response = await fetch(`http://127.0.0.1:8000/scrape?url=${encodeURIComponent(url)}&search_term=${encodeURIComponent(searchTerm)}`);
        if (!response.ok) throw new Error("Failed to scrape data");
        const result = await response.json();
        displayData(result.data);
        createDownloadLink(result.data, "web_scraping_result.csv");
    } catch (error) {
        document.getElementById("output").innerText = "Error during web scraping.";
        console.error(error);
    }
});

// Handle Database Form Submission
document.getElementById("dbForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    const dbHost = document.getElementById("dbHost").value;
    const dbUser = document.getElementById("dbUser").value;
    const dbPassword = document.getElementById("dbPassword").value;
    const dbName = document.getElementById("dbName").value;
    const tableName = document.getElementById("tableName").value;

    try {
        const response = await fetch(`http://127.0.0.1:8000/mysql_data?db_host=${encodeURIComponent(dbHost)}&db_user=${encodeURIComponent(dbUser)}&db_password=${encodeURIComponent(dbPassword)}&db_name=${encodeURIComponent(dbName)}&table_name=${encodeURIComponent(tableName)}`);
        if (!response.ok) throw new Error("Failed to fetch database data");
        const result = await response.json();
        displayData(result.data);
        createDownloadLink(result.data, "database_result.csv");
    } catch (error) {
        document.getElementById("output").innerText = "Error fetching database data.";
        console.error(error);
    }
});

// Function to display data in a table
function displayData(data) {
    if (!data || data.length === 0) {
        document.getElementById("output").innerText = "No data available.";
        return;
    }
    const table = document.createElement("table");
    const headers = Object.keys(data[0]);

    // Create table header
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    headers.forEach(header => {
        const th = document.createElement("th");
        th.textContent = header;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create table body
    const tbody = document.createElement("tbody");
    data.forEach(row => {
        const tr = document.createElement("tr");
        headers.forEach(header => {
            const td = document.createElement("td");
            td.textContent = row[header];
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
    table.appendChild(tbody);

    // Display the table
    const output = document.getElementById("output");
    output.innerHTML = ""; // Clear previous output
    output.appendChild(table);
}

// Function to create a CSV download link
function createDownloadLink(data, filename) {
    if (!data || data.length === 0) return;

    // Convert data to CSV
    const headers = Object.keys(data[0]);
    const csvRows = [];
    csvRows.push(headers.join(","));
    data.forEach(row => {
        const values = headers.map(header => `"${row[header] || ""}"`);
        csvRows.push(values.join(","));
    });
    const csvContent = csvRows.join("\n");

    // Create a Blob for the CSV
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);

    // Create a download link
    const downloadLink = document.createElement("a");
    downloadLink.href = url;
    downloadLink.download = filename;
    downloadLink.textContent = "Download CSV";
    downloadLink.style.display = "block";
    downloadLink.style.marginTop = "20px";

    // Append the link to the output section
    const output = document.getElementById("output");
    output.appendChild(downloadLink);
}
