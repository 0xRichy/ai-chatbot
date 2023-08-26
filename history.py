@app.route("/history")
def get_history():
    user_id = request.args.get("user_id")
    c.execute("SELECT conversation FROM history WHERE user_id = ?", (user_id,))
    history = c.fetchall()
    return json.dumps(history)
