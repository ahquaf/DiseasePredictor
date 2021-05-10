import shutil

from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename
import joblib
from authentication_model import database, login, UserModel, DoctorModel, AcceptConsultancy, AdminModel
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime

model = joblib.load('trained_model3.pkl')
countvec = joblib.load('countvector_transformer.pkl')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/mysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = 'static/images/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg', 'gif'}

app.secret_key = 'kjdsgoign!3942309zkfnsd804t80u3'

database.init_app(app)
login.init_app(app)
login.login_view = 'index'

spec = ''

#list of symptoms

l1=['itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain',
  'stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_ urination',
  'fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy',
  'patches_in_throat','irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating',
  'dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes',
  'back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
  'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
  'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
  'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
  'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
  'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
  'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
  'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
  'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
  'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
  'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
  'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
  'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
  'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum',
  'rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion',
  'receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen',
  'history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf',
  'palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
  'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose',
  'yellow_crust_ooze']

#Diseases in the data set
disease=['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction','Peptic ulcer diseae','AIDS','Diabetes ',
  'Gastroenteritis','Bronchial Asthma','Hypertension ','Migraine','Cervical spondylosis','Paralysis (brain hemorrhage)',
  'Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
  'Hepatitis E', 'Alcoholic hepatitis','Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
  'Heart attack', 'Varicose veins','Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
  'Arthritis', '(vertigo) Paroymsal  Positional Vertigo','Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']



def predict_disease(symptomData):

    cleaned_data = symptomData[0] + " " + symptomData[1] + " " + symptomData[2] + " " + symptomData[3] + " " + symptomData[4]
    x_new_count = countvec.transform([cleaned_data])
    print(x_new_count.shape)

    #predictInput = [l2]
    predict = model.predict(x_new_count)
    predicted = predict[0]
    hasDisease = 'no'
    disease_name = disease[predicted]

    for num in range(0, len(disease)):
        if(predicted == num):
            hasDisease = 'yes'
            break

    if(hasDisease == 'yes'):
        probabilityScore = model.predict_proba(x_new_count)
        confidenceScore = probabilityScore.max()*100

    Rheumatologist = ['Osteoarthristis', 'Arthritis']

    Cardiologist = ['Heart attack', 'Bronchial Asthma', 'Hypertension ']

    ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo', 'Hypothyroidism']

    Orthopedist = []

    Neurologist = ['Varicose veins', 'Paralysis (brain hemorrhage)', 'Migraine', 'Cervical spondylosis']

    Allergist_Immunologist = ['Allergy', 'Pneumonia',
                              'AIDS', 'Common Cold', 'Tuberculosis', 'Malaria', 'Dengue', 'Typhoid']

    Urologist = ['Urinary tract infection',
                 'Dimorphic hemmorhoids(piles)']

    Dermatologist = ['Acne', 'Chicken pox', 'Fungal infection', 'Psoriasis', 'Impetigo']

    Gastroenterologist = ['Peptic ulcer diseae', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Gastroenteritis',
                          'Hepatitis E',
                          'Alcoholic hepatitis', 'Jaundice', 'hepatitis A',
                          'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Diabetes ', 'Hypoglycemia']

    if disease_name in Rheumatologist:
        consultdoctor = "Rheumatologist"

    elif disease_name in Cardiologist:
        consultdoctor = "Cardiologist"

    elif disease_name in ENT_specialist:
        consultdoctor = "ENT specialist"

    elif disease_name in Orthopedist:
        consultdoctor = "Orthopedist"

    elif disease_name in Neurologist:
        consultdoctor = "Neurologist"

    elif disease_name in Allergist_Immunologist:
        consultdoctor = "Allergist/Immunologist"

    elif disease_name in Urologist:
        consultdoctor = "Urologist"

    elif disease_name in Dermatologist:
        consultdoctor = "Dermatologist"

    elif disease_name in Gastroenterologist:
        consultdoctor = "Gastroenterologist"

    else:
        consultdoctor = "other"

    return [confidenceScore, consultdoctor, disease_name]

@app.route("/patientSignIn", methods=['GET', 'POST'])
def patientSignIn():
    msg=''
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        user = UserModel.query.filter_by(email=email).first()

        if user is not None and user.check_password(password):
            session['current_user'] = 'patient'
            login_user(user)
            return redirect(url_for('profile'))
        else:
            msg='Incorrect Username/Password'

    return render_template("patientSignIn.html", msg=msg)

@app.route('/logout')
def logout():
    logout_user()
    session.pop("current_user", None)
    return redirect(url_for('index'))

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/patientSignUp', methods=['GET', 'POST'])
def patientSignUp():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        age = request.form['age']
        gender = request.form['gender']
        email = request.form['email']
        password = request.form['password']
        city = request.form['city']

        if UserModel.query.filter_by(email=email).first():
            return render_template('patientSignUp.html', msg='Email already exists')

        if UserModel.query.filter_by(username=username).first():
            return render_template('patientSignUp.html', msg='Username already exists')

        if not username or not age or not gender or not email or not password:
            return render_template('patientSignUp.html', msg='Please fill in the missing fields')

        if 'file' not in request.files:
            return render_template('patientSignUp.html', msg='No File Part')

        file=request.files['file']
        if file.filename == '':
            return render_template('patientSignUp.html', msg='Please select a file')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if filename != '':
                if os.path.exists(app.config['UPLOAD_FOLDER'] + username):
                    shutil.rmtree(app.config['UPLOAD_FOLDER'] + username)
                os.makedirs(app.config['UPLOAD_FOLDER'] + username)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'] + username, filename))
            else:
                return render_template('patientSignUp.html', msg='File Not secure')
        else:
            return render_template('patientSignUp.html', msg='Invalid File Extension!')

        password_hash=UserModel.set_password(password)
        user = UserModel(email=email, password=password_hash, gender=gender, age=age, profile_name=filename, username=username, city=city)

        database.session.add(user)
        database.session.commit()
        msg = 'Account Successfully Created'

    elif request.method == 'POST':
        msg = 'Please fill in the form'

    return render_template('patientSignUp.html', msg=msg)

