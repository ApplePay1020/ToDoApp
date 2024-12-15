from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, \
    QMessageBox, QListWidget, QListWidgetItem, QCheckBox
from PyQt5.QtCore import Qt
import json
import sys
from pathlib import Path


class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Let It Done')
        self.setGeometry(150, 150, 500, 500)
        self.todoList = []

        self.widgetToDo = QListWidget()
        self.inputToDo = QLineEdit()
        self.saveToDo = QPushButton('저장')

        self.initUI()
        self.loadjson()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Gonna Do..'))
        layout.addWidget(self.inputToDo)
        layout.addWidget(self.widgetToDo)
        layout.addWidget(self.saveToDo)

        self.saveToDo.clicked.connect(self.addtodo)
        self.inputToDo.returnPressed.connect(self.addtodo)

        self.setLayout(layout)

    def save2json(self):
        todos = [{'task': task, 'checked': item.checkState() == Qt.Checked} for task, item in self.todoList]
        filepath = 'todoList.json'
        with open(filepath, 'w') as file:
            json.dump(todos, file, indent=4)

        QMessageBox.information(self, 'Let It Done', 'ToDo가 저장되었습니다')

    def addtodo(self):
        todoitem = self.inputToDo.text()
        if todoitem:
            checkbox = QCheckBox()
            checkbox.setChecked(False)

            # QLabel과 QCheckBox를 담을 수 있는 컨테이너 위젯 생성
            container = QWidget()
            container_layout = QHBoxLayout()
            container_layout.addWidget(QLabel(todoitem))
            container_layout.addStretch(1)  # 체크박스를 우측에 정렬하기 위한 스트레치 추가
            container_layout.addWidget(checkbox)
            container.setLayout(container_layout)

            item = QListWidgetItem()
            item.setSizeHint(container.sizeHint())  # 컨테이너 위젯의 크기 설정
            self.widgetToDo.addItem(item)
            self.widgetToDo.setItemWidget(item, container)

            self.todoList.append((todoitem, checkbox))

            self.save2json()
            self.inputToDo.clear()

    def loadjson(self):
        filepath = 'todoList.json'
        try:
            with open(filepath, 'r') as file:
                todos = json.load(file)
                for todo in todos:
                    task = todo['task']
                    checked = todo.get('checked', False)

                    checkbox = QCheckBox()
                    checkbox.setChecked(checked)

                    container = QWidget()
                    container_layout = QHBoxLayout()
                    container_layout.addWidget(QLabel(task))
                    container_layout.addStretch(1)
                    container_layout.addWidget(checkbox)
                    container.setLayout(container_layout)

                    item = QListWidgetItem()
                    item.setSizeHint(container.sizeHint())
                    self.widgetToDo.addItem(item)
                    self.widgetToDo.setItemWidget(item, container)

                    self.todoList.append((task, checkbox))
        except FileNotFoundError:
            pass

    def remove_checked_todos(self):
        items_to_remove = []

        for index in range(self.widgetToDo.count()):
            item = self.widgetToDo.item(index)
            widget = self.widgetToDo.itemWidget(item)
            checkbox = widget.findChild(QCheckBox)

            if checkbox.isChecked():
                items_to_remove.append((index, item))

        for index, item in reversed(items_to_remove):
            self.widgetToDo.takeItem(index)
            self.todoList.pop(index)

    def closeEvent(self, event):
        self.remove_checked_todos()
        self.save2json()
        event.accept()

    def apply_styles(self):
        # 각 항목 사이에 구분선을 넣기 위한 스타일 시트 적용
        style_sheet = """
            QListWidget::item {
                border-bottom: 1px solid rgba(0, 0, 0, 0.2);
                padding: 5px;
            }
        """
        self.widgetToDo.setStyleSheet(style_sheet)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    todoApp = ToDoApp()
    todoApp.apply_styles()
    todoApp.show()
    sys.exit(app.exec_())
