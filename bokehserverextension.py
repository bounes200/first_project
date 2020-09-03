from subprocess import Popen


def load_jupyter_server_extension(nbapp):
    """serve the SNI_app directory with bokeh server"""
    Popen(["bokeh", "serve", "SNI_app", "--allow-websocket-origin=*"])
