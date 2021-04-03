# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

import firestore
from flask import current_app, flash, Flask, Markup, redirect, render_template
from flask import request, url_for
import google.cloud.logging
import storage


app = Flask(__name__)
app.config.update(
    SECRET_KEY='bananalemonadeacid',
    MAX_CONTENT_LENGTH=8 * 1024 * 1024,
    ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg', 'gif'])
)

app.debug = False
app.testing = False

# Configure logging
if not app.testing:
    logging.basicConfig(level=logging.INFO)
    client = google.cloud.logging.Client()
    # Attaches a Google Stackdriver logging handler to the root logger
    client.setup_logging()


@app.route('/')
def points():
    # TODO delete me
    start_after = request.args.get('start_after', None)
    houses = firestore.get_houses()

    houses_dict = {house['name']: house for house in houses}
    return render_template('base.html', houses=houses_dict)


@app.route('/headmaster', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        house = firestore.update(data)
        log_entry = firestore.log_entry(
            data['house'],
            data['points'],
            house['points'],
            data['reason']
        )

        return redirect('/ledger')

    return render_template('form.html')

@app.route('/ledger', methods=['GET'])
def logs():
    entries = firestore.get_entries()
    return render_template('ledger.html', entries=entries)


@app.route('/errors')
def errors():
    raise Exception('This is an intentional exception.')


@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
