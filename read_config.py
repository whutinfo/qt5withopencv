import json

def read():
    with open('data.json') as f:
        data = json.load(f)
    print('配置中有'+str(len(data))+'个摄像头')
    return(data)
