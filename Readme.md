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