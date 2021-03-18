
#### Remove 'none' type fields (list items or dict values) from input data
def json_remove_none_data(
    data,               # json data
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
            jd2 = list()
        elif isinstance(data, dict):
            jd2 = dict()
            
        # for each item in the collection (list or dict)
        for k1,v1 in get_next_item(data):
            if v1 is None:
                continue

            if isinstance(v1, list) or isinstance(v1, dict):
                res = json_remove_none_data(v1)
            else:
                res = v1
                       
            # store the processed result for this item k1,v1 in the collection (list or dict)
            if isinstance(data, list):
                jd2.append(res)
            elif isinstance(data, dict):
                jd2[k1] = res
                
    except Exception as e:
        print(f"ERROR - in function json_remove_none_data. Exception: {e}")
        exit()
        
    return jd2


#### Example Run - when this file is run directly
if __name__ == "__main__":
    import yaml
    import pprint

    data = """
        - a
        - b
        - 
        - d: 
            d1: hello
            d2: 
            d3: world
            d4: 
             - d41
             -
             - d42
    """

    json1 = yaml.load(data, Loader=yaml.FullLoader)
    pprint.pprint(json1, indent=4)
    print("\n")

    json2 = json_remove_none_data(json1)
    pprint.pprint(json2, indent=4)
    
