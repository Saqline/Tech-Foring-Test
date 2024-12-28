Tech-Foring-Test 
1. create Virtual Environment from project root folder:
python -m venv venv

2. Activate Virtual Environment:
On Windows: 
venv\Scripts\activate

On macOS/Linux:
source venv/bin/activate

3. Install Dependencies:
pip install -r requirements.txt

4. Migration DB:
python manage.py makemigrations
python manage.py migrate

5. run server:
python manage.py runserver

6. Watch Swagger Documentation:
http://127.0.0.1:8000/api/schema/swagger-ui/

Then in User Section
/api/api/users/register/  -for register and
/api/api/users/login/   -for login with unique username and password during register.









Or For Docker Run :

1. docker build -t project_management .
2. docker run -p 8000:8000 project_management

Then Watch Swagger Documentation:
http://127.0.0.1:8000/api/schema/swagger-ui/
  
Verify docker run : 
docker ps


