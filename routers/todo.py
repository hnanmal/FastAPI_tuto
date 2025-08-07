from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(prefix="/todos", tags=["todos"])
