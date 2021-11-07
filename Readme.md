# Install dependencies
Python 3.9.7
```
pip install -r requirements.txt
```

# Run the crawler
```
python -m scrapy runspider ./crawler/crawl.py  -o output.jl
```

# Post-process crawled data
Output is stored in `output.csv`.
```
python post_process.py
```

# Running in Spark
Preprocess data for Spark
```
python create_edge_vertex_tables.py
```

Download spark Docker image for local development
```
docker pull jupyter/pyspark-notebook
```

Run the container in detached mode
```
docker run -p 8889:8889 -d -p 4040:4040 -p 4041:4041 -v /Users/tomashoffer/Documents/Coding-Projects/vinf:/home/jovyan -it --rm --name pyspark-notebook jupyter/pyspark-notebook
```
Run Jupyter notebook with Spark from within the container
```
docker exec -it pyspark-notebook bash
export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS=notebook
pyspark --packages graphframes:graphframes:0.8.2-spark3.2-s_2.12
```
Jupyter notebook server now listens on localhost:8089...