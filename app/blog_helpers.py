from markdown import markdown
import os
def render_markdown(file_name, dir_path = 'app/views'):
    """Takes the specified file path and
    returns it as HTML
    """
    html = ""

    #os.path.join creates an OS-valid path
    path = os.path.join(dir_path, file_name)
    with open(path) as html_file:
        html = html_file.read()

        if file_name.endswith("md"):
            html = markdown(html)
    return html