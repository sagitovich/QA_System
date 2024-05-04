#                               start                                #
- curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
- python get-pip.py (python3 get-pip.py)

- pip install virtualenv 

- git clone https://github.com/sagitovich/QA_System.git

- virtualenv venv
- source venv/bin/activate

#                       libraries for bot.py                         #

- pip install pyTelegramBotAPI telebot python-dotenv 

#                   libraries for ai_system.py                       #

- pip install GroQ 

#                  libraries for pdf_to_text.py                      #

- pip install pypdf2 pdfminer pdfplumber pillow pdf2image pytesseract

#                             run Bot                                #

- python3 bot.py
