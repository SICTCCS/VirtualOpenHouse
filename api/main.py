from app import app, scheduler, get_all_data

scheduler.start()
get_all_data()
app.run(host="0.0.0.0", port=5000, debug=True)