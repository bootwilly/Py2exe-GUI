from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QLabel,
    QMessageBox,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from py2exe_gui.Core.subprocess_tool import SubProcessTool


class ScriptFileDlg(QFileDialog):
    """用于获取入口脚本文件的对话框"""

    def __init__(self, parent: QWidget = None) -> None:
        super(ScriptFileDlg, self).__init__(parent)
        self._setup()

    def _setup(self) -> None:
        """
        配置脚本路径对话框 \n
        :return: None
        """

        self.setAcceptMode(QFileDialog.AcceptOpen)
        self.setDefaultSuffix("py")
        self.setNameFilters(("Python脚本文件 (*.py *.pyw)", "All (*)"))
        self.setFileMode(QFileDialog.ExistingFiles)
        self.setLabelText(QFileDialog.FileName, "Python入口文件")
        self.setLabelText(QFileDialog.FileType, "Python文件")
        self.setLabelText(QFileDialog.Accept, "打开")
        self.setLabelText(QFileDialog.Reject, "取消")


class IconFileDlg(QFileDialog):
    """用于获取应用图标文件的对话框"""

    def __init__(self, parent: QWidget = None) -> None:
        super(IconFileDlg, self).__init__(parent)
        self._setup()

    def _setup(self) -> None:
        """
        配置应用图标对话框 \n
        :return: None
        """

        self.setAcceptMode(QFileDialog.AcceptOpen)
        self.setDefaultSuffix("ico")
        self.setNameFilters(("图标文件 (*.ico *.icns)", "All (*)"))
        self.setFileMode(QFileDialog.ExistingFile)
        self.setLabelText(QFileDialog.FileName, "图标")
        self.setLabelText(QFileDialog.FileType, "图标文件")
        self.setLabelText(QFileDialog.Accept, "打开")
        self.setLabelText(QFileDialog.Reject, "取消")


class AboutMessage(QMessageBox):
    """用于显示关于信息的对话框"""

    def __init__(self, parent: QWidget = None) -> None:
        super(AboutMessage, self).__init__(parent)
        self._about_text: str = ""
        self._setup()

    def _setup(self) -> None:
        """
        配置关于信息对话框 \n
        :return: None
        """

        self.setWindowTitle("关于Py2exe-GUI")
        self.setStandardButtons(QMessageBox.Ok)
        self.setTextFormat(Qt.MarkdownText)
        self.setText(self.about_text)

    @property
    def about_text(self) -> str:
        """
        返回本程序的关于信息文本 \n
        :return: 关于信息
        """

        self._about_text = (
            "Py2exe-GUI 是一个[开源程序](https://github.com/muziing/Py2exe-GUI)。\n\n"
            "旨在为 [PyInstaller](https://pyinstaller.org/) 提供简单易用的图形界面。\n\n"
            "作者：[muzing](https://muzing.top/about)。"
        )
        return self._about_text


class SubProcessDlg(QDialog):
    """用于显示子进程信息的对话框"""

    def __init__(self, parent: QWidget = None) -> None:
        super(SubProcessDlg, self).__init__(parent)
        self.info_label = QLabel(self)
        self.browser = QTextBrowser(self)
        self._setup()

    def _setup(self) -> None:
        """
        配置子进程信息对话框 \n
        """

        self.setWindowTitle("PyInstaller")
        self.setModal(True)

        layout = QVBoxLayout()
        layout.addWidget(self.info_label)
        layout.addWidget(self.browser)
        self.setLayout(layout)

    def handle_output(self, subprocess_output: tuple[int, str]) -> None:
        """
        处理子进程的输出 \n
        :param subprocess_output: 子进程输出
        :return: None
        """

        output_type, output_text = subprocess_output
        if output_type == SubProcessTool.STDOUT:
            self.browser.append(output_text)
        elif output_type == SubProcessTool.STDERR:
            self.browser.append(output_text)
        elif output_type == SubProcessTool.FINISHED:
            self.info_label.setText("打包完成！")
        elif output_type == SubProcessTool.STATE:
            self.info_label.setText(output_text)


if __name__ == "__main__":
    import sys

    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    # window = ScriptFileDlg()
    # window = IconFileDlg()
    # window.fileSelected.connect(lambda f: print(f))  # type: ignore
    # window = AboutMessage()
    window = SubProcessDlg()
    window.open()
    sys.exit(app.exec())
