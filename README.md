# 🧪 Pharma Report Analysis Tool

A small but meaningful Python project I built while learning how to work with **Pandas**, **CSVs**, and **API ingestion**.  
This project represents my first hands-on experience combining data handling and real-world API interactions into a cohesive workflow.  
I worked **alongside a developer** to put together the API that powers this project, which helped me understand how backend endpoints are designed and how frontend data scripts consume them.

---

## 🚀 Project Overview

The **Pharma Report Analysis Tool** reads an existing CSV file containing yearly financial data (such as revenue, profit, cost, and price) for a small healthcare company.  
If the user requests a year range that includes missing years, the program automatically retrieves those missing records from an API and appends them to a new CSV file.

At its core, the project:
- Reads and validates CSV data with **Pandas**
- Iterates over a user-defined year range
- Fetches missing data from a live **API endpoint**
- Merges and exports the complete dataset to a results folder

This was a simple project, but one that helped me bridge the gap between static data handling and dynamic data ingestion.

---

## 🧩 Key Concepts I Learned

1. **Working with CSVs in Pandas**  
   - Loading, cleaning, validating, and manipulating data.  
   - Handling missing values and removing duplicates.  
   - Using `DataFrame` indexing for fast lookups.

2. **Interacting with APIs using Requests**  
   - Making GET requests and parsing JSON responses.  
   - Understanding API response structures and error handling.  
   - Dynamically ingesting data and integrating it into existing data pipelines.  
   - Collaborating on API design and understanding backend-frontend data exchange.

3. **Automating Data Processing**  
   - Iterating through user-specified year ranges.  
   - Detecting missing entries and filling them in automatically.  
   - Writing processed results back to disk for reporting.

4. **Structuring Python Projects**  
   - Organizing functions, constants, and helper utilities.  
   - Using `__main__` blocks for terminal execution.  
   - Building clear, readable code focused on functionality over optimization.

---

## ⚙️ How It Works

1. Run the program in a terminal:
   ```bash
   python main.py
   ```
2. Enter the start and end years when prompted.  
3. The tool reads the existing dataset from:
   ```
   Data/LogData.csv
   ```
4. For each year in the range:
   - If the data already exists, it reuses it.  
   - If the data is missing, it calls the API:
     ```
     https://pharamapi.com/financialReport/?year=YYYY
     ```
     and adds the new record to the dataset.
5. The final merged dataset is exported to:
   ```
   Results/result.csv
   ```

---

## 🗂️ Project Structure

```
Pharma-Report-Tool/
│
├── Data/
│   └── LogData.csv           # Original dataset
│
├── Results/
│   └── result.csv            # Output file (auto-generated)
│
├── main.py                   # Entry point script
│
└── README.md
```

---

## 🧠 What This Project Taught Me

This was my introduction to **data pipelines** — moving data from one place to another, transforming it along the way.  
Through this project, I learned how to:
- Think about data as structured objects rather than raw text.  
- Build lightweight automation tools that add value to static datasets.  
- Debug issues between local data and external APIs.  
- Collaborate with another developer to integrate a working API endpoint.  
- Write code that’s simple, modular, and easy to understand.

---

## 🔮 Future Improvements

I plan to expand this project beyond a terminal tool:

- **📊 Data Visualization:**  
  Add visual charts using libraries like `matplotlib` or `plotly` to visualize revenue, profit, and cost over time.

- **🌐 Web Interface:**  
  Create a small web dashboard (possibly with `Flask` or `Streamlit`) where users can input year ranges and view real-time reports.

- **📦 Extended API Usage:**  
  Introduce more API endpoints (e.g., historical market data, cost breakdowns) and merge them for deeper insights.

- **🧰 Better Error Handling:**  
  Handle network issues, malformed responses, and local data corruption more gracefully.

---

## 💬 Personal Reflection

While the logic is simple, this project taught me how real-world data workflows function.  
It made me comfortable reading documentation, debugging APIs, and using Python libraries to automate small but meaningful tasks.  
Working with another developer to design and consume an API also gave me insight into how backend and frontend systems communicate.  

It’s a foundational project — not complex, but one that reflects my willingness to **learn by building**.

---

## 🧑‍💻 Technologies Used

- **Python 3.12+**  
- **Pandas** – Data manipulation and CSV handling  
- **Requests** – API interaction  
- **Pathlib & Sys** – File handling and CLI interaction  

---

## 📥 Running the Project

1. Install dependencies:
   ```bash
   pip install pandas requests
   ```
2. Run the program:
   ```bash
   python main.py
   ```
3. Enter your desired year range when prompted.
4. Find your output file in the `Results/` directory.

---

## 🧾 Example Output

```
Welcome to the Pharma Report Analysis Tool
Start year: 2015
End year: 2025
Fetching missing data...
Wrote Results/result.csv with 11 rows
results saved
```

---

## 🪄 Takeaway

This project might be small, but it represents an important step in my development journey —  
understanding how to combine **data engineering**, **API integration**, and **Python scripting** into a functional mini-application.  
It also gave me experience collaborating with a developer to connect backend and frontend components of a small data product.
