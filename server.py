from fastapi import FastAPI, Depends, HTTPException, Request, Response

from pydantic import BaseModel

from typing import Optional



app = FastAPI()

@app.get('/')