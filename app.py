from flask import Flask, render_template, request, redirect, session
from database import init_db, get_db
from auth import AuthService
from car_service import CarService
from booking_service import BookingService
from message_service import MessageService
from payment_service import PaymentService
from patterns.chain import Q1Handler, Q2Handler, Q3Handler
from notification_service import NotificationService
from message_service import MessageService

msg_service = MessageService()

notifications = NotificationService()

messages = MessageService()
payment = PaymentService()

app = Flask(__name__)
app.secret_key = "driveshare-secret"

init_db()

auth = AuthService()
cars = CarService()
bookings = BookingService()


# HOME
@app.route("/")
def home():
    return render_template("index.html")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        ok, msg = auth.register(
            request.form["email"],
            request.form["password"],
            request.form["q1"],
            request.form["q2"],
            request.form["q3"]
        )
        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        ok, user = auth.login(
            request.form["email"],
            request.form["password"]
        )

        if ok:
            session["user_id"] = user["id"]
            return redirect("/dashboard")

    return render_template("login.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


# CARS LIST

@app.route("/cars", methods=["GET"])
def cars_page():

    if "user_id" not in session:
        return redirect("/login")

    location = request.args.get("location")

    if location:
        data = cars.search_by_location(location)
    else:
        data = cars.get_all_cars()

    return render_template("cars.html", cars=data)


# ADD CAR
@app.route("/add_car", methods=["GET", "POST"])
def add_car():
    if request.method == "POST":
        cars.add_car(
            session["user_id"],
            request.form["model"],
            request.form["year"],
            request.form["mileage"],
            request.form["location"],
            request.form["price"],
            request.form["available"]
        )
        return redirect("/my_cars")

    return render_template("add_car.html")

@app.route("/my_cars")
def my_cars():
    data = cars.get_my_cars(session["user_id"])
    return render_template("my_cars.html", cars=data)

@app.route("/edit_car/<int:car_id>", methods=["GET", "POST"])
def edit_car(car_id):
    if request.method == "POST":
        cars.update_car(
            car_id,
            request.form["price"],
            request.form["available"]
        )
        return redirect("/my_cars")

    return render_template("edit_car.html", car_id=car_id)


# BOOK CAR
@app.route("/book/<int:car_id>", methods=["GET", "POST"])
def book(car_id):

    if "user_id" not in session:
        return redirect("/login")

    car = cars.get_car_by_id(car_id)

    if request.method == "POST":
        ok, msg = bookings.book_car(
            car_id,
            session["user_id"],
            request.form["start_date"],
            request.form["end_date"]
        )

        return render_template(
            "book.html",
            message=msg,
            car=car
        )

    return render_template(
        "book.html",
        car=car
    )


@app.route("/message/<int:car_id>", methods=["GET", "POST"])
def message(car_id):

    car = cars.get_car_by_id(car_id)

    if request.method == "POST":
        text = request.form["text"]

        msg_service.send(
            session["user_id"],
            car["owner_id"],
            text
        )

        return render_template("message.html", success="Message sent!")

    return render_template("message.html", car=car)




@app.route("/pay/<int:car_id>")
def pay(car_id):


    if "user_id" not in session:
        return redirect("/login")

    car = cars.get_car_by_id(car_id)

    result = payment.pay(car["price"])

    notifications.send(
        car["owner_id"],
        f"Payment received for {car['model']} (${car['price']})"
    )

    notifications.send(
        session["user_id"],
        f"You paid ${car['price']} for {car['model']}"
    )

    return render_template(
        "book.html",
        message=f"Payment successful: ${car['price']} paid",
        car=car
    )


@app.route("/recover", methods=["GET", "POST"])
def recover():
    result = None
    allow_reset = False
    email = None

    if request.method == "POST":

        db = get_db()

        # STEP 1: CHECK EMAIL + SECURITY ANSWERS
        if "new_password" not in request.form:
            email = request.form["email"]

            user = db.execute(
                "SELECT * FROM users WHERE email=?",
                (email,)
            ).fetchone()

            if not user:
                result = "User not found"
            else:
                chain = Q1Handler(Q2Handler(Q3Handler()))

                data = {
                    "input_q1": request.form["q1"],
                    "input_q2": request.form["q2"],
                    "input_q3": request.form["q3"],
                    "db_q1": user["q1"],
                    "db_q2": user["q2"],
                    "db_q3": user["q3"]
                }

                ok = chain.handle(data)

                if ok:
                    allow_reset = True
                    email = user["email"]
                else:
                    result = "Security answers incorrect"

        # STEP 2: RESET PASSWORD
        else:
            email = request.form["email"]

            db.execute(
                "UPDATE users SET password=? WHERE email=?",
                (request.form["new_password"], email)
            )
            db.commit()

            result = "Password updated successfully"

    return render_template(
        "recover.html",
        result=result,
        allow_reset=allow_reset,
        email=email
    )

@app.route("/notifications")
def show_notifications():

    user_id = session["user_id"]

    data = notifications.get(user_id)

    return render_template("notifications.html", notifications=data)

@app.route("/reply/<int:to_user_id>", methods=["POST"])
def reply(to_user_id):

    if "user_id" not in session:
        return redirect("/login")

    text = request.form["text"]

    msg_service.send(
        session["user_id"],
        to_user_id,
        text
    )

    return redirect("/notifications")

@app.route("/watch/<int:car_id>", methods=["POST"])
def watch(car_id):

    db = get_db()
    user_id = session["user_id"]
    max_price = request.form["max_price"]

    db.execute("""
        INSERT INTO watches (car_id, user_id, max_price)
        VALUES (?, ?, ?)
    """, (car_id, user_id, max_price))

    db.commit()

    return redirect("/cars")

if __name__ == "__main__":
    app.run(debug=True)

