from django.shortcuts import render
from .models import TransformerData, TransformerSpecification
from django.views.decorators.csrf import csrf_exempt 
import json
# Create your views here.


@csrf_exempt
def gsm_receive_data(request):
    # view to handle data received from gsm module
    # POST requests only
    # decode the data
    # check if transformer devUID is in the table for TransformerSpecifications
    # if true
    # extract data from the post request related to the TransformerData and create a new entry
    # else
    # ignore the request
    # on successful requests just return from the function
    pass
    

@csrf_exempt
def ttn_receive_data(request):
    # view to handle data received from the things network (LoRaWAN)
    # POST requests only
    # decode the data
    # check if transformer devUID is in the table for TransformerSpecifications
    # if true
    # extract data from the post request related to the TransformerData and create a new entry
    # else
    # ignore the request
    # on successful requests just return from the function 
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        devUID = data.get('devEUI', None)

        if devUID:
            transformer = TransformerSpecification.objects.get(transformer_id=devUID)
            
            if transformer != None:
                # save a transformerdata object with the values given from the request object
                pass