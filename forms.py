from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email

def consentCheck(form, consent):
    if consent.data == False:
        raise ValidationError('Please check "Saya setuju data akan digunakan untuk analisis".')

class ProfileForm(FlaskForm):
    profile = RadioField('Anda mengisi sebagai', choices=[('perusahaan','perusahaan'),('individu','individu')], validators=[DataRequired()])
    nama = StringField("Nama Lengkap", render_kw={"placeholder": "Tulis nama lengkap"}, validators=[DataRequired()])
    perusahaan = StringField("Perusahaan/Organisasi", render_kw={"placeholder": "Kosongkan jika individu"})
    role = StringField("Jabatan/Peran", render_kw={"placeholder": "Opsional"})
    email = StringField("Email", render_kw={"placeholder": "Opsional"})
    consent = BooleanField("Saya setuju data akan digunakan untuk analisis", validators=[consentCheck])
    submit = SubmitField("Submit")

class AssessmentForm(FlaskForm):
    fi1 = RadioField(u'Inovasi berfokus pada peningkatan efisiensi teknis produksi', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    fi2 = RadioField(u'Inovasi melibatkan pengembangan SDM dan organisasi', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    fi3 = RadioField(u'Inovasi diarahkan untuk perubahan perilaku konsumen/masyarakat', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    fi4 = RadioField(u'Perusahaan memiliki strategi jangka panjang untuk inovasi berkelanjutan', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    fk1 = RadioField(u'Inovasi paling utama ditujukan pada efisiensi ekonomi dan kepatuhan regulasi', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    fk2 = RadioField(u'Aspek lingkungan/sosial dipertimbangkan dalam inovasi', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    fk3 = RadioField(u'Inovasi menciptakan nilai ekonomi, sosial, dan lingkungan secara seimbang', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    fk4 = RadioField(u'Perusahaan memiliki komitmen jelas pada prinsip triple bottom line (ekonomi, sosial, lingkungan)', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    in1 = RadioField(u'Praktik keberlanjutan dalam inovasi masih berdiri sendiri di unit tertentu', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    in2 = RadioField(u'Sebagian unit/divisi menerapkan keberlanjutan dalam inovasi', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    in3 = RadioField(u'Inovasi berkelanjutan sudah menjadi budaya organisasi', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    in4 = RadioField(u'Karyawan di berbagai level dilibatkan aktif dalam inisiatif inovasi berkelanjutan', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    ek1 = RadioField(u'Perusahaan jarang bekerja sama dengan pihak eksternal', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    ek2 = RadioField(u'Ada kerja sama terbatas dengan mitra eksternal', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    ek3 = RadioField(u'Perusahaan membangun jaringan kolaborasi luas & strategis', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    ek4 = RadioField(u'Perusahaan berbagi pengetahuan/inovasi dengan komunitas atau industri lain untuk mendorong keberlanjutan', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    am1 = RadioField(u'Fokus pada pemanfaatan teknologi/proses yang ada', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    am2 = RadioField(u'Mulai mengeksplorasi ide-ide baru di samping pemanfaatan yang ada', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    am3 = RadioField(u'Seimbang antara eksplorasi ide baru & pemanfaatan teknologi/proses yang ada', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    am4 = RadioField(u'Perusahaan berinvestasi dalam R&D untuk menciptakan inovasi baru tanpa mengabaikan efisiensi saat ini', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    da1 = RadioField(u'Perhatian keberlanjutan terbatas pada tahap produksi/manufaktur', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    da2 = RadioField(u'Keberlanjutan dipertimbangkan pada tahap penggunaan/akhir masa pakai', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    da3 = RadioField(u'Inovasi mencakup seluruh siklus hidup produk (desain-produksi-pakai-daur ulang)', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    da4 = RadioField(u'Perusahaan berupaya mengurangi dampak lingkungan dari produk sejak tahap desain awal', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    submit = SubmitField("Submit")

