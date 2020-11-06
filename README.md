# bookstore-api-tests

__Description__: Demonstrate API test automation of [Book Store API](https://demoqa.com/swagger) in Python and PyTest.

__Platform__: Darwin

## Features
 * Pytest test framework
 * Parallel execution (~5x faster than sequential)
 * Random execution
 * Parametrize (DDT) test cases
 * HTML report
 * Performance profiling
 * No data collision
 * Repeat N-time(s) excecution

## Prerequisite Software

Download and install [Python 3.9.0](https://www.python.org/downloads/release/python-390/) for Mac.

## Setup

1. Setup Virtual Environment
```
make setup
```
2. Install Dependencies
```
make install
```
3. Activate Your Virtual Environment
```
bookstore
```
You should see ```(.bookstore)``` in your command prompt.

## Execute the Tests
```
make
```

## View the HTML Test Results Report
```
reports/report.html
```
## Deactivate Your Virtual Environment
```
deactivate
```
