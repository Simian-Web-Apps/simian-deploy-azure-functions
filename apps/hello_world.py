from simian.gui import Form, component, utils

github_url = "https://github.com/Simian-Web-Apps/simian-deploy-render"

# Run this file locally
if __name__ == "__main__":
    import simian.local

    simian.local.Uiformio(
        "hello_world",
        window_title="Simian: Hello World!",
    )


def gui_init(meta_data: dict) -> dict:
    """Create a form and set a logo and title."""

    # Create form.
    form = Form()

    # Base payload
    payload = {
        "form": form,
        "navbar": {
            "title": (
                f'<a class="text-white" href="{github_url}" target="_blank"><i class="fa fa-github"></i></a> Hello World - from Simian!'
            )
        },
    }

    # Create a textfield.
    hello_text = component.TextField("helloKey", form)
    hello_text.label = "Enter greeting to world"
    hello_text.defaultValue = "Hello"

    # Create a button.
    world_button = component.Button("buttonKey", form)
    world_button.label = "Greet World!"
    world_button.setEvent("WorldButtonPushed")

    # Create a textfield.
    result_text = component.TextField("resultKey", form)
    result_text.label = "The result"
    result_text.placeholder = "Click button to display result ..."
    result_text.disabled = True

    return payload


def gui_event(meta_data: dict, payload: dict) -> dict:
    # Process the events.
    Form.eventHandler(WorldButtonPushed=say_hello)
    callback = utils.getEventFunction(meta_data, payload)

    return callback(meta_data, payload)


def say_hello(meta_data: dict, payload: dict) -> dict:
    # Print the "<helloKey> world!" string to the console.
    result_text = utils.getSubmissionData(payload, "helloKey")[0] + " world!"
    utils.setSubmissionData(payload, "resultKey", result_text)

    return payload
