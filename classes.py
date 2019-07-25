from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Email(MIMEMultipart):
    def __init__(self,to,From,body,subject,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self['Subject'] = subject
        self['From'] =  From
        self['To'] =  to
        self.attach(MIMEText(body,'html'))

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

def Get_config(config):
    import yaml
    with open(config) as f:
        return Struct(**yaml.safe_load(f))
        
cfg=Get_config('config.yml')

if __name__ == "__main__":
    import email
    import time
    from aiosmtpwrapper import SMTP
    cfg=Get_config('config.yml')
    message=Email(to=cfg.smtp['username'],
                    From=cfg.smtp['username'],
                    body='<p><b>Privet!!<br>%s</p>' % time.ctime(),
                    subject="Тестовая тема")
    print(SMTP(cfg.smtp['host'],cfg.smtp['port'],cfg.smtp['username'],cfg.smtp['password'],True).send([message,]))
    
    