@app.route("/DoctorSignIn", methods=['GET', 'POST'])
def doctorSignIn():
    msg=''
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        user = DoctorModel.query.filter_by(email=email).first()

        if user is not None and user.check_password(password):
            session['current_user'] = 'doctor'
            login_user(user)
            return redirect(url_for('profile'))
        else:
            msg='Incorrect Username/Password'

    return render_template("DoctorSignIn.html", msg=msg)

@app.route('/DoctorSignUp', methods=['GET', 'POST'])
def doctorSignUp():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    msg=''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        name = request.form['name']
        address = request.form['address']
        specialization = request.form['specialization']
        city = request.form['city']

        if DoctorModel.query.filter_by(email=email).first():
            return render_template('DoctorSignUp.html', msg='Email already exists')

        if not email or not password or not mobile or not name or not address or not specialization or not city:
            return render_template('DoctorSignUp.html', msg='Please fill in the missing fields')

        if 'file' not in request.files:
            return render_template('DoctorSignUp.html', msg='No File Part')

        file=request.files['file']
        if file.filename == '':
            return render_template('DoctorSignUp.html', msg='Please select a file')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if filename != '':
                if os.path.exists(app.config['UPLOAD_FOLDER'] + name):
                    shutil.rmtree(app.config['UPLOAD_FOLDER'] + name)
                os.makedirs(app.config['UPLOAD_FOLDER'] + name)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'] + name, filename))
            else:
                return render_template('DoctorSignUp.html', msg='File Not secure')
        else:
            return render_template('DoctorSignUp.html', msg='Invalid File Extension!')

        password_hash=DoctorModel.set_password(password)
        user = DoctorModel(email=email, password=password_hash, name=name, mobile=mobile, address=address, specialization=specialization, city=city,
                         profile_name=filename)

        database.session.add(user)
        database.session.commit()
        msg = 'Account Successfully Created'

    elif request.method == 'POST':
        msg = 'Please fill in the form'

    return render_template('DoctorSignUp.html', msg=msg)


@app.route('/consultancy', methods=['GET', 'POST'])
@login_required
def consultancy():

    if request.method == 'POST' and 'consult' in request.form:
        consultdoc = request.form['consult']
        city = current_user.city
        global spec
        spec = consultdoc
        doclist = DoctorModel.query.filter_by(city=city, specialization=consultdoc).all()
        return render_template('consultancy.html', doclist=doclist)

    if request.method == 'POST' and 'date' in request.form:
        docName = request.form['doc-name']
        docAddress = request.form['doc-address']
        docEmail = request.form['doc-email']
        docMobile = request.form['doc-mobile']
        docSpec = request.form['doc-spec']
        date = request.form['date']
        datetimeNow = datetime.now()
        dateString = datetimeNow.strftime("%Y-%m-%dT%H:%M")
        if dateString >= date:
            error_message = True
            send_msg = 'Please enter a time after the current time before submitting'
            doclist = DoctorModel.query.filter_by(city=current_user.city, specialization=spec).all()
            return render_template('consultancy.html', msg_value=error_message, error_msg=send_msg, doclist=doclist,
                                   docName=docName, docMobile=docMobile, docAddress=docAddress, docEmail=docEmail,
                                   docSpec=docSpec)
        else:
            datetime_object = datetime.strptime(date, "%Y-%m-%dT%H:%M")
            consult = AcceptConsultancy(doctor_name=docName, username=current_user.username, diseaseName=session['current_disease'],
                                        appointmentDateTime=datetime_object, status='pending')
            database.session.add(consult)
            database.session.commit()
            redirect(url_for('profile'))

    return redirect(url_for('profile'))


@app.route('/profile')
@login_required
def profile():
    currentUser = session['current_user']
    if currentUser == 'doctor':
        pathName = app.config['UPLOAD_FOLDER'] + current_user.name + '/' + current_user.profile_name
        return render_template('doctor_profile.html', path=pathName, user=current_user.name, specialization=current_user.specialization)
    elif currentUser == 'patient':
        pathName = app.config['UPLOAD_FOLDER'] + current_user.username + '/' + current_user.profile_name
        return render_template('patient_profile.html', path=pathName, user=current_user.username, gender=current_user.gender, age=current_user.age)

@app.route("/index", methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    return render_template("index.html")

@app.route("/check_disease", methods=['GET'])
@login_required
def check_disease():
    return render_template("check.html")

@app.route("/predicted_disease", methods=["POST"])
@login_required
def getSymptoms():

    Symptom1 = request.form['Symptom1']
    Symptom2 = request.form['Symptom2']
    Symptom3 = request.form['Symptom3']
    Symptom4 = request.form['Symptom4']
    Symptom5 = request.form['Symptom5']

    result = predict_disease([Symptom1, Symptom2, Symptom3, Symptom4, Symptom5])

    confidence = result[0]
    consultdoc = result[1]
    predictedDisease = result[2]

    session['current_disease'] = predictedDisease

    return render_template('prediction.html', ConfidenceScore=confidence, ConsultDoc=consultdoc, diseaseName=predictedDisease,
                           sym1=Symptom1, sym2=Symptom2, sym3=Symptom3, sym4=Symptom4, sym5=Symptom5, user=current_user.username, age=current_user.age)

if __name__ == '__main__':
    app.run(port=5000, debug=True)