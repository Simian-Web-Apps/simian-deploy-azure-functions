from simian.gui import Form, component, component_properties, utils

examples_url = "https://github.com/Simian-Web-Apps/deploy-azure-functions"
hello_world_step = 1

# Run this file locally
if __name__ == "__main__":
    import simian.local

    simian.local.Uiformio(
        f"hello_world_step_{hello_world_step}",
        window_title=f"Simian: Hello World - Step {hello_world_step} !",
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
                f'<a class="text-white" href="{examples_url}" target="_blank">'
                f'<i class="fa fa-github"></i></a>&nbsp;Hello World Step {hello_world_step} - from Simian!'
            )
        },
    }

    html_hello = component.HtmlElement("html_hello", form)
    html_hello.content = f"Hello World - Step {hello_world_step}"

    return payload


def gui_event(meta_data: dict, payload: dict) -> dict:
    return payload
