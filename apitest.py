from datetime import datetime
from mimetypes import init
from typing import List, Union
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound
from typing import List, Tuple, Dict
import pickle as pkl 
import os.path
import os

app=FastAPI()

# STATUS_CODES
API_CALL_SUCCESS = 0
API_FAIL_INVALID_CUSTOMER = 1
API_FAIL_INVALID_PRODUCT = 2
API_FAIL_REC_FAIL = 3

STATUS_CODE = "statusCode"
MESSAGE = "message"
DATA = "data"

store1_model = None

model_list = {
    'store1':store1_model
}

@app.get("/item_rec/status", tags=["recommend"])
async def read_status():
    return {
        STATUS_CODE: API_CALL_SUCCESS,
        MESSAGE: "ready"
    }
   
@app.get('/item_rec/{customer_id}/',tags=['recommend'])
async def check_customer(customer_id:int):
    try:
        file_exists=os.path.exists(customer_id+'_model\.bin')
        if file_exists==True : 
            return #item_rec value
        else:
            print('Input the correct customer ID') 
            # status code message
    except ValueError:
        return {
            STATUS_CODE: API_FAIL_INVALID_CUSTOMER,
            MESSAGE : "Invalid customer id %d" %(customer_id)
        }

@app.get("/item_rec/{customer_id}/{product_id}",tags=['recommend'])
async def check_product(customer_id:int, product_id:int):
    try:
        file_exists=os.path.exists(customer_id+'_model\.bin')
        if file_exists==True :
            return {
                STATUS_CODE : API_CALL_SUCCESS,
                MESSAGE : 'success',
                DATA:{
                    'customer_id':customer_id,
                    'product_id':product_id
                }
            }
        else:
            return{
                STATUS_CODE : API_FAIL_INVALID_PRODUCT,
                MESSAGE :'There is no product id %d'(product_id)
            }
        
    except NoResultFound:
        return {
            STATUS_CODE : API_FAIL_REC_FAIL
        }