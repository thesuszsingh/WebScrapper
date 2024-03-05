# SAFE-+-SIDE 
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

class WebScraperApp(QtWidgets.QWidget):
    def _init_(self):
        super()._init_()
     
        self.setWindowTitle("Web Scraper")
        self.setGeometry(100, 100, 800, 600)  # Increased height to accommodate images

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # URL Entry
        self.url_entry = QtWidgets.QLineEdit()
        layout.addWidget(self.url_entry)

        # Scrape Button
        self.scrape_button = QtWidgets.QPushButton("Scrape")
        self.scrape_button.clicked.connect(self.scrape_website)
        layout.addWidget(self.scrape_button)

        # Result Text
        self.result_text = QtWidgets.QTextEdit()
        layout.addWidget(self.result_text)

        # Result Image Label
        self.image_label = QtWidgets.QLabel()
        layout.addWidget(self.image_label)

        self.setLayout(layout)

        # Apply dark mode stylesheet with increased font size
        self.setStyleSheet("""
            QWidget {
                background-color: #000000;
                color: #00ff00;  /* Green font color */
                font-size: 14pt;  /* Increase font size to 14 points */
            }
            QLineEdit, QPushButton, QTextEdit {
                background-color: #333333;
                color: #00ff00;  /* Green font color */
                border: 1px solid #888888;
                font-size: 14pt;  /* Increase font size to 14 points */
            }
        """)

    def scrape_website(self):
        url = self.url_entry.text()
        try:
            # Make an HTTP request
            response = requests.get(url)
            response.raise_for_status()

            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title
            title = soup.title.text

            # Extract body content
            body_content = soup.body.text

            # Extract HTML code
            html_code = str(soup)

            # Extract images and display them
            image_urls = [img['src'] for img in soup.find_all('img')]
            self.display_images(image_urls)

            # Extract comments
            comments = [comment.string for comment in soup.find_all(string=lambda text: isinstance(text, str)) if isinstance(comment, str)]
            comments_text = '\n'.join(comments)

            # Display the scraped data
            self.result_text.setPlainText(f"Title: {title}\n\nBody Content:\n{body_content}\n\nHTML Code:\n{html_code}\n\nComments:\n{comments_text}")

        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error accessing the URL: {e}")

    def display_images(self, image_urls):
        for url in image_urls:
            try:
                # Fetch image
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))

                # Display image
                pixmap = QtGui.QPixmap(img)
                pixmap_resized = pixmap.scaledToWidth(300)  # Resize image
                self.image_label.setPixmap(pixmap_resized)
                self.image_label.setAlignment(QtCore.Qt.AlignCenter)
                self.image_label.setScaledContents(True)  # Enable scaling of image

                break  # Display only the first image

            except Exception as e:
                print(f"Error fetching image from URL: {url}, Error: {e}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = WebScraperApp()
    window.show()
    sys.exit(app.exec_())

if _name_ == "_main_":
    main()