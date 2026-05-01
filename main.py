from PyQt6.QtWidgets import QApplication
from voteloginlogic import *


def main() -> None:
    application = QApplication([])
    window = Voteloginlogic()
    window.show()
    application.exec()


if __name__ == "__main__":
    main()
