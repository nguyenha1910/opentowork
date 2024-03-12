# Examples

* [1. Set up the repo](#set-up)
* [2. Run the app](#run-app)
* [3. Update data](#data-scraping)
* [4. Explore the web application](#web-app)
* [5. Run unit tests](#run-tests)

<a id="set-up"></a>
### 1. Set up

Clone the repo by running this command:
```bash
git clone https://github.com/nguyenha1910/opentowork.git
```

Set up `opentowork` virtual environment
```bash
conda env create -f environment.yml
```

Activate the environment
```bash
conda activate opentowork
```

<a id="run-app"></a>
### 2. Run the app

#### Run locally
To run the app locally, run this command
```bash
conda activate opentowork
python -m streamlit run pages/home.py
```

<a id="data-scraping"></a>
### 3. Update job listing data
A starter data file is included in the repository. To update this data, click the "Update Job Posting Data" button in the web app. (The button is only visible after uploading a resume). Additional requirements to install for this function are listed [here](../README.md#data).

*Note that the scraping process may take anywhere from 10-20 minutes to complete. We also cannot guarantee that the scraper will get data everytime, as it depends on LinkedIn and Indeed website behavior. More details can be found [here](scraper.md).

<a id="web-app"></a>
### 4. Explore the web application
[Tutorial](streamlit_app.md)

[Video demo]()

<a id="run-tests"></a>
### 5. Run unit tests
To run unit tests on the code, make sure all dependencies (including [scraping requirements](../README.md#data)) are met.

Run the following code from the root opentowork folder:
```bash
conda activate opentowork
python -m unittest discover
```

Unit tests cover the skill analyzer, match score generator, scraper, and UI functionalities and may take about 15-20 minutes to run all of them.