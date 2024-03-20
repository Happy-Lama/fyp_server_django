from django.shortcuts import render, HttpResponse
from .models import TransformerData, TransformerSpecification
from django.views.decorators.csrf import csrf_exempt 
import json
from . import utils
from django.utils import timezone
from .serializers import TransformerDataSerializer
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
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        devUID = data.get('devEUI', None)
        payload = data.get('payload', None)

        if devUID and payload:
            decoded_payload = utils.decode_uplink(payload)
            print(decoded_payload)   
            # check if the devEUI exists
            transformer = TransformerSpecification.objects.get(transformer_id=devUID)

            if transformer:
                transformer_instance = TransformerData(
                    transformer_id=transformer,
                    timestamp = timezone.now(),

                    # output phase voltages
                    out_ua = decoded_payload['line_to_neutral'][0],
                    out_ub = decoded_payload['line_to_neutral'][1],
                    out_uc = decoded_payload['line_to_neutral'][2],

                    # output phase currents
                    out_ia = decoded_payload['phase_current'][0],
                    out_ib = decoded_payload['phase_current'][1],
                    out_ic = decoded_payload['phase_current'][2],

                    # output line to line voltages
                    out_uab = decoded_payload['line_to_neutral'][1] + decoded_payload['line_to_neutral'][0],
                    out_ubc = decoded_payload['line_to_neutral'][2] + decoded_payload['line_to_neutral'][1],
                    out_uca = decoded_payload['line_to_neutral'][0] + decoded_payload['line_to_neutral'][2],

                    # output active phase power
                    out_pa = decoded_payload['active_power_per_phase'][0],
                    out_pb = decoded_payload['active_power_per_phase'][1],
                    out_pc = decoded_payload['active_power_per_phase'][2],

                    # output reactive phase power
                    out_qa = decoded_payload['reactive_power_per_phase'][0],
                    out_qb = decoded_payload['reactive_power_per_phase'][1],
                    out_qc = decoded_payload['reactive_power_per_phase'][2],

                    # output apparent phase power
                    out_sa = decoded_payload['apparent_power_per_phase'][0],
                    out_sb = decoded_payload['apparent_power_per_phase'][1],
                    out_sc = decoded_payload['apparent_power_per_phase'][2],

                    # output power factor per phase
                    # out_pha = models.FloatField(default=0)
                    # out_phb = models.FloatField(default=0)
                    # out_phc = models.FloatField(default=0)

                    # output frequency
                    out_freq = decoded_payload['frequency'],

                    status = 'ON' if decoded_payload['status'] == 1 else 'OFF'
                )

                if transformer_instance.status == 'ON':
                    overloaded = TransformerDataSerializer().percentage_transformer_loading(transformer.power_rating, transformer_instance.out_sa, transformer_instance.out_sb, transformer_instance.out_sc) >= 0.9

                    if overloaded:
                        transformer_instance.status = 'OVERLOADED'
                
                transformer_instance.save()

            return HttpResponse(status=200)
    return HttpResponse(status=405)       

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
        print(data)
        # if devUID:
        #     transformer = TransformerSpecification.objects.get(transformer_id=devUID)
            
        #     if transformer != None:
        #         payload = data.get('data', None)

        #         if devUID and payload:
        #             decoded_payload = utils.decode_uplink(payload)
        #             print(decoded_payload)   
        #             # check if the devEUI exists
        #             transformer = TransformerSpecification.objects.get(transformer_id=devUID)

        #             if transformer:
        #                 transformer_instance = TransformerData(
        #                     transformer_id=transformer,
        #                     timestamp = timezone.now(),

        #                     # output phase voltages
        #                     out_ua = decoded_payload['line_to_neutral'][0],
        #                     out_ub = decoded_payload['line_to_neutral'][1],
        #                     out_uc = decoded_payload['line_to_neutral'][2],

        #                     # output phase currents
        #                     out_ia = decoded_payload['phase_current'][0],
        #                     out_ib = decoded_payload['phase_current'][1],
        #                     out_ic = decoded_payload['phase_current'][2],

        #                     # output line to line voltages
        #                     out_uab = decoded_payload['line_to_neutral'][1] + decoded_payload['line_to_neutral'][0],
        #                     out_ubc = decoded_payload['line_to_neutral'][2] + decoded_payload['line_to_neutral'][1],
        #                     out_uca = decoded_payload['line_to_neutral'][0] + decoded_payload['line_to_neutral'][2],

        #                     # output active phase power
        #                     out_pa = decoded_payload['active_power_per_phase'][0],
        #                     out_pb = decoded_payload['active_power_per_phase'][1],
        #                     out_pc = decoded_payload['active_power_per_phase'][2],

        #                     # output reactive phase power
        #                     out_qa = decoded_payload['reactive_power_per_phase'][0],
        #                     out_qb = decoded_payload['reactive_power_per_phase'][1],
        #                     out_qc = decoded_payload['reactive_power_per_phase'][2],

        #                     # output apparent phase power
        #                     out_sa = decoded_payload['apparent_power_per_phase'][0],
        #                     out_sb = decoded_payload['apparent_power_per_phase'][1],
        #                     out_sc = decoded_payload['apparent_power_per_phase'][2],

        #                     # output power factor per phase
        #                     # out_pha = models.FloatField(default=0)
        #                     # out_phb = models.FloatField(default=0)
        #                     # out_phc = models.FloatField(default=0)

        #                     # output frequency
        #                     out_freq = decoded_payload['frequency'],

        #                     status = 'ON' if decoded_payload['status'] == 1 else 'OFF'
        #                 )

        #                 if transformer_instance.status == 'ON':
        #                     overloaded = TransformerDataSerializer().percentage_transformer_loading(transformer.power_rating, transformer_instance.out_sa, transformer_instance.out_sb, transformer_instance.out_sc) >= 0.9

        #                     if overloaded:
        #                         transformer_instance.status = 'OVERLOADED'
                        
        #                 transformer_instance.save()

        return HttpResponse(status=200)
    return HttpResponse(status=405)