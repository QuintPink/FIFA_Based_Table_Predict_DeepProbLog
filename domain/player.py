class Player: 
    def __init__(self, name: str, OVR: int,POT: int) -> None:
        self.name : str = name 
        self.OVR : str = OVR
        self.POT : str = POT
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return self.__str__()

if __name__ == "__main__":
    pass