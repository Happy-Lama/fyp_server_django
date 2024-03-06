from rest_framework import serializers
from .models import TransformerData, TransformerSpecification
from django.db.models import Max, Avg, Min, F
from django.utils import timezone
import pandas as pd
from django.db.models import Func, FloatField

class TransformerSpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransformerSpecification
        fields = '__all__'



class TransformerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransformerData
        fields = '__all__'

    def percentage_transformer_loading(self, transformer_rating, *apparent_power):
        # if type(apparent_power[0]) == type(list):
            # total_apparent_power = sum(apparent_power)
        total_apparent_power = sum(apparent_power)
        return (total_apparent_power/(transformer_rating*1000))*100
    
    def get_latest_data(self):
        transformers_with_latest_data = []
        transformers = TransformerSpecification.objects.all()
        for transformer_spec in transformers:
            latest_data = transformer_spec.transformerdata_set.order_by('-timestamp').first()
            transformer = TransformerSpecificationsSerializer(transformer_spec)
            transformer_data = transformer.data
            transformer_data['percentage_loading'] = self.percentage_transformer_loading(transformer_data['power_rating'], latest_data.out_sa, latest_data.out_sb, latest_data.out_sc)
            transformer_data['status'] = latest_data.status

            transformers_with_latest_data.append(transformer_data)

        return transformers_with_latest_data
    
    def get_overall_data(self):
        # fill in percentage loading values and put dictionaries in a list
        data = []
        transformers = TransformerSpecification.objects.all()
        for transformer in transformers:
            latest_data = transformer.transformerdata_set.order_by('-timestamp').first()
            latest_data = self.__class__(latest_data).data
            latest_data['percentage_loading'] = self.percentage_transformer_loading(transformer.power_rating, latest_data['out_sa'], latest_data['out_sb'], latest_data['out_sc'])
            data.append(latest_data)

        output = {}
        # loading
        output['min_loading'] = min(data, key=lambda x: x['percentage_loading'])
        output['max_loading'] = max(data, key=lambda x: x['percentage_loading'])
        output['avg_loading'] = sum(_['percentage_loading'] for _ in data) / len(data)
        # transformer stats
        output['number_overloaded'] = sum(_['status'] == 'OVERLOADED' for _ in data)
        output['number_off'] = sum(_['status'] == 'OFF' for _ in data)
        output['number_on'] = sum(_['status'] in ['ON', 'OVERLOADED']  for _ in data)
        # output['number_on_not_overloaded'] = sum(_['status'] =='ON' for _ in data)
        output['number_registered'] = len(transformers)
        # frequency
        output['min_freq'] = min(data, key=lambda x: x['out_freq'])
        output['max_freq'] = max(data, key=lambda x: x['out_freq'])
        output['avg_freq'] = sum(_['out_freq'] for _ in data) / len(data)
        # voltage
        output['min_ua'] = min(data, key=lambda x: x['out_ua'])
        output['max_ua'] = max(data, key=lambda x: x['out_ua'])
        output['avg_ua'] = sum(_['out_ua'] for _ in data) / len(data)

        output['min_ub'] = min(data, key=lambda x: x['out_ub'])
        output['max_ub'] = max(data, key=lambda x: x['out_ub'])
        output['avg_ub'] = sum(_['out_ub'] for _ in data) / len(data)

        output['min_uc'] = min(data, key=lambda x: x['out_uc'])
        output['max_uc'] = max(data, key=lambda x: x['out_uc'])
        output['avg_uc'] = sum(_['out_uc'] for _ in data) / len(data)


        return output

        
    def moving_average(self, startTime, interval):

        data = TransformerData.objects.filter(timestamp__gte=startTime).order_by('timestamp').annotate(
                rating=F('transformer_id__power_rating')
            ).values('timestamp', 'out_sa', 'out_sb', 'out_sc', 'out_ua', 'out_ub', 'out_uc', 'rating', 'out_freq')
        
        data_df = pd.DataFrame(list(data))
        data_df.set_index('timestamp', inplace=True)

        loading_percentage = []
        for idx, row in data_df.iterrows():
            # print(row)
            loading_percentage.append(self.percentage_transformer_loading(row['rating'], row['out_sa'], row['out_sb'], row['out_sc']))

        data_df['loading_percentage'] = loading_percentage
        
        rolling_stats = data_df.rolling(window=f'{interval}min').agg({
                'loading_percentage':['min', 'max', 'mean'], 
                'out_ua': ['min', 'max', 'mean'],
                'out_ub': ['min', 'max', 'mean'],
                'out_uc': ['min', 'max', 'mean'],
                'out_freq': ['min', 'max', 'mean'],
            })
        
        # print(rolling_stats.to_dict())
        dict_data = rolling_stats.to_dict()
        dict_ = {str(key): {str(key1): value1 for key1, value1 in value.items()} for key, value in dict_data.items()}
        # print(dict_)
        return dict_

    def transformer_data(self, transformer_id):
        transformer_data = TransformerSpecification.objects.get(transformer_id=transformer_id).transformerdata_set.order_by('timestamp')
        return self.__class__(transformer_data, many=True).data

