
#### Expands all keys in input json data that has key name ending in a given suffix (i.e. __csv),
#       and value is a string, into a list i.e. csv fields are converted into a list. The original 
#       key name is renamed removing the suffix (i.e. __csv) from it i.e. host__csv becomes host
def json_csv_key_to_list(
    data,               # json data
    csv_suffix,         # key suffix to identity it's value is a csv string
    ):
    
    # A helper function to iterate over a collection regardless its a list or a dict
    def get_next_item(d):
        if isinstance(d, list):
            for k,v in enumerate(d):
                yield (k, v)
        elif isinstance(d, dict):
            for k,v in d.items():
                yield (k, v)
                
    try:
        if isinstance(data, list):
            d_type = 'l'
            jd2 = list()
        elif isinstance(data, dict):
            d_type = 'd'
            jd2 = dict()
            
        # for each item in the collection (list or dict)
        for k1,v1 in get_next_item(data):
            # if item is dict, val str & key ends in csv_suffix, clean key and expand val to a list
            if d_type == 'd' and isinstance(v1, str) and k1.endswith(csv_suffix):
                key = k1.replace(csv_suffix, '')
                jd2[key] = v1.split(',')
                # we have entirely processed this item, so skip remaining code for it
                continue
                
            # if item val is a dict
            if isinstance(v1, dict):
                d2 = dict()
                # iterate over all dict items
                for k2,v2 in v1.items():
                    # if val is str & key ends in csv_suffix, clean key and expand val to a list
                    if isinstance(v2, str) and k2.endswith(csv_suffix):
                        key = k2.replace(csv_suffix, '')
                        d2[key] = v2.split(',')
                    # else process the key-val normally
                    else:
                        # if val is a list or dict, recurse into this function again
                        if isinstance(v2, list) or isinstance(v2, dict):
                            d2[k2] = json_csv_key_to_list(v2, csv_suffix)
                        # else val is scaler
                        else:
                            d2[k2] = v2
                res = d2
            # else store the item
            else:
                res = v1
                
            # store the processed result for this item k1,v1 in the collection (list or dict)
            if isinstance(data, list):
                jd2.append(res)
            elif isinstance(data, dict):
                jd2[k1] = res
                
    except Exception as e:
        print(f"ERROR - in function json_csv_key_to_list. Exception: {e}")
        exit()
        
    return jd2


#### Example Run - when this file is run directly
if __name__ == "__main__":
    import yaml
    import pprint

    data = """
    - hostname: switch1
      domain_servers__csv: 10.1.1.1,10.1.1.2
      radius:
        servers__csv: 10.2.2.1,10.2.2.2
        shared_key: abcd1234
      acl:
      - vty_access__csv: 10.9.9.1,10.9.9.2,10.9.9.3
      - snmp_access:
        - 33.33.33.33
        - 44.44.44.44
    """

    json1 = yaml.load(data, Loader=yaml.FullLoader)
    pprint.pprint(json1, indent=2)
    print("\n")

    json2 = json_csv_key_to_list(json1, '__csv')
    pprint.pprint(json2, indent=2)
