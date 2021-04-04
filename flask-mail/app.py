from flask import render_template


def create_app():
    from . import event_email, config, init_database

    app = config.app

    @app.route('/')
    def home():
        """
        home page of this app, respond for localhost:5000/
        :return: the rendered template 'home.html'
        """
        return render_template('home.html')

    config.api.add_resource(event_email.EventEmailListResource, f'{config.api_dir}/event_emails')
    config.api.add_resource(event_email.EventEmailCreateResource, f'{config.api_dir}/save_emails')
    config.api.add_resource(event_email.EventEmailResource, f'{config.api_dir}/event_emails/<int:id>')

    # add command
    app.cli.add_command(init_database.init_db_command)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
