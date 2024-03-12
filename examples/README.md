# Examples

* [1. Set up the repo](#set-up)
* [2. Run the app](#run-app)
* [3. Update data](#data-scraping)
* [4. Explore the web application](#web-app)

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
A starter data file is included in the repository. To update this data, click the "Update Job Posting Data" button in the web app. (The button is only visible after uploading a resume)

*Note that the scraping process may take anywhere from 10-30 minutes to complete. We also cannot guarantee that the scraper will get data everytime, as it depends on LinkedIn and Indeed website behavior. More details can be found [here](scraper.md).

<a id="web-app"></a>
### 4. Explore the web application
[Tutorial](streamlit_app.md)

[Video demo]()