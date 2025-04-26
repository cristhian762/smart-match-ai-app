Clone o repositório e acesse a pasta ´smart-match-ai-app´:

```bash
git clone ...
cd smart-match-ai-app
```

Criei o ambiente virtual e instale as dependências do projeto:


```bash
python -m venv venv/
source venv/bin/activate
pip install -r requirements.txt
pip install uvicorn
```

Baixe os currículos base para o banco de dados vetorial, crie uma pasta e descompacte o zip:

```bash
wget https://github.com/florex/resume_corpus/raw/refs/heads/master/resumes_corpus.zip
mkdir resumes
unzip resumes_corpus.zip -d resumes/ 
rm resumes_corpus.zip
```

Run: 
```bash
uvicorn app:app
```
