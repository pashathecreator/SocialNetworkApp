import logging

from fastapi import FastAPI

from .routers import post, user, authentication, vote

from fastapi.middleware.cors import CORSMiddleware


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d #%(levelname)-8s "
    "[%(asctime)s] - %(name)s - %(message)s",
)



app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)

logger.error("gasgsag")


@app.get("/")
def root():
    return {"message": "Hello World"}
