from src.models.Client import *


class Miner:
    def __init__(self, blockchain, client):
        self.client = client
        self.blockchain = blockchain
        self.count = 0

    def click(self):
        self.count += 1
        if self.count == self.blockchain.curr_proof:
            raise SuccessException()

    def update(self, message):
        """при достижении нужного кол-ва кликов создается новый блок, счетчик обнуляется и пруф в объекте Blockchain
        инкрементится """
        new_block = self.blockchain.new_block(self.blockchain.curr_proof, None, comment=message)

        # print("New Block")
        self.count = 0
        self.blockchain.curr_proof += 1  # Увеличение кол-ва кликов для майнинга (MAX_COUNT)
        # print(len(self.blockchain.chain))
        # TODO: Здесь нужно послать полученный блок
        self.client.send_block(new_block)
        self.client.notifi_flag = False


class SuccessException(Exception):
    def __init__(self, msg="Success"):
        super().__init__()
        self.msg = msg
