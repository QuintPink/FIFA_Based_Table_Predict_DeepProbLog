class Player: 
    def __init__(self, name: str, OVR: int,) -> None:
        self.name : str = name 
        self.OVR : str = OVR
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return self.__str__()

if __name__ == "__main__":
    pass