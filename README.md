# market-trends
[![Build Status](https://dev.azure.com/scottbreitenbach/scottbreitenbach/_apis/build/status/sbreitenbach.market-trends?branchName=main)](https://dev.azure.com/scottbreitenbach/scottbreitenbach/_build/latest?definitionId=4&branchName=master) [![Version](https://img.shields.io/github/v/release/sbreitenbach/market-trends)](https://img.shields.io/github/v/release/sbreitenbach/market-trends)


## A Script to Look for Trends in the Market

### THIS IS NOT FINIACIAL ADVICE
This is provided for informational purposes only and should not be used as financial advice. I am not a financial advisor, this tool is not a substitute for research and a consultation with a financial advisor. 

### Running the Script
1. You will need to get a valid API key for all data sources, see the sample secret configuration file for an example of the expected configuration. Please note that while this code is open source, you need to review the user agreements for each data source to ennsure your usage is within their guidelines.
2. You can adjust the data sources and depth of the search using the public configuration file.
3. Before the first run you may need to install any missing packages and [download emojis.](https://pypi.org/project/demoji/)
4. Run the main.py file, it will print out the results to the console. Note that due to rate limiting the initial data collection can take a long time.
