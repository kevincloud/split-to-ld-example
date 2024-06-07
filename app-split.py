import os
import atexit
from flask import Flask
from flask import render_template
from flask import make_response
from flask_cors import CORS

import ldclient
from ldclient.config import Config


app = Flask(__name__)
CORS(app)


# Handle flag changes
class change_tracker:
    def __call__(self, changed):
        print(
            "Old value: "
            + str(changed.old_value)
            + ", New value: "
            + str(changed.new_value)
        )


# Setup and instantiate SDK
ldclient.set_config(Config(os.environ["LD_SDK_KEY"]))

if ldclient.get().is_initialized():
    print("SDK successfully initialized!")
else:
    print("SDK failed to initialize")


def exitapp():
    ldclient.get().close()


atexit.register(exitapp)

# Create data set to identity customer and targets
mycontext = ldclient.Context.from_dict(
    {
        "key": "018e7bd4-ab96-782e-87b0-b1e32082b481",
        "kind": "device",
        "name": "Linux",
    }
)

# Listen for flag changes
ldclient.get().flag_tracker.add_flag_value_change_listener(
    "test-flag", mycontext, change_tracker()
)


# Get flag value
flag_value = ldclient.get().variation("test-flag", mycontext, False)
print("The initial value is: " + str(flag_value))


# Setup web service
@app.route("/")
def show_page():
    retval = make_response(render_template("index.html"))
    return retval


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
