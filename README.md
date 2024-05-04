
# Currency Parser


This project is a Streamlit app that parses data from Finmarket and Iban and generate chart from parsed SQL data.

*Developer: Mariia Salikova*
  

## Getting Started

  

1.  **Clone the repository:**

  

```bash

git  clone  https://github.com/mariiasalikova/currencyParser.git

```
---
2. **Bulid and run docker:**


```bash

docker build -t my_app .
docker run --name streamlit my_app

```

----

**OR, IF YOU GETTING TROUBLES**

2.  **Install the required packages:**

  

- Create a virtual environment and activate it:

  

```bash

python  -m  venv  venv

source  venv/bin/activate  # On Windows, use `venv\Scripts\activate`

```  

- Install the required packages using pip:


```bash

pip  install  -r  requirements.txt

```
  

**3. Run the application:**

  
```bash
streamlit run main.py
```