import os
import sys

from flask import Flask, render_template
from flask_caching import Cache

cache = Cache(config={"CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": 300})

def init_extensions(app: Flask):
    # use .init_app() on your extensions to register them on
    # the Flask instance
    cache.init_app(app)
    pass


def get_root_dir_abs_path() -> str:
    """
    Get the absolute path to the root directory of the application.
    """
    # Check if the application runs in a bundled executable from PyInstaller.
    # When executed, the bundled executable get's unpacked into the temporary directory sys._MEIPASS.
    # See also: https://pyinstaller.readthedocs.io/en/stable/runtime-information.html#using-file
    return getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))


def create_app(config_object_name) -> Flask:
    """
    :param config_object_name: The python path of the config object.
                               E.g. appname.settings.ProdConfig
    """

    root_dir_abs_path = get_root_dir_abs_path()

    # Initialize the core application
    app = Flask(
        __name__,
        instance_relative_config=False,
        static_folder=os.path.join(root_dir_abs_path, "static"),
        template_folder=os.path.join(root_dir_abs_path, "templates"),
    )
    app.config.from_object(config_object_name)

    # Initialize Plugins at startup using init_app()
    init_extensions(app)

    with app.app_context():
        # Register Blueprints
        from app.views import home, blog, youtube, people, faq, contact
        from app.views.services import dashboard, digital_forensics
        app.register_blueprint(home.bp)
        app.register_blueprint(dashboard.bp)
        app.register_blueprint(digital_forensics.bp)
        app.register_blueprint(blog.bp)
        app.register_blueprint(youtube.bp)
        app.register_blueprint(people.bp)
        app.register_blueprint(faq.bp)
        app.register_blueprint(contact.bp)

        @app.errorhandler(404)
        def page_not_found(error):
            return render_template("page/errors/404.html", title="Page Not Found"), 404

        return app
