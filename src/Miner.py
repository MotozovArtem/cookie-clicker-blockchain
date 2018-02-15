

class Miner:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.count = 0

    def click(self):
        self.count += 1
        if self.count == self.blockchain.curr_proof:
            self.update()

    def update(self):
        """при достижении нужного кол-ва кликов создается новый блок, счетчик обнуляется и пруф в объекте Blockchain
        инкрементится """
        self.blockchain.new_block(self.blockchain.curr_proof, comment=self.open_comment_window())
        self.count = 0
        self.blockchain.curr_proof += 1

    def open_comment_window(self):
        """Сначала всех оповещаем о созданном блоке, затем все остальное"""
        # send_a_message_that_i've_created_a_block()
        # everything_else()
        pass
