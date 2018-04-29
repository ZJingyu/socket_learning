"""
url规范
第一个?之前是path，参数是?之后的键值对
"""
import urllib.parse, socket

from routes import route_static, route_dict

# 定义一个class用于保存请求的数据
class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''

    
    def form(self):
        """form用于把body解析为一个字典并返回"""
        # username=a+u%26a%3F&password=
        # username=g u&a?&password=
        # body = urllib.parse.unquote(self.body)  # 为了处理参数中带有特殊字符的这种情况
        args = self.body.split("&")
        f = {}
        for arg in args:
            arg = urllib.parse.unquote(arg)  # 应该在这里进行转码
            k, v = arg.split("=")
            f[k] = v
        return f
    
    
request = Request()


def parsed_path(path):
    """
    解析路径和参数
    msg=hello&author=alex
    {
        'msg': 'hello',
        'author': 'alex',
    }
    """
    index = path.find("?")
    # 如果没有找到?说明没有传递参数，那就 返回路径本身和空的字符串
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split("?", 1)
        args = query_string.split("&")
        query = {}
        for arg in args:
            k, v = arg.split("=")
            query[k] = v
        return path, query

def error(request, code=404):
    pass

def response_for_path(path):
    path, query = parsed_path(path)   # 路径解析
    request.path = path 
    request.query = query
    print('path and query', path, query)
    """
    根据path调用相应的处理函数，没有处理的path会返回404
    """
    # 加载静态资源
    r = {
        '/static': route_static,
    }
    # 加载路由映射
    r.update(route_dict)
    # 传递request给url对应的函数
    response = r.get(path, error)
    return response(request)
    


def run(host='', port=3000):
    
    with socket.socket() as s:
        s.bind((host, port))
        
        while True:
            s.listen(5)
            connection, address = s.accept()
            r = connection.recv(1024)
            # print("原始信息: ", r)
            r = r.decode(encoding='utf-8')
            # print(r)
            # GET /msg?a=123&b=456 HTTP/1.1 200 OK
            # POST /msg HTTP/1.1 200 OK ... a=123&b=456
            # 获取请求的参数和请求的路由, 丢掉剩余的header
            request.method, path = r.split()[:2]
            # 把body放到request中
            request.body = r.split("\r\n\r\n", 1)[1]
            # 用response函数来得到path对应的响应
            response = response_for_path(path)
            # 把响应发送给客户端
            connection.sendall(response)
            
            connection.close()
            


if __name__ == '__main__':
    config_dict = dict(
        host='',
        port=3000,
    )
    run(**config_dict)
