# Streamlit Offline App
---

## Requirements

* **Windows OS**
* **Python 3.8+** (via Conda environment)
* **Conda** (Anaconda or Miniconda)

---

## Setup Instructions

1. **Download or copy this project**

```
my_app/
├── streamlit_app.py
├── requirements.txt
├── run_app.bat
└── data/      (if your app uses data files)
```

2. **Create the Conda environment** (first-time setup)

Open Anaconda Prompt or terminal and run:

```bash
conda create -n my_env_name python=3.10
conda activate my_env_name
pip install -r requirements.txt
```

> Replace `my_env_name` with your preferred environment name.

3. **Check the batch file**

Open `run_app.bat` in a text editor and make sure the path to your Conda installation is correct:

```bat
call C:\Users\YourUserName\miniconda3\Scripts\activate.bat
conda activate my_env_name
streamlit run streamlit_app.py
pause
```

---

## Running the App

* Double-click **`run_app.bat`**.
* This will:

  1. Activate the Conda environment
  2. Run the Streamlit app
  3. Open the app in your default web browser

---

## Notes

* The terminal window stays open to show errors.
* If you add new dependencies, run:

```bash
pip install -r requirements.txt
```

* Ensure any data files your app uses are inside the project folder.

---