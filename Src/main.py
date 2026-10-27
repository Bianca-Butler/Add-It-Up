from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
expenses = []

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        amount = float(request.form.get("amount"))
        category = request.form.get("category")

        expense = {
                   "name": name , 
                   "amount": amount, 
                   "category": category
                   }
        expenses.append(expense)
        return redirect(url_for("home"))
    return render_template("index.html", expenses = expenses, total = calculateTotal())

def calculateTotal():
    total = 0
    for expense in expenses:
        total += expense["amount"]

    return total

if __name__ == "__main__":
    app.run(debug=True)