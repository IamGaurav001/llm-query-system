import google.generativeai as genai

genai.configure(api_key="AIzaSyDLCPcOEhxFsJ2Y2jKfNYTh8zk7XQTUm9U")  # <-- add this line

models = genai.list_models()
for model in models:
    print(model)