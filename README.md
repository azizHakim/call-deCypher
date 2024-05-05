# RAG application for analyzing call logs

It takes in multiple call logs as text file and a question about the calls. The call logs are then extracted and indexed in a vector store with langchain. Then necessary facts are retreived according to the question. We have combined two chains: `facts_chain` extracts the necessary facts and finally `refine_facts_chain` return the answer by removing unnecessary facts.

Checkout the live version [here](https://rag-chatapp-sbeilyjgrq-uc.a.run.app/) (deployed on GCP with cloud build and cloud run).


### ✔️ Installation and Runnning
1. Get the repo: 
   - `git clone git@github.com:azizHakim/call-deCypher.git`
2. cd into the root directory: 
   - `cd call-deCypher`
3. Rename `env.sample` to `.env`:  
    - `mv env.sample .env`
4. Assign your openai api key to `OPENAI_API_KEY` variable inside `.env`
3. Build the docker image: 
    - `docker build . -t calldecypher`
4. Run the docker image: 
     - `docker run -p 5000:5000 calldecypher`
5. Finally go to `http://localhost:5000` to enjoy the app


### 🦾 Tests
Wrote tests for apis and webpage.

Run the tests
- `pytest`


### ⚙️ Tech stack
- FLask
- OpenAI API
- LangChain
- uWSGI
- Docker

## 📫 How to reach me 

Feel free to reach out to me on [Twitter](https://twitter.com/aziz_raihan19) or [LinkedIn](https://www.linkedin.com/in/aziz-hakim) for collaboration. Know more about me at [azizhakim.github.io](https://azizhakim.github.io)

[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/aziz_raihan19)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:hakim.smazizul@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/aziz-hakim)