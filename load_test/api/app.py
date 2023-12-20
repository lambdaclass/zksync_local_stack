import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route('/run', methods=['POST'])
def run_command():
    command = request.json.get('command')

    assert "zksync-era-cli" == command[:14]

    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return {"output": output}, 200
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}, 400


if __name__ == '__main__':
    app.run(debug=True)
