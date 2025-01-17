from dataclasses import dataclass


@dataclass(frozen=True)
class Person:
    """Dataclass to represent a person."""

    person_id: int
    name: str

    def __eq__(self, __value: object) -> bool:
        """Compare two Person objects."""
        return isinstance(__value, Person) and self.person_id == __value.person_id and self.name == __value.name


@dataclass(frozen=True)
class Transaction:
    """Type definition for a transaction."""

    debtor: Person
    creditor: Person
    amount: float
