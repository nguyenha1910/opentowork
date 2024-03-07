# Examples

* [1. Set up the repo](#set-up)
* [2. Scrape data](#data-scraping)
* [3. Run the app](#run-app)
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

<a id="data-scraping"></a>
### 2. Scrape data

<a id="run-app"></a>
### 3. Run the app

#### Run locally
To run the app locally, run this command
```bash
conda activate opentowork
python -m streamlit run pages/home.py
```

#### Deployment
Our sharable web-app: [link](link)


<a id="web-app"></a>
### 4. Explore the web application
[Tutorial](./streamlit_app.md)  
[Video demo]()