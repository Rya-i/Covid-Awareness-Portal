# COVID-19 Awareness and Information Portal

Final-year Computer Engineering STQA mini project. A Flask + MySQL website with educational pages, an informational symptom questionnaire (nothing stored), and a feedback form (saved in MySQL).

**Disclaimer:** general awareness only; not medical advice or a diagnostic tool.

## 1. Features
Home, About, Symptoms (with warning signs), Prevention, FAQ accordion (11 items), Questionnaire, Trusted Resources, Feedback form with server-side validation, custom 404/500 pages.

## 2. Technologies
HTML5, CSS3, JavaScript, Python Flask, Jinja2, MySQL, `mysql-connector-python`, `python-dotenv`.

## 3. Prerequisites
Windows 10/11, Python 3.10+ (tick "Add Python to PATH"), MySQL Server 8.x with the `mysql` command available, Google Chrome.

## 4. Virtual environment (PowerShell, inside `CovidAwarenessSTQA`)
```powershell
cd path\to\CovidAwarenessSTQA
python -m venv venv
.\venv\Scripts\Activate.ps1
```
If activation is blocked: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## 5. Install dependencies
```powershell
pip install -r requirements.txt
```

## 6. Configure MySQL Server
Install MySQL Server and note your root (or other user) password. Check it is running:
```powershell
Get-Service MySQL*
Start-Service MySQL80   # use the service name shown above if different
```

## 7. Create the database
```powershell
mysql -u root -p < schema.sql
```
(If `<` fails in PowerShell, use: `cmd /c "mysql -u root -p < schema.sql"`.) This creates `covid_awareness_db` and the `feedback` table.

## 8. Configure `.env`
```powershell
Copy-Item .env.example .env
notepad .env
```
Set `SECRET_KEY` to a long random string and fill `DB_USER` / `DB_PASSWORD`. Never commit `.env`.

## 9. Run
```powershell
python app.py
```

## 10. Open
Go to http://127.0.0.1:5000 in Chrome.

## 11. Troubleshooting
- **`mysql` not recognized:** add `C:\Program Files\MySQL\MySQL Server 8.0\bin` to PATH, or use the full path.
- **Feedback says "could not save":** check MySQL is running, `.env` credentials, and that `schema.sql` was imported.
- **`ModuleNotFoundError`:** activate the venv and re-run `pip install -r requirements.txt`.
- **Port 5000 in use:** close the other app or run `flask --app app run --port 5001`.
- **Access denied (MySQL):** verify `DB_USER`/`DB_PASSWORD`.

## Project structure
`app.py` (routes/validation), `database.py` (MySQL), `schema.sql`, `templates/`, `static/css/style.css`, `static/js/main.js`.
