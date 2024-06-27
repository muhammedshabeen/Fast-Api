from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn


app = FastAPI()




@app.get('/blog')
def get_blog(limit = 10 ,published: bool = True, sort:Optional[str] = None):
    if published:
        return {"data":f"{limit} published blog from the db"}
    else:
        return {"data":f"{limit} blog from the db"}
    



class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = None


@app.post('/create-post')
def create_post(blog: Blog):
    return {"data":f"Blog is created with title {blog.title}"}





# if __name__ == '__blog__':
#     uvicorn.run(app,host="127.0.0.1", port=9000)