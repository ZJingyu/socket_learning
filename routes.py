from models import User, Message


def template(name, header=None):
    """模板加载"""
    path = "templates/" + name
    # 请求头
    if not header:
        header = 'HTTP/1.1 210 OK\r\nContent-Type: text/html\r\n\r\n'
    
    with open(path, encoding='utf-8', mode='r') as f:
        return header + f.read()
        

def route_index(request):
    """返回主页响应"""
    r = template('index.html')
    return r.encode(encoding='utf-8')

def route_login(request):
    if request.method == 'POST':
        # request.form会把body里的参数转换成字典
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            result = "登陆成功！"
        else:
            result = "用户名或者密码错误!"
    else:
        result = ""
    body = template('login.html')
    body = body.replace('{{result}}', result)
    return body.encode(encoding='utf-8')

def route_register(request):
    if request.method == "POST":
        form = request.form()
        u = User.new(form)
        # 验证
        if u.validate_register():
            u.save()
            result = "注册成功<br> <pre>{}</pre>".format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    return body.encode('utf-8')


# 存储form表单里的数据
message_list = []
def route_message(request):
    if request.method == "POST":
        form = request.form()
        msg = Message.new(form)
        message_list.append(msg)
    body = template('html_basic.html')
    msgs = '<br>'.join([str(m) for m in message_list])
    print(msgs)
    body = body.replace("{{messages}}", msgs)
    return body.encode(encoding='utf-8')

def route_static(request):
    """
    静态资源的架加载
    """
    filename = request.query.get('file', 'dog.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
        img = header + f.read()
        return img


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message, 
}