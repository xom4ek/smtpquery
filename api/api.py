from client import EmailRpcClient
import yaml
import tarfile
import io
import shutil
from flask import Flask, request, jsonify, send_file


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)
def Get_config(config):
    import yaml
    with open(config) as f:
        return Struct(**yaml.safe_load(f))

cfg=Get_config('config.yml')

email_rpc = EmailRpcClient(**cfg.rabbit)


@app.route('/sendMail')
def sendMail():
    try:
        response = jsonify(email_rpc.sendEmail(**request.args.to_dict()))
        return response
    except TypeError:
        return 'Wrong parameters'


@app.route('/sendTemplate')
def sendTemplate():
    try:
        response = jsonify(email_rpc.sendTemplate(**request.args.to_dict()))
        return response
    except TypeError:
        return 'Wrong parameters'

# @app.route('/getDetailedInfo')
# def getDetailedInfo():
#     try:
#         response = jsonify(HPSM.getDetailedInfo(**request.args.to_dict()))
#         return response
#     except TypeError:
#         return 'Wrong parameters'


# @app.route('/takeCustomFieldValues')
# def takeCustomFieldValues():
#     try:
#         response = jsonify(HPSM.takeCustomFieldValues(
#             **request.args.to_dict()))
#         return response
#     except TypeError:
#         return 'Wrong parameters'


# @app.route('/takeTopicContent')
# def takeTopicContent():
#     try:
#         response = jsonify(HPSM.takeTopicContent(
#             **request.args.to_dict()))
#         return response
#     except TypeError:
#         return 'Wrong parameters'


# @app.route('/downloadFiles')
# def downloadFiles():
#     try:
#         files = HPSM.downloadFiles(**request.args.to_dict())
#     except TypeError:
#         return 'Wrong parameters'
#     tar_file = io.BytesIO()
#     with tarfile.open(fileobj=tar_file, mode='w:gz') as tar:
#         for name in files:
#             file_info = tarfile.TarInfo(name=name)
#             file_info.size = files[name].getbuffer().nbytes
#             files[name].seek(0)
#             tar.addfile(tarinfo=file_info, fileobj=files[name])
#     tar_file.seek(0)
#     return send_file(
#         tar_file,
#         as_attachment=True,
#         attachment_filename=request.args.get('topic')+'.tar.gz',
#         mimetype='application/tar'
#     )


if __name__ == '__main__':
    app.run()
