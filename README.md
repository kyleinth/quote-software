# Quote Software

This project implements a minimal quoting system for uploading PDF documents and STEP models. The application calculates a quote based on the number of pages in the PDF file and the size of the STEP file.

## Features

- Upload a PDF and STEP file using a simple web interface.
- Quote is calculated as:
  - `$0.05` per page of the PDF file.
  - `$0.10` per megabyte of the STEP file.
- Returns the quote in JSON format.

## Running the application

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   python src/app.py
   ```
3. Open a browser to `http://localhost:5000` to upload files and get a quote.

## Endpoints

- `GET /` – simple upload form.
- `POST /quote` – accepts `pdf` and `step` files in `multipart/form-data` and returns quote information in JSON.

## Uploading to GitHub

After committing your changes locally, create a new repository on GitHub and run:

```bash
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin work
```

Replace `USERNAME` and `REPO` with your GitHub username and repository name.
