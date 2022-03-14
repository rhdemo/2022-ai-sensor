# For sample predict functions for popular libraries visit https://github.com/opendatahub-io/odh-prediction-samples

# Import libraries
# import tensorflow as tf

# Load your model.
# model_dir = 'models/myfancymodel'
# saved_model = tf.saved_model.load(model_dir)
# predictor = saved_model.signatures['default']


# Write a predict function
import config
import utils

cals = utils.read_json(config.cals_loc)
fields = utils.read_json(config.fields_loc)

def predict(data, cals, fields):
    '''Input is data packet
    '''
    
    #data = args_dict['data']
    #cals = args_dict['cals']
    #fields = args_dict['fields']
    
    res = {}
    
    for f in data['features']: #'acc', 'led_1' etc.
        res = {}
        if f=='accelerometer':
            val = 0
            for k in fields[f]:
                val += data['features'][f][k]**2
            val = np.sqrt(val)

            k = 'mag'
            r = (val > cals[data['deviceuid']][f'{f}_{k}']['low']) and (val < cals[data['deviceuid']][f'{f}_{k}']['high'])
            
        else:
            for k in fields[f]:
                
                val = data['features'][f][k]
                
                r = (val > cals[data['deviceuid']][f'{f}_{k}']['low']) and (val < cals[data['deviceuid']][f'{f}_{k}']['high'])
                
                res[f'{f}_{k}'] = r
        
    return res
