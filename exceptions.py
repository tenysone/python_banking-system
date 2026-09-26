class BankingException(Exception):
    def __init__(self, message, error_type="GENERAL"):
        self.error_type = error_type
        super().__init__(f"[{error_type}] {message}")
