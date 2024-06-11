import os
import atexit
from flask import Flask
from flask import render_template
from flask import make_response
from flask_cors import CORS

from splitio import get_factory


app = Flask(__name__)
CORS(app)


# Handle flag changes
#
# !!! No SDK functionality to handle flag changes
#


# Setup and instantiate SDK
factory = get_factory(
    os.environ["SPLIT_API_KEY"], config={"impressionsMode": "optimized"}
)
factory.block_until_ready(5)
split = factory.client()


# Create data set to identity customer and targets
attributes = dict()
attributes["kind"] = "device"
attributes["name"] = "Linux"
attributes["allocated"] = True

# Listen for flag changes
#
# !!! No SDK functionality to listen for flag changes
#


# Get flag value
treatment = split.get_treatment(
    "018ef239-957b-744a-b50b-c83bde2699cc", "Test_Flag", attributes
)
print("The initial value is: " + str(treatment))


# Setup web service
@app.route("/")
def show_page():
    retval = make_response(render_template("index.html"))
    return retval


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
