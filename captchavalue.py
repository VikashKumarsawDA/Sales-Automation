import random

def generatecaptcha():
    captcha = ''
    a=str(random.randint(1,9))
    b=chr(random.randint(65,90))
    c=str(random.randint(1,9))
    d=chr(random.randint(97,121))
    e=str(random.randint(1,9))
    captcha =' '+a+' '+b+' '+c+' '+d+' '+e+' '
    return captcha


def generatepass():
    password = ''
    a=str(random.randint(1,9))
    b=str(random.randint(1,9))
    c=str(random.randint(1,9))
    d=str(random.randint(1,9))
    e=str(random.randint(10,99))
    password = (a+b+c+d+e)
    password =int(password)
    return password