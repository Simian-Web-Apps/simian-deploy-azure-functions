from simian.gui import Form, component, component_properties, utils

examples_url = "#"


# Run this file locally
if __name__ == "__main__":
    import simian.local

    simian.local.Uiformio("hello_world", window_title="Simian: Hello World!")


def gui_init(meta_data: dict) -> dict:
    """Create a form and set a logo and title."""

    # Create form.
    form = Form()

    # Base payload
    payload = {
        "form": form,
        "navbar": {
            "title": (
                f'<a class="text-white" href="{examples_url}" target="_blank">'
                '<i class="fa fa-github"></i></a>&nbsp;Hello World - from Simian!'
            )
        },
    }

    html_hello = component.HtmlElement("html_hello", form)
    html_hello.content = "Hello World"

    return payload


def gui_event(meta_data: dict, payload: dict) -> dict:
    return payload
