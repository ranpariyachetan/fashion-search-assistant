# Fashion Search Assistant
This is a search application facilitating users to search products from fashion dataset. The assistant is implemented using RAG with LlamaIndex.

## How to use
- Clone the repository on the local computer.
- Create virtual environment using env, Docker, Conda or PyCharm.
- Create .env file under the root director and add variable `OpenAI_API_Key` with valid openai api key assigned to it.
- Navigate to the root directory in terminal or command prompt.
- Run command `pip install -r requirements.text`.
- Run command `streamlit run app.py`.
- It will take a while (4-5 minutes) on first run as embeddings will be created for the entire dataset.
- The app will start and open browser with a web page.
- Enter search term such as Kurta, Stylish Top, T-Shirts, Jackets etc. in the text box and hit `Enter`.
- The app will search for the products for search terms and display results along with pictures of each searched product.
- If app is can not find any relevant product, it will display a message accordingly.
  ![searchresult1.png](../searchresult1.png)