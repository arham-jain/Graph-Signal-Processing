# Graph-Signal-Processing

An analytic tool to automate preprocessing and analysis using Graph Signal Processing. The project is written in Python, it is recommended to replicate the environment by creating a virtual environment. On creation, all the dependencies need to be installed from the requirements.txt.

## Creating Virtual Environment

Python 3 already ships virtualenv. But if it’s not installed in your environment for some reason, you can install it via the package for your operating systems, otherwise you can install from pip:

```pip install virtualenv```

You can create and activate a virtualenv by:
```
# virtualenv is shipped in Python 3.6+ as venv instead of pyvenv.
# See https://docs.python.org/3.6/library/venv.html
python3 -m venv venv
. venv/bin/activate
```

On windows the syntax for activating it is a bit different:

```venv\Scripts\activate```

Once you activated your virtualenv everything you are doing is confined inside the virtualenv. To exit a virtualenv just type deactivate.

## Installing Dependencies

Once the virtual environment is activated. Use the following command to download all the python dependencies

```python -m pip install -r requirements.txt```

## Run the project

Head to the directory of the project and run the following command:

```python app.py```

The URL's Currently working are:
- http://127.0.0.1:5000/
- http://127.0.0.1:5000/dashboard/name
  Example use: http://127.0.0.1:5000/dashboard/Yamraj
- http://127.0.0.1:5000/dashboard/param_selection
- http://127.0.0.1:5000/dashboard/indicator_code/year
  Example use: http://127.0.0.1:5000/dashboard/SP.POP.DPND/1999
- http://127.0.0.1:5000/dashboard/gspboard
- http://127.0.0.1:5000/dashboard/gspboard/new
