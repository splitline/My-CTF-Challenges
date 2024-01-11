import pymssql


def db():
    return pymssql.connect('sqlserver', 'meow', 'da7ab4s3_p455w0rd', 'CatEmojiDB', as_dict=True)
