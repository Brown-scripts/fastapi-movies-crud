from fastapi import FastAPI,HTTPException
import mysql.connector
from model import Movie
from dotenv import load_dotenv
import os

load_dotenv()

db_host = os.getenv('DB_HOST')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')

mydb=mysql.connector.connect(host=db_host,username=db_username,password=db_password,database="movies")

mycursor=mydb.cursor()

# uvicorn main:app --reload to run
app = FastAPI()


@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get('/movies')
def get_movies():
    query="SELECT * FROM movies"
    mycursor.execute(query)
    movies =mycursor.fetchall()
    return movies
    
@app.get("/movie/{title}")
def get_single_movie(title:str):
    query = "SELECT * FROM movies WHERE title = %s"
    mycursor.execute(query, (title,))
    movie = mycursor.fetchone()
    if movie:
        # Format the result into a dictionary
        movie_data = {
            "id": movie[0],
            "title": movie[1],
            "year": movie[2]
        }
        return movie_data
    else:
        raise HTTPException(status_code=404,detail='Movie not Found')

@app.post("/movie")
def create_movie(movie:Movie):
    query= "INSERT INTO movies(Title,Year) VALUES (%s,%s)"
    val=(movie.Title,movie.Year)
    mycursor.execute(query, val)
    mydb.commit()
    return movie


@app.put('/update_movie')
def update_movie(movie:Movie):
    query = "UPDATE movies SET Title = %s,Year= %s WHERE id= %s"
    val=(movie.Title,movie.Year,movie.id)
    mycursor.execute(query,val)
    mydb.commit()
    return movie


@app.delete('/movie/delete/{title}')
def delete_movie(title: str):
    select_query = "SELECT * FROM movies WHERE Title = %s"
    mycursor.execute(select_query, (title,))
    result = mycursor.fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    delete_query = "DELETE FROM movies WHERE Title = %s"
    mycursor.execute(delete_query, (title,))
    mydb.commit()

    return {"message": "Movie deleted successfully"}

