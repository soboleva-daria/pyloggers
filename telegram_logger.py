import sys
from telegram.ext import Updater, CommandHandler
class TelegramLogger(object):
    def __init__(self,
                 token = '178242696:AAEMAggoA8XSn3vXfO__2Wd1nutx6fKjQLo',
                 name="logger",
                 reader_chat_id=None,
                 print_dual_logging=True,
                 max_local_log_size=5):
        self.name = name
        self.log_queue = []
        self.reader_chat_id = None
        self.max_local_log_size = max_local_log_size

        self.bot = None
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler('reader', self.set_reader))
        self.dispatcher.add_handler(CommandHandler('flush', lambda b, u: self.flush()))
        self.launch()
    def send_to_reader(self, msg):
        self.bot.sendMessage(chat_id=self.reader_chat_id,
                             text='<{}> {}'.format(self.name, msg))
    def push(self, string, flush=True):
        self.log_queue.append(string)
        if flush or len(self.log_queue) > self.max_local_log_size:
            self.flush()
        return self
    def flush(self):
        if self.reader_chat_id is None or self.bot is None:
            return
        for msg in self.log_queue:
            self.send_to_reader(msg)
        self.log_queue = []
        
    def launch(self):
        self.updater.start_polling()
        
    def set_reader(self, bot, update):
        text = update.message.text.strip()
        if len(text.split()) > 1:
            name = ' '.join(text.split()[1:]).strip().split()[0]
            if name != self.name:
                return

        self.reader_chat_id = update.message.chat_id
        self.bot = bot
        self.send_to_reader('You are a reader now')
        pass    
    def stop(self):
        self.updater.stop()
        
    def __del__(self):
        self.stop()
