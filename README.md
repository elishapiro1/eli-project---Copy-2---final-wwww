# Flask Web Application

A modern Flask web application with Bootstrap 5 styling and responsive design.

## Features

- Modern Bootstrap 5 UI
- Responsive design
- Template inheritance
- Environment variable support
- Clean project structure

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
- Copy `.env.example` to `.env`
- Update the values in `.env` with your configuration

## Running the Application

1. Start the development server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
.
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── .env               # Environment variables
├── static/            # Static files (CSS, JS, images)
│   └── css/
│       └── style.css
└── templates/         # HTML templates
    ├── base.html
    ├── index.html
    └── about.html
``` 