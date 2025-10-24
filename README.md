# SOI Evaluation Framework

## Setup

1.Open directory in shell
2.Create python virtual environment
```bash
pip -m venv venv
```
3.Activate virtual environment <br />
Mac/Linux
```bash
source venv/bin/activate
```
Windows
```
```bash
venv\Scripts\activate
```
4.Install requirements
```bash
pip install -r requirements.txt
```
5.Get app password for smtp<br />
https://myaccount.google.com/u/0/apppasswords<br />
6.Get AI API key<br />
https://aistudio.google.com/api-keys<br />
7.Make ".env" file
```bash
EMAIL = 'youremailhere@here.com'
PASSWORD = 'app password here from step 5'
AI_API_KEY ='AI_API_KEY_HERE'
```
8.With virtual environment on (step 3) run the app
```bash
python app.py
```
