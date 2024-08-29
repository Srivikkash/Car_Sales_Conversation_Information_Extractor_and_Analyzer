import os
import spacy
from spacy.matcher import PhraseMatcher, Matcher
import json
import PyPDF2
from flask import Flask, request, render_template, redirect, url_for
from pyngrok import ngrok

ngrok_key = "2ZvgnEswiTrzK0HqIWummQSVqOG_6fnjV8bzTVFPEkithywRD"
port = 5000

from pyngrok import ngrok
ngrok.set_auth_token(ngrok_key)
print(ngrok.connect(port).public_url)

# Initialize Flask app and SpaCy model
app = Flask(__name__,template_folder='templates/')
nlp = spacy.load("en_core_web_sm")

# Set up upload and report directories
UPLOAD_FOLDER = 'uploads/'
REPORT_FOLDER = 'reports/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORT_FOLDER'] = REPORT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# Start ngrok for public URL access
print(ngrok.connect(5000).public_url)
def extract_data(conversation):
    conversation  = conversation.lower()
    # Initialize matchers for different categories
    customer_requirements_matchers = {
        "Car_Type": PhraseMatcher(nlp.vocab),
        "Fuel_Type": PhraseMatcher(nlp.vocab),
        "Color": PhraseMatcher(nlp.vocab),
        "Transmission_Type": PhraseMatcher(nlp.vocab),
    }

    company_policy_matchers = {
        "Free_RC_Transfer": PhraseMatcher(nlp.vocab),
        "5_Day_Money_Back_Guarantee": PhraseMatcher(nlp.vocab),
        "Free_RSA": PhraseMatcher(nlp.vocab),
        "Return_Policy": PhraseMatcher(nlp.vocab),
    }

    customer_objection_matchers = {
        "Refurbishment_Quality": PhraseMatcher(nlp.vocab),
        "Car_Issues": PhraseMatcher(nlp.vocab),
        "Price_Issues": PhraseMatcher(nlp.vocab),
        "Customer_Experience_Issues": PhraseMatcher(nlp.vocab),
    }

    # Define keywords for each matcher
    customer_requirements_keywords = {
        "Car_Type": ["sedan", "hatchback", "suv", "crossover", "coupe", "convertible", "wagon", "pickup truck", "minivan", "sport car", "electric vehicle (ev)", "hybrid", "luxury car"],
        "Fuel_Type": ["diesel","petrol", "electric", "hybrid"],
        "Color": ["white", "black", "blue", "red", "silver", "grey"],
        "Transmission_Type": ["automatic", "manual", "cvt"],
    }

    company_policy_keywords = {
        "Free_RC_Transfer": ["free rc transfer"],
        "5_Day_Money_Back_Guarantee": ["5 days","five days" "money back"],
        "Free_RSA": ["free rsa"],
        "Return_Policy": ["return policy"],
    }

    customer_objection_keywords = {
        "Refurbishment_Quality": ["refurbished", "second owner", "reconditioned", "restored", "damages", "repainted", "parts replaced", "repair history"],
        "Car_Issues": ["engine problems","vibrating", "transmission issues", "brake failure", "electrical faults", "leaks", "overheating", "tire issues", "suspension problems", "oil leaks", "noises", "performance issues", "fuel system problems"],
        "Price_Issues": ["too expensive","expensive", "budget constraints", "hidden fees", "additional costs", "financing options", "price negotiation", "unfair pricing", "high price", "price comparison", "value for money", "affordability", "market price"],
        "Customer_Experience_Issues": ["long wait time", "poor service", "salesperson behavior", "lack of communication", "unclear information", "unprofessional staff", "inconvenient location", "difficulty in scheduling", "limited options", "follow-up issues", "unresponsive", "staff knowledge", "rudeness", "unavailability"],
    }

    # Add patterns to matchers
    for key, matcher in customer_requirements_matchers.items():
        matcher.add(key, [nlp(text) for text in customer_requirements_keywords[key]])

    for key, matcher in company_policy_matchers.items():
        matcher.add(key, [nlp(text) for text in company_policy_keywords[key]])

    for key, matcher in customer_objection_matchers.items():
        matcher.add(key, [nlp(text) for text in customer_objection_keywords[key]])

    # Patterns for distance travelled and make year
    distance_pattern = [{"LIKE_NUM": True}, {"LOWER": {"IN": ["km", "miles", "kilometers"]}}]
    year_pattern = [{"TEXT": {"REGEX": r"^(19|20)\d{2}$"}}]

    distance_year_matcher = Matcher(nlp.vocab)
    distance_year_matcher.add("DISTANCE_TRAVELLED", [distance_pattern])
    distance_year_matcher.add("MAKE_YEAR", [year_pattern])

    # Process the conversation with NLP
    doc = nlp(conversation)

    # Initialize extracted data structure
    extracted_data = {
        "Customer_Requirements": {
            "Car_Type": "Null",
            "Fuel_Type": "Null",
            "Color": "Null",
            "Distance_Travelled": "Null",
            "Make_Year": "Null",
            "Transmission_Type": "Null",
        },
        "Company_Policies": {
            "Free_RC_Transfer": "Null",
            "5_Day_Money_Back_Guarantee": "Null",
            "Free_RSA": "Null",
            "Return_Policy": "Null",
        },
        "Customer_Objections": {
            "Refurbishment_Quality": "Null",
            "Car_Issues": "Null",
            "Price_Issues": "Null",
            "Customer_Experience_Issues": "Null",
        },
    }

    # Extract information using matchers
    def extract_phrase(matcher, doc):
        matches = matcher(doc)
        if matches:
            match_id, start, end = matches[0]  # Get the first match
            return doc[start:end].text
        return None

    # Split conversation into sentences
    sentences = conversation.split('\n')

    for doc_word in sentences:
      doc_word = doc_word.strip()
      doc_word = nlp(doc_word)
      # Extract customer requirements
      for key, matcher in customer_requirements_matchers.items():
          matched_phrase = extract_phrase(matcher, doc_word)
          if matched_phrase:
              extracted_data["Customer_Requirements"][key] = matched_phrase

      # Extract company policies
      for key, matcher in company_policy_matchers.items():
          matched_phrase = extract_phrase(matcher, doc_word)
          if matched_phrase:
              extracted_data["Company_Policies"][key] = matched_phrase

      # Extract customer objections
      for key, matcher in customer_objection_matchers.items():
          matched_phrase = extract_phrase(matcher, doc_word)
          if matched_phrase:
              extracted_data["Customer_Objections"][key] = matched_phrase

    for sentence in sentences:
        sentence = sentence.strip()
        doc_sentence = nlp(sentence)

        # Check for distance and year
        distance_year_matches = distance_year_matcher(doc_sentence)
        for match_id, start, end in distance_year_matches:
            span = doc_sentence[start:end]
            if doc.vocab.strings[match_id] == "DISTANCE_TRAVELLED":
                extracted_data["Customer_Requirements"]["Distance_Travelled"] = span.text
            elif doc.vocab.strings[match_id] == "MAKE_YEAR":
                extracted_data["Customer_Requirements"]["Make_Year"] = span.text

    return extracted_data
def extract_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return extract_data(text)

def extract_from_txt(txt_file):
    with open(txt_file, 'r') as file:
        text = file.read().lower()
        return extract_data(text)

def save_to_json(data, output_file):
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            if filename.endswith('.pdf'):
                data = extract_from_pdf(filepath)
            elif filename.endswith('.txt'):
                data = extract_from_txt(filepath)
            else:
                return "Unsupported file format. Please upload a PDF or TXT file."

            report_filename = f"{os.path.splitext(filename)[0]}_report.json"
            report_filepath = os.path.join(app.config['REPORT_FOLDER'], report_filename)
            save_to_json(data, report_filepath)

            return redirect(url_for('report', report_filename=report_filename))

    return render_template('index.html')

@app.route('/report/<report_filename>')
def report(report_filename):
    report_filepath = os.path.join(app.config['REPORT_FOLDER'], report_filename)
    with open(report_filepath, 'r') as file:
        report_data = json.load(file)
    return render_template('report.html', data=report_data)

if __name__ == '__main__':
    port = 5000
    app.run(port=port)
