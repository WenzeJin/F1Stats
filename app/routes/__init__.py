def register_routes(app):
    from .home import home_bp
    from .tr import tr_bp
    from .stint import stint_bp
    from .live import live_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(tr_bp)
    app.register_blueprint(stint_bp)
    app.register_blueprint(live_bp)