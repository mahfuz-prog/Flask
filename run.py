from flaskapp import create_app, config_class

app = create_app()
if __name__ == '__main__':
	app.run(debug=True)