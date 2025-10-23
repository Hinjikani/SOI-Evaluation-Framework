import polars as pl
import uuid
import os
import dotenv
from plotly import utils
import plotly.express as px
from flask import Flask, render_template, redirect, url_for, session
from forms import ProfileForm, AssessmentForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from json import dumps
from send_email import sendEmail
from google import genai
from google.genai import types
import pathlib

dotenv.load_dotenv()
api_key = os.getenv("AI_API_KEY")

app = Flask(__name__)
client = genai.Client(api_key=api_key)

#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SOI.db'
app.config['SECRET_KEY'] ='secret'

db = SQLAlchemy(app)

class Profile(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64), nullable=False)
    nama = db.Column(db.String(512), nullable=False)
    nama_perusahaan = db.Column(db.String(1024), nullable=True)
    role = db.Column(db.String(1024), nullable=True)
    email = db.Column(db.String(1024), nullable=True)
    date_added = db.Column(db.DateTime, default = datetime.now(timezone.utc))
    #connecting to evaluation model
    assessment = db.relationship('Assessment', backref='profile', lazy='dynamic')
    results = db.relationship('Results', backref='profile', lazy='dynamic')

class Assessment(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    fi1 = db.Column(db.Integer, nullable=False)
    fi2 = db.Column(db.Integer, nullable=False)
    fi3 = db.Column(db.Integer, nullable=False)
    fi4 = db.Column(db.Integer, nullable=False)
    fk1 = db.Column(db.Integer, nullable=False)
    fk2 = db.Column(db.Integer, nullable=False)
    fk3 = db.Column(db.Integer, nullable=False)
    fk4 = db.Column(db.Integer, nullable=False)
    in1 = db.Column(db.Integer, nullable=False)
    in2 = db.Column(db.Integer, nullable=False)
    in3 = db.Column(db.Integer, nullable=False)
    in4 = db.Column(db.Integer, nullable=False)
    ek1 = db.Column(db.Integer, nullable=False)
    ek2 = db.Column(db.Integer, nullable=False)
    ek3 = db.Column(db.Integer, nullable=False)
    ek4 = db.Column(db.Integer, nullable=False)
    am1 = db.Column(db.Integer, nullable=False)
    am2 = db.Column(db.Integer, nullable=False)
    am3 = db.Column(db.Integer, nullable=False)
    am4 = db.Column(db.Integer, nullable=False)
    da1 = db.Column(db.Integer, nullable=False)
    da2 = db.Column(db.Integer, nullable=False)
    da3 = db.Column(db.Integer, nullable=False)
    da4 = db.Column(db.Integer, nullable=False)
    #foreign key
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    results = db.relationship('Results', backref='assessment', lazy='dynamic')

class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fokus_inovasi = db.Column(db.Float(16), nullable=False)
    fokus_keberlanjutan = db.Column(db.Float(16), nullable=False)
    integrasi_intra_organisasi = db.Column(db.Float(16), nullable=False)
    integrasi_ekstra_organisasi = db.Column(db.Float(16), nullable=False)
    ambidexterity = db.Column(db.Float(16), nullable=False)
    daur_hidup_fisik = db.Column(db.Float(16), nullable=False)
    maturity_level = db.Column(db.String(64), nullable=False)
    recommendation = db.Column(db.Text, nullable=False)
    #foreign key
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    assessment_id = db.Column(db.String(40), db.ForeignKey('assessment.id'))

@app.route("/", methods=['GET', 'POST'])
def index():
    form = ProfileForm()
    if form.validate_on_submit():
        profile = Profile(status = form.profile.data, nama = form.nama.data, nama_perusahaan = form.perusahaan.data, role = form.role.data, email = form.email.data)
        db.session.add(profile)
        db.session.commit()
        session['profile_id'] = profile.id
        return redirect(url_for('assessment'))
    return render_template("index.html",
                            form=form,
                            title="SOI Assessment")

@app.route("/assessment", methods=['GET', 'POST'])
def assessment():
    profile_id = session.get('profile_id')
    if not profile_id:
        return redirect(url_for('index'))

    form = AssessmentForm()
    if form.validate_on_submit():
        link_id = str(uuid.uuid4())
        assessment = Assessment(
            profile_id=profile_id,
            id = link_id,
            fi1=form.fi1.data,
            fi2=form.fi2.data,
            fi3=form.fi3.data,
            fi4=form.fi4.data,
            fk1=form.fk1.data,
            fk2=form.fk2.data,
            fk3=form.fk3.data,
            fk4=form.fk4.data,
            in1=form.in1.data,
            in2=form.in2.data,
            in3=form.in3.data,
            in4=form.in4.data,
            ek1=form.ek1.data,
            ek2=form.ek2.data,
            ek3=form.ek3.data,
            ek4=form.ek4.data,
            am1=form.am1.data,
            am2=form.am2.data,
            am3=form.am3.data,
            am4=form.am4.data,
            da1=form.da1.data,
            da2=form.da2.data,
            da3=form.da3.data,
            da4=form.da4.data,
            )
        db.session.add(assessment)
        db.session.commit()

        #Sending email
        recipients = Profile.query.get_or_404(profile_id).email
        nama = Profile.query.get_or_404(profile_id).nama
        if Profile.query.get_or_404(profile_id).email == "":
            session['link_id'] = link_id
            return redirect(url_for('results', link_id=link_id))
        elif Profile.query.get_or_404(profile_id).nama_perusahaan != "":
            company_name = Profile.query.get_or_404(profile_id).nama_perusahaan
            sendEmail(recipients, nama, link_id, company_name)
        else:
            sendEmail(recipients, nama)
        
        session['link_id'] = link_id

        return redirect(url_for('results', link_id=link_id))
    return render_template("assessment.html",
                            form=form,
                            title="SOI Assessment"
                            )

@app.route('/results/<string:link_id>')
def results(link_id):
    if result := Results.query.filter_by(assessment_id=link_id).first():
        FokusInovasiScore = result.fokus_inovasi
        FokusKeberlanjutanScore = result.fokus_keberlanjutan 
        IntegrasiIntraOrganisasiScore = result.integrasi_intra_organisasi
        IntegrasiEkstraOrganisasiScore = result.integrasi_ekstra_organisasi
        AmbidexterityScore = result.ambidexterity
        DaurHidupFisikScore = result.daur_hidup_fisik
        maturity_level = result.maturity_level
        response = result.recommendation

        def kategori(avg: float) -> str:
            if avg <= 2.5:
                return "Basic (Operational Optimisation)"
            if avg <= 3.5:
                return "Intermediate (Organisational Transformation)"
            return "Advance (Systems Building)"

        df = pl.DataFrame({
            "score": [FokusInovasiScore, FokusKeberlanjutanScore, IntegrasiIntraOrganisasiScore, IntegrasiEkstraOrganisasiScore, AmbidexterityScore, DaurHidupFisikScore],
            "dimensi": ["Fokus Inovasi", "Fokus Keberlanjutan", "Integrasi Intra Organisasi", "Integrasi Ekstra Organisasi", "Ambidexterity", "Daur Hidup Fisik"],
            "kategori": [kategori(FokusInovasiScore), kategori(FokusKeberlanjutanScore), kategori(IntegrasiIntraOrganisasiScore), kategori(IntegrasiEkstraOrganisasiScore), kategori(AmbidexterityScore), kategori(DaurHidupFisikScore)]
        })

        #Two decimal score
        df = df.with_columns(
            pl.col("score").round(2).alias("score_text")
        )
        fig = px.line_polar(df.to_pandas(), r='score', theta='dimensi', line_close=True)
        fig.update_traces(fill='toself', mode='lines+markers+text', textfont_size=14)
        # Set the range of the radial axis from 0 to 5
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            font_size=14,
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=150, r=180, t=80, b=80)
        )
        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        result = df.to_dict()

        return render_template('results.html',
                            chart_html=chart_html,
                            title="SOI Assessment Results",
                            result=result,
                            maturity_level=maturity_level,
                            response = response)
    else:
        link_id = Assessment.query.get_or_404(link_id)
        FokusInovasiScore = (link_id.fi1 + link_id.fi2 + link_id.fi3 + link_id.fi4)/4
        FokusKeberlanjutanScore = (link_id.fk1 + link_id.fk2 + link_id.fk3 + link_id.fk4)/4
        IntegrasiIntraOrganisasiScore = (link_id.in1 + link_id.in2 + link_id.in3 + link_id.in4)/4
        IntegrasiEkstraOrganisasiScore = (link_id.ek1 + link_id.ek2 + link_id.ek3 + link_id.ek4)/4
        AmbidexterityScore = (link_id.am1 + link_id.am2 + link_id.am3 + link_id.am4)/4
        DaurHidupFisikScore = (link_id.da1 + link_id.da2 + link_id.da3 + link_id.da4)/4

        def kategori(avg: float) -> str:
            if avg <= 2.5:
                return "Basic (Operational Optimisation)"
            if avg <= 3.5:
                return "Intermediate (Organisational Transformation)"
            return "Advance (Systems Building)"

        df = pl.DataFrame({
            "score": [FokusInovasiScore, FokusKeberlanjutanScore, IntegrasiIntraOrganisasiScore, IntegrasiEkstraOrganisasiScore, AmbidexterityScore, DaurHidupFisikScore],
            "dimensi": ["Fokus Inovasi", "Fokus Keberlanjutan", "Integrasi Intra Organisasi", "Integrasi Ekstra Organisasi", "Ambidexterity", "Daur Hidup Fisik"],
            "kategori": [kategori(FokusInovasiScore), kategori(FokusKeberlanjutanScore), kategori(IntegrasiIntraOrganisasiScore), kategori(IntegrasiEkstraOrganisasiScore), kategori(AmbidexterityScore), kategori(DaurHidupFisikScore)]
        })

        #Two decimal score
        df = df.with_columns(
            pl.col("score").round(2).alias("score_text")
        )
        fig = px.line_polar(df.to_pandas(), r='score', theta='dimensi', line_close=True)
        fig.update_traces(fill='toself', mode='lines+markers+text', textfont_size=14)
        # Set the range of the radial axis from 0 to 5
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            font_size=14,
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=150, r=150, t=80, b=80)
        )
        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        result = df.to_dict()
        maturity_level = kategori(df['score'].mean())

        #AI Recommendations
        scores = df['score'].to_list()
        profile_id = link_id.profile_id
        profile = Profile.query.get_or_404(profile_id)
        company_name = profile.nama_perusahaan
        research_file = pathlib.Path('research.pdf')
        prompt = f"""You are a sustainability expert, focusing in sustainability oriented innovation. You will create few recommendations served in bullet points based on the research paper provided the output will be in HTML format that is compatible to be inside <body> tag, your output won't have any text other than what's compatible inside the <body> tag, don't say html on the start of your sentence. You are given few scores that are the results of lickert scale 1-5 assessment, {company_name} have these scores:
        Innovation focus = {scores[0]}
        Sustainability focus = {scores[1]}
        intra-organisational integration = {scores[2]}
        Inter-organisational integration = {scores[3]}
        ambidexterity = {scores[4]}
        physical life cycle = {scores[5]}
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=research_file.read_bytes(),
                    mime_type="application/pdf"
                ),
                prompt
            ]
        )

        #Add to Database
        results = Results(
            fokus_inovasi = FokusInovasiScore,
            fokus_keberlanjutan = FokusKeberlanjutanScore,
            integrasi_intra_organisasi = IntegrasiIntraOrganisasiScore,
            integrasi_ekstra_organisasi = IntegrasiEkstraOrganisasiScore,
            ambidexterity = AmbidexterityScore,
            daur_hidup_fisik = DaurHidupFisikScore,
            maturity_level = maturity_level,
            recommendation = response.text,
            profile_id = profile_id,
            assessment_id = link_id.id
        )
        db.session.add(results)
        db.session.commit()
        return render_template('results.html',
                            chart_html=chart_html,
                            title="SOI Assessment Results",
                            result=result,
                            maturity_level=maturity_level,
                            response = response.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)