from cs50 import SQL

db = SQL("sqlite:///management.db")
key = "PVTLTD786"

def qr_id_generation(passcode):
    if passcode != key:
        return 0
    row = db.execute("SELECT QR_ID FROM constants WHERE key = ?;", key)
    count = row[0]["QR_ID"].replace("QR", "")
    count = int(count) + 1
    new = "QR" + str(count)
    db.execute("UPDATE constants SET QR_ID = ? WHERE key = ?;", new, key)
    return new

def job_card_generation(passcode):
    if passcode != key:
        return 0
    row = db.execute("SELECT Job_Card FROM constants WHERE key = ?;", key)
    count = row[0]["Job_Card"].replace("JC", "")
    count = int(count) + 1
    new = "JC" + str(count)
    db.execute("UPDATE constants SET Job_Card = ? WHERE key = ?;", new, key)
    return new

def order_id_generation(passcode):
    if passcode != key:
        return 0
    row = db.execute("SELECT Order_ID FROM constants WHERE key = ?;", key)
    count = row[0]["Order_ID"].replace("OD", "")
    count = int(count) + 1
    new = "OD" + str(count)
    db.execute("UPDATE constants SET Order_ID = ? WHERE key = ?;", new, key)
    return new

def customer_id_generation(passcode):
    if passcode != key:
        return 0
    row = db.execute("SELECT Customer_ID FROM constants WHERE key = ?;", key)
    count = row[0]["Customer_ID"].replace("C", "")
    count = int(count) + 1
    new = "C" + str(count)
    db.execute("UPDATE constants SET Customer_ID = ? WHERE key = ?;", new, key)
    return new

