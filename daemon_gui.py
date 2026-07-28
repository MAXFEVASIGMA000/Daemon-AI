import sys
import os
import psutil

import agent

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel,
    QListWidget,
    QFrame
)

from PySide6.QtGui import QPixmap


class DaemonGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Daemon IDE")
        self.resize(1100, 700)

        self.setStyleSheet("""
            QWidget {
                background-color: #0d1117;
                color: white;
                font-family: JetBrains Mono;
            }

            QTextEdit {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 10px;
            }

            QLineEdit {
                background-color: #161b22;
                border: 1px solid #58a6ff;
                border-radius: 8px;
                padding: 10px;
                color: white;
            }

            QPushButton {
                background-color: #238636;
                border-radius: 8px;
                padding: 10px;
            }

            QPushButton:hover {
                background-color: #2ea043;
            }

            QListWidget {
                background-color: #010409;
                border: none;
            }
        """)


        main = QHBoxLayout()


        # SIDEBAR

        sidebar = QFrame()
        sidebar.setFixedWidth(260)

        side_layout = QVBoxLayout()


        logo = QLabel()

        image = QPixmap("daemon-logo.png")

        if not image.isNull():
            logo.setPixmap(
                image.scaled(120, 120)
            )

        side_layout.addWidget(logo)


        title = QLabel(
            "◉ DAEMON IDE"
        )

        title.setStyleSheet(
            "color:#39ff88;font-size:22px;font-weight:bold;"
        )

        side_layout.addWidget(title)


        self.stats = QLabel()

        self.stats.setStyleSheet(
            "color:#58a6ff;"
        )

        side_layout.addWidget(self.stats)


        side_layout.addWidget(
            QLabel("WORKSPACE")
        )


        self.files = QListWidget()

        self.refresh_files()

        side_layout.addWidget(self.files)


        sidebar.setLayout(side_layout)



        # CHAT

        chat_layout = QVBoxLayout()


        self.chat = QTextEdit()

        self.chat.setReadOnly(True)


        self.chat.append(
            """
            <h2 style='color:#39ff88'>
            ◉ DAEMON ONLINE
            </h2>

            <p>
            Coding agent ready.
            </p>
            """
        )


        chat_layout.addWidget(self.chat)


        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "Ask Daemon to code, edit, or use tools..."
        )


        self.input.returnPressed.connect(
            self.send
        )


        chat_layout.addWidget(self.input)


        button = QPushButton(
            "Send"
        )

        button.clicked.connect(
            self.send
        )

        chat_layout.addWidget(button)



        main.addWidget(sidebar)
        main.addLayout(chat_layout)

        self.setLayout(main)


        self.update_stats()



    def refresh_files(self):

        self.files.clear()

        workspace = os.path.expanduser(
            "~/daemon-ai/workspace"
        )

        if os.path.exists(workspace):

            for root, dirs, files in os.walk(workspace):

                for file in files:

                    path = os.path.join(
                        root,
                        file
                    )

                    self.files.addItem(
                        path.replace(
                            workspace,
                            ""
                        )
                    )



    def update_stats(self):

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        self.stats.setText(
            f"""
ONLINE

CPU: {cpu}%
RAM: {ram}%

MODEL:
llama3.1
"""
        )



    def send(self):

        message = self.input.text()

        if not message:
            return


        self.chat.append(
            f"""
            <p style='color:#58a6ff'>
            <b>You:</b> {message}
            </p>
            """
        )


        self.input.clear()


        self.chat.append(
            """
            <p style='color:#aaaaaa'>
            Daemon is working...
            </p>
            """
        )


        QApplication.processEvents()


        try:

            answer = agent.ask_daemon(
                message
            )


        except Exception as e:

            answer = (
                "Daemon error:\n"
                + str(e)
            )


        self.chat.append(
            f"""
            <p style='color:#39ff88'>
            <b>Daemon:</b><br>
            {answer}
            </p>
            """
        )


        self.refresh_files()
        self.update_stats()



app = QApplication(sys.argv)

window = DaemonGUI()

window.show()

sys.exit(app.exec())
