class Package:
    def __init__(self, payload: bytes):
        self._payload = self._parse(payload)

    @staticmethod
    def _parse(payload: bytes) -> dict:
        int_payload = [x for x in payload]
        n = 3
        split_payload = [int_payload[i * n:(i + 1) * n] for i in range((len(int_payload) + n - 1) // n )]
        output = {}
        for data in split_payload:
            output[data[0]] = (data[1] << 8) | data[2]
        return output

    def dict(self) -> dict:
        return self._payload 