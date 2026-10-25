"""COVID-19 Awareness and Information Portal - Flask application."""
import os
import re
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

load_dotenv()
import database  # noqa: E402  (after load_dotenv so env vars are available)

app = Flask(__name__)
# Secret key comes from .env; a random one is used only if missing (sessions reset on restart).
app.secret_key = os.getenv("SECRET_KEY") or os.urandom(24)

# ---- Static educational content (no database needed) ----
SYMPTOMS = [
    ("🌡️", "Fever or chills", "A raised body temperature, sometimes with shivering."),
    ("😮‍💨", "Cough", "A new or worsening cough that may be dry or produce mucus."),
    ("🗣️", "Sore throat", "Scratchy or painful throat, especially when swallowing."),
    ("🔋", "Fatigue", "Unusual tiredness or low energy that is hard to explain."),
    ("👃", "Loss of taste or smell", "A sudden change or loss in taste or smell."),
    ("🤕", "Headache and body aches", "Muscle or joint pain and headaches are also reported."),
]
WARNING_SIGNS = [
    "Trouble breathing or shortness of breath at rest",
    "Persistent pain or pressure in the chest",
    "New confusion or difficulty staying awake",
    "Bluish lips or face",
    "Inability to speak or move normally",
]
PREVENTION = [
    ("🧼", "Hand hygiene", "Wash hands with soap and water for at least 20 seconds, or use an alcohol-based sanitizer."),
    ("🤧", "Respiratory etiquette", "Cover coughs and sneezes with a tissue or elbow and dispose of tissues safely."),
    ("🪟", "Ventilation", "Open windows or improve airflow in shared indoor spaces."),
    ("🏠", "Reduce exposure when ill", "Stay home when unwell and avoid close contact with others, especially vulnerable people."),
    ("💉", "Vaccination", "Vaccines help reduce severe illness. Ask a healthcare professional or official health site which vaccines suit you."),
]
FAQS = [
    ("What is COVID-19?", "COVID-19 is an infectious respiratory disease caused by the SARS-CoV-2 virus."),
    ("How does COVID-19 spread?", "Mainly through respiratory droplets and aerosols when an infected person coughs, sneezes, talks or breathes, and sometimes through contaminated surfaces."),
    ("What are the common symptoms?", "Fever, cough, sore throat, fatigue and loss of taste or smell are common, but symptoms vary from person to person."),
    ("Can COVID-19 symptoms overlap with flu or colds?", "Yes. Many respiratory illnesses cause similar symptoms, so symptoms alone cannot tell them apart."),
    ("Can someone spread the virus without symptoms?", "Yes. Some infected people have mild or no symptoms but can still pass the virus on."),
    ("How can I reduce my risk?", "Practise hand hygiene, cover coughs, improve ventilation, stay home when sick and keep vaccinations up to date as advised by health authorities."),
    ("Do vaccines help?", "Public-health agencies report that vaccines help lower the risk of severe illness. Check official sources for current recommendations."),
    ("When should I seek urgent medical help?", "If you have trouble breathing, persistent chest pain or pressure, confusion, bluish lips or face, or you cannot stay awake, seek emergency care immediately."),
    ("Should I use this website to diagnose myself?", "No. This site is for general awareness only. A healthcare professional can advise on testing and care."),
    ("Where can I find reliable information?", "WHO, CDC and the Ministry of Health and Family Welfare (India) publish current guidance. See the Resources page."),
    ("Does guidance change over time?", "Yes. Recommendations are updated as evidence evolves, so check official sources for the latest advice."),
]
RESOURCES = [
    ("World Health Organization (WHO)", "https://www.who.int/health-topics/coronavirus", "Global health topic page on coronavirus."),
    ("Centers for Disease Control and Prevention (CDC)", "https://www.cdc.gov/covid/", "US public-health guidance on COVID-19."),
    ("Ministry of Health and Family Welfare, India", "https://mohfw.gov.in/", "Official updates from the Government of India."),
]
Q_COMMON = [("fever", "Fever or chills"), ("cough", "Cough"), ("sore_throat", "Sore throat"),
            ("fatigue", "Fatigue"), ("taste_smell", "Loss of taste or smell"),
            ("aches", "Headache or body aches"), ("runny_nose", "Runny or blocked nose")]
Q_SEVERE = [("breathing", "Trouble breathing"), ("chest_pain", "Persistent chest pain or pressure"),
            ("confusion", "New confusion or cannot stay awake"), ("bluish", "Bluish lips or face")]
CATEGORIES = ["Website design", "Content accuracy", "Suggestion", "Bug report", "Other"]
Q_ALL = {k for k, _ in Q_COMMON + Q_SEVERE}
SEVERE_KEYS = {k for k, _ in Q_SEVERE}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@app.context_processor
def inject_globals():
    return {"warning_signs": WARNING_SIGNS}


@app.route("/")
def index():
    cards = [("🩺", "Symptoms", "Learn the common signs.", "symptoms"),
             ("🛡️", "Prevention", "Everyday protective habits.", "prevention"),
             ("❓", "FAQs", "Answers to common questions.", "faq"),
             ("🔗", "Trusted resources", "Official public-health sources.", "resources")]
    return render_template("index.html", cards=cards)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/symptoms")
def symptoms():
    return render_template("symptoms.html", symptoms=SYMPTOMS)


@app.route("/prevention")
def prevention():
    return render_template("prevention.html", items=PREVENTION, resources=RESOURCES)


@app.route("/faq")
def faq():
    return render_template("faq.html", faqs=FAQS)


@app.route("/resources")
def resources():
    return render_template("resources.html", resources=RESOURCES)


@app.route("/questionnaire", methods=["GET", "POST"])
def questionnaire():
    """Informational only. Responses are never stored or scored."""
    result, error = None, None
    selected = []
    if request.method == "POST":
        selected = [s for s in request.form.getlist("symptoms") if s in Q_ALL]
        if not selected and request.form.get("none") != "1":
            error = "Please select at least one symptom, or tick \"None of these\"."
        elif selected and any(s in SEVERE_KEYS for s in selected):
            result = ("urgent", "You selected a serious warning sign. Seek urgent medical attention or call your local emergency number now.")
        elif selected:
            result = ("info", "These symptoms can occur with COVID-19 and many other illnesses. If you are concerned, please consult a healthcare professional and follow current official guidance.")
        else:
            result = ("info", "You did not select any symptoms. If you feel unwell or are concerned, consult a healthcare professional.")
    return render_template("questionnaire.html", common=Q_COMMON, severe=Q_SEVERE,
                           selected=selected, result=result, error=error)


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    form, errors = {"name": "", "email": "", "category": "", "message": ""}, []
    if request.method == "POST":
        for key in form:  # strip whitespace from every field
            form[key] = request.form.get(key, "").strip()
        if len(form["name"]) > 100:
            errors.append("Name must be 100 characters or fewer.")
        if form["email"] and (len(form["email"]) > 150 or not EMAIL_RE.match(form["email"])):
            errors.append("Please enter a valid email address.")
        if form["category"] not in CATEGORIES:
            errors.append("Please choose a feedback category.")
        if not 10 <= len(form["message"]) <= 1000:
            errors.append("Message must be between 10 and 1000 characters.")
        if not errors:
            try:
                database.save_feedback(form["name"], form["email"], form["category"], form["message"])
                return redirect(url_for("feedback_success"))
            except database.DatabaseError:
                errors.append("Sorry, we could not save your feedback right now. Please try again later.")
    return render_template("feedback.html", form=form, errors=errors, categories=CATEGORIES)


@app.route("/feedback/success")
def feedback_success():
    return render_template("feedback_success.html")


@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


@app.errorhandler(500)
@app.errorhandler(Exception)
def server_error(_e):
    # Generic page only: no stack traces or credentials are shown.
    if hasattr(_e, "code") and _e.code and _e.code != 500:
        return _e
    return render_template("500.html"), 500


if __name__ == "__main__":
    # Debug is OFF unless FLASK_DEBUG=1 is set for local development.
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
