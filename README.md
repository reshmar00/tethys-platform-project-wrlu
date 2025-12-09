# Water-Related Land Use (WRLU) App

## Overview

The WRLU App is a [Tethys Platform](https://www.tethysplatform.org/) web application that visualizes water-related land use in Utah from 1989 to 1999. Users can:

- View an interactive map with land use polygons loaded from a GeoJSON file on AWS S3.
- Explore total WRLU area per year via a line plot aggregated from CSV data on S3.
- Use drawing and map controls to interact with the spatial data.

This app is built with the **Tethys SDK**, **Django**, **Python**, and **Pandas**, fetching data directly from AWS S3 using access keys.

## Demo

## Features

- **Interactive Map:** View and interact with water-related land use polygons.
- **Line Plot:** Aggregated total acreage per survey year (1989–1999).
- **Drawing Tools:** Add points, lines, polygons, or modify existing features.

## Installation and Setup

### Prerequisites

- **Python** 3.10 or 3.11
- **Tethys Platform** 4.8.3  
- **Pandas**  
- **Boto3** (for S3 access)  

Ensure you have Python installed. You can install dependencies via pip:

```
pip install tethys-sdk pandas boto3 python-dotenv
```

### Setting Up the Project

1. **Clone the repository:**

```
git clone https://github.com/yourusername/wrlu-app.git
cd wrlu-app
```

2. **Create a conda virtual environment:**

```
conda create -n tethys_env python=3.11 -y
conda activate tethys_env
```

3. **Install dependencies:**

```
pip install -r requirements.txt
```

4. **Configure environment variables:**

```
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
BUCKET_NAME=your_s3_bucket_name
GEOJSON_KEY=path/to/geojson_file.geojson
CSV_KEY=path/to/csv_file.csv
```

**Note:** I stored the GeoJSON and CSV files that I downloaded from [Utah's Open Water Data website](https://dwre-utahdnr.opendata.arcgis.com/pages/wrlu-data)(Publicly available data provided by the Utah Division of Water Resources) in an S3 bucket. If you want to follow my method of doing that, you just have to change variable names. If you'd rather work with files locally, you will have to change parts of the code where files are accessed.

5. **Run the Tethys server:**

```
tethys manage start
```

6. **Access the app:**
Open your browser and go to:

```
http://127.0.0.1:8000/apps/project-wrlu/
```

## Usage

- Explore the map and interact with land use polygons.
- Use the drawing tools to add or modify spatial features.
- View the line plot of total WRLU acreage per year below the map.

## Project Structure

```
├── README.md
└── .env                                 # Environment variables
└── requirements.txt
└── tethysapp-project_wrlu
   ├── install.yml
   ├── pyproject.toml
   ├── tethysapp
   │   └── project_wrlu
   │       ├── __init__.py
   │       ├── app.py                  # App configuration
   │       ├── controllers.py          # Main controller handling map & plot
   │       ├── public
   │       │   ├── css
   │       │   │   └── main.css
   │       │   ├── images
   │       │   │   └── icon.gif
   │       │   └── js
   │       │       └── main.js
   │       ├── resources
   │       ├── templates
   │       │   └── project_wrlu
   │       │       ├── base.html
   │       │       └── home.html        # Template for the homepage
   │       └── tests
   │           ├── __init__.py
   │           ├── __pycache__
   │           └── tests.py
```

## Notes

- The app fetches data securely from S3 using AWS Access Keys. Ensure your keys have appropriate read permissions.
- If S3 objects are private, the app requires access keys to fetch CSV and GeoJSON.
- The map and plot will display even if the CSV fails to load, but a placeholder will be shown.

### Contact

If you encounter any issues or have any questions, reach out to me.

Enjoy exploring Water-Related Land Use in Utah!
