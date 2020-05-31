import config
import json

MODULE_PATH='env_lang'

def get(key):
    lang_data={}
    with open(MODULE_PATH+'/'+'%s.json' % (config.env),'r') as language_file:
        lang_data=json.loads(language_file.read())
    key_arr=key.split('.')
    result=lang_data
    for one_key in key_arr:
        if one_key in result:
            result=result[one_key]
        else:
            return key
    if not isinstance(result,str):
        return key
    return result