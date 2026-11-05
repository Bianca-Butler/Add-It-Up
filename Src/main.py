from flask import Flask, render_template, request, redirect, url_for
import csv
import json

app = Flask(__name__)
expenses = []
budgetHistory = []
budget = 0.0


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
        saveExpenses()

        return redirect(url_for("home"))
    return render_template("index.html", expenses = expenses, total = calculateTotal(), budget=budget, remaining = calculateRemaining(), budgetHistory=budgetHistory)

def calculateTotal():
    total = 0
    for expense in expenses:
        total += expense["amount"]

    return total

@app.route("/budget", methods = ["POST"])
def setBudget():
    global budget

    budgetAmount = float(request.form.get("budget"))

    if budget > 0:
        previousBudget = {
        "budget": budget,
        "expenses": expenses.copy()}

        budgetHistory.append(previousBudget)
        saveBudgetHistory()

    budget = budgetAmount

    expenses.clear()
    saveExpenses()

    saveBudget()

    return redirect(url_for("home"))

def calculateRemaining():
    remainingBudget = budget - calculateTotal()

    return remainingBudget

def saveExpenses():
    with open("Data/expenses.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "amount", "category"])

        for expense in expenses:
            writer.writerow([expense["name"], expense["amount"], expense["category"]])

def loadExpenses():
    with open("Data/expenses.csv", "r", newline = "") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["amount"] = float(row["amount"])
            expenses.append(row)

def saveBudget():
    with open("Data/budget.txt", "w") as file:
        file.write(str(budget))

def loadBudget():
    global budget

    with open("Data/budget.txt", "r") as file:
        budget = float(file.read())

def saveBudgetHistory():
    with open("data/budget_history.json", "w") as file:
        json.dump(budgetHistory, file, indent=4)

def loadBudgetHistory():
    global budgetHistory

    try:
        with open("data/budget_history.json", "r") as file:
            budgetHistory = json.load(file)
    except FileNotFoundError:
        budgetHistory = []

if __name__ == "__main__":
    loadExpenses()
    loadBudget()
    loadBudgetHistory()
    app.run(debug=True)