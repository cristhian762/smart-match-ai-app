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
```

Baixe os currículos base para o banco de dados vetorial, crie uma pasta e descompacte o zip:

```bash
wget https://github.com/florex/resume_corpus/raw/refs/heads/master/resumes_corpus.zip
mkdir -p resumes/original
unzip resumes_corpus.zip -d resumes/original
rm resumes_corpus.zip
```


Rode o script `filtered.py` para descartar os currículo inválidos:

```bash
python scripts/filtered.py
```

Rode o script `chroma.py` para gerar os bancos de dados vetoriais: 

```bash
python scripts/chroma.py
`

Run: 
```bash
uvicorn app:app
```
