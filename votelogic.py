import csv
import time

from PyQt6.QtWidgets import *
from voteui import *


class Votelogic(QMainWindow, Ui_MainWindow):
    account_id = 0

    def __init__(self, id, login_window):
        super().__init__()
        self.setupUi(self)
        self.account_id = id
        self.login_window = login_window

        self.SubmitButton.clicked.connect(lambda: self.submit())
        self.load_data()

    def load_data(self):
        try:
            with open("votedata.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and int(row[0]) == self.account_id:
                        self.FirstNameField.setText(row[1])
                        self.LastNameField.setText(row[2])
                        self.DobDate.setDate(
                            QtCore.QDate.fromString(row[3], "MM/dd/yyyy")
                        )  # I looked this one up since we didnt cover the date field in any of the assignments.
                        if row[4] == "John":
                            self.CanidateOneButton.setChecked(True)
                        elif row[4] == "Jane":
                            self.CanidateTwoButton.setChecked(True)
        except FileNotFoundError:
            pass

    def submit(self):
        first = self.FirstNameField.text().strip()
        last = self.LastNameField.text().strip()
        dob = self.DobDate.text().strip()
        id = self.account_id

        vote = self.buttonGroup.checkedButton()
        if not vote:
            self.ErrorLabel.setText(
                "Please select the canidate you would like to vote for"
            )
            return
        else:
            vote_text = vote.text()

        rows = []
        account_found = False

        try:
            with open("votedata.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and int(row[0]) == id:
                        rows.append([id, first, last, dob, vote_text])
                        account_found = True
                    else:
                        rows.append(row)
        except FileNotFoundError:
            pass

        if not account_found:
            rows.append([id, first, last, dob, vote_text])

        with open("votedata.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        self.ErrorLabel.setText("Submitting Vote...")
        QApplication.processEvents()
        time.sleep(2)
        self.login_window.show()  # For this I did use AI to help me figure out how to utilize two windows without producing the "QCoreApplication::exec: The event loop is already running" error.
        self.FirstNameField.clear()
        self.LastNameField.clear()
        self.DobDate.clear()
        self.account_id = 0
        checked = self.buttonGroup.checkedButton()  # The reset that we used previous was throwing an error for me so I found this solution.
        self.ErrorLabel.setText("Enter your details and cast your vote")
        if checked is not None:
            self.buttonGroup.setExclusive(False)
            checked.setChecked(False)
            self.buttonGroup.setExclusive(True)
        self.close()
