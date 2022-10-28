# https://nbs.sk/en/press/news-overview/ spider and API

Scrapy crawler scraping data from nbs.sk, and FastAPI endpoints to update, delete and filter items from Sqlite3 database. 
<pre>
/articles/             Lists all items from database  
/articles/?date=       Returns items with matching date  
/articles/?label=      Returns items with matching label  
/articles/id           Finds item by ID  
/articles/id           Delete method  
/articles/id           Update method  
</pre>
# Installation

To install and run this project:

1. Clone the project  
   **git clone https://github.com/ddhad/nbs_sk**
2. Create and activate virtual environment
3. Install the project packages  
   **pip install -r requirements.txt**

# How to run

1. Run spider (With the name "example")  
   **cd nbs_sk**  
   **scrapy crawl example**
2. Run server  
   **cd ..**  
   **uvicorn working:app --reload**  
   uvicorn <name_of_file>:<name_of_FastAPI()_variable> --reload  

# Pipelines

1. Validates the entire item based on a given JSON Schema  
   **'scrapy_jsonschema.JsonSchemaValidatePipeline': 100,**
2. Stores the output data in a SQLite database  
   **'ScrapyNbs_sk.pipelines.ScrapynbsSkPipeline': 300,**
