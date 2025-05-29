
def register_routes(app):
    from .home import home_bp
    from .tr import tr_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(tr_bp)