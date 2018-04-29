import json

def save(data, path):
    """把一个dict或者list写入文件"""
    
    # indent是缩进, ensure_ascii=False用于保存中文
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        print('save', path, s, data)
        f.write(s)

def load(path):
    """从一个文件中载入数据并转化为dict或者list"""
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        print('load', s)
        return json.loads(s)

# Model是用于存储数据的基类
class Model(object):
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = '{}.txt'.format(classname)
        return path
    
    @classmethod
    def new(cls, form):
        m = cls(form)  # 初始化实例 m = Model(form)
        return m
    
    @classmethod
    def all(cls):
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms
    
    def save(self):
        models = self.all()
        print('models', models)
        models.append(self)
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)
        
    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)


# 以下两个类用于实际的数据处理
class User(Model):
    def __init__(self, form):
        self.username = form.get('username', "")
        self.password = form.get('password', "")
    
    def validate_login(self):
        return self.username == "gua" and self.password == "123"
    
    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


# 定义一个class用于保存message
class Message(Model):
    def __init__(self, form):
        self.author = form.get('author', "")
        self.message = form.get('message', "")