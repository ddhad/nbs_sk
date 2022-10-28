# https://nbs.sk/en/press/news-overview/ spider

Scrapy crawler scraping data from nbs.sk. The result is saved in a sqlite3 database. Items can be listed and deleted
using FastAPI.

# Installation

To install and run this project we can use the IDE for auto setup

1. Clone the project  
   **git clone https://github.com/ddhad/nbs_sk**
2. Create and activate virtual environment
3. Install the project packages  
   **pip install -r requirements.txt**

# Pipelines

1. Validates the entire item based on a given JSON Schema  
   **'scrapy_jsonschema.JsonSchemaValidatePipeline': 100,**
2. Stores the output data in a SQLite database  
   **'ScrapyNbs_sk.pipelines.ScrapynbsSkPipeline': 300,**

# How to run

1. Run spider (With the name "example")  
   **cd nbs_sk**  
   **scrapy crawl example**
2. Run server  
   **cd ..**  
   **uvicorn working:app --reload**  
   uvicorn <name_of_file>:<name_of_FastAPI()_variable> --reload  
