format:
	black src/
run: 
	cd src && \
	gunicorn --bind :1234 --workers 1 --threads 8 --timeout 0 app:app
