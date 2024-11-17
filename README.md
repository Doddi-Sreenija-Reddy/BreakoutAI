# AI Agent Dashboard for Automated Data Retrieval

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Getting Started](#getting-started)
4. [Using the Application](#using-the-application)
   - [CSV File Input](#using-csv-files)
   - [Google Sheets Input](#using-google-sheets)
   - [Search Query Configuration](#search-query-configuration)
5. [API Keys and Environment Setup](#api-keys-and-environment-setup)
   - [Groq API](#groq-api-key)
   - [SerpAPI](#serpapi-key)
   - [Google Sheets API](#google-sheets-credentials)
6. [Optional Features](#optional-features)
7. [Export Options](#export-options)
8. [Data Validation](#data-validation)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)
11. [License](#license)

---

## Introduction

The **AI Agent Dashboard** is a comprehensive solution for automated information retrieval, enabling users to extract and analyze data from CSV files or Google Sheets. This tool leverages the power of Large Language Models (LLMs) and web scraping APIs to provide dynamic query handling and AI-powered data extraction. It is designed to streamline the process of gathering insights on entities, making it suitable for various applications in domains like market research, content analysis, and competitive intelligence.

---

## Features

- **Multi-source Data Input**: Supports CSV uploads and Google Sheets for flexible data sourcing.
- **Dynamic Search Query Configuration**: Customize search prompts using placeholders for entity names.
- **API Integration**: Utilizes Groq API, SerpAPI, and Google Sheets API for comprehensive data extraction.
- **Real-time Processing**: View live progress updates while data is being processed.
- **Advanced Export Options**: Download results in CSV format for further analysis.
- **Enhanced Search and AI Response Control**: Customize search result limits, AI temperature, and token limits.

---

## Getting Started

To get started, ensure that you have the required dependencies installed and the necessary API keys set up. Follow the instructions below for installation and configuration.

### Prerequisites

- Python 3.8 or above
- `pip` package manager

### Installation

1. **Clone the Repository**:
    ```bash
    git clone (https://github.com/Doddi-Sreenija-Reddy/BreakoutAI.git)
    cd BreakoutAI
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Environment Configuration**:
   - Create a `.env` file in the project root directory and add your API keys

---
## Loom Video Demo
Check out a quick walkthrough of the project [here]().

### Using CSV Files

1. **Navigate to the Sidebar** and select **CSV Upload**.
2. **Upload Your CSV File** containing entities for analysis.
3. **Select the Target Column** with your desired entities.
4. **Enter a Custom Search Prompt** (e.g., "What are the main products of {entity}?").
5. Click the **Process Data** button to begin analysis.
6. **Download Results** using the **Download Results** button after processing.

### Using Google Sheets

1. **Set up Google Sheets Credentials**.
2. In the sidebar, select **Google Sheets**.
3. **Enter the URL** of your Google Sheet.
4. Choose the target column containing entities.
5. **Enter a Custom Search Prompt** and click **Process Data** to start the analysis.
6. Download the results using the **Download Results** button.

---

## Search Query Configuration

- Customize your search prompts using `{entity}` as a placeholder (e.g., "Provide an overview of {entity}'s latest products").
- The system automatically replaces `{entity}` with actual values from your CSV or Google Sheets data.
- You can adjust AI response settings such as temperature and token limits for better control over the outputs.

---

## API Keys and Environment Setup

To utilize the full functionality of this application, you'll need API keys for Groq, SerpAPI, and Google Sheets. Make sure all API keys are added to your `.env` file.

### Groq API Key
1. [Sign up at Groq](https://groq.com) and obtain your API key.
2. Add it to your `.env` file:
    ```bash
    GROQ_API_KEY=your_groq_api_key
    ```

### SerpAPI Key
1. [Register at SerpAPI](https://serpapi.com) to get your API key.
2. Add it to your `.env` file:
    ```bash
    SERPAPI_API_KEY=your_serpapi_api_key
    ```

### Google Sheets Credentials
1. Create a project in [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Google Sheets API**.
3. Download the service account credentials JSON file.
4. Rename it to `google_sheets_credentials.json` and place it in the project root.

---

## Optional Features

### Enhanced Search Options
- **Adjust Search Results**: Specify the number of results to retrieve per query.
- **AI Response Parameters**: Customize temperature and maximum token length for refined AI responses.
- **Custom Search Templates**: Use templates tailored to your analysis requirements.

### Data Validation
- **Automatic Missing Value Detection**: Identifies and flags missing values in your data.
- **Input Validation**: Ensures correct Google Sheets URL format to avoid errors.
- **Error Notifications**: Alerts users about any configuration or data-related issues.

---

## Export Options

- **CSV Export**: Download processed results in CSV format for easy integration with other tools.
- **Real-time Processing Progress**: Monitor the status of your data processing in real time.
- **Data Preview**: Review data before starting the analysis to ensure accuracy.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

--- 

Feel free to reach out if you have any questions or need further assistance. Happy analyzing! 🚀
