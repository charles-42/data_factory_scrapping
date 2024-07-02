Il faut avoir installer azure-functions-core-tools@4 sur votre ordinateur

python3.11 -m venv env
activate virtual env

pip install scrapy azure-functions SQLAlchemy psycopg2-binary python-dotenv
pip freeze > requirements.txt 

func init AllocineFolder --worker-runtime python --model V2 

cd AllocineFolder

func new --template "Http Trigger" --name MyHttpTrigger --authlevel "anonymous"

to test:
func start         