from typing import Protocol, List
import requests


class SequenceDatabase(Protocol):
    def lookup(self, entry: str) -> str:
        """Given protein entry, returns FASTA format"""

    def lookup_many(self, entry_list: List[str]) -> str:
        """Given protein entry array, returns FASTA format"""


class DBFetch(SequenceDatabase):
    """
    API used: https://www.ebi.ac.uk/Tools/dbfetch/
    """

    is_individually_retrieved: bool

    def __init__(self, is_individually_retrieved: bool):
        """
        is_individually_retrieved: The order of uniprot_entries_list is not guaranteed to match the fasta_format returned. Because of this, individually retrieved
        Further explanation: https://www.ebi.ac.uk/Tools/dbfetch/faq.jsp#Q2
        """
        self.is_individually_retrieved = is_individually_retrieved

    def lookup(self, entry: str) -> str:
        """
        entry: Uniprot entry
        """
        response = requests.get(
            f"https://www.ebi.ac.uk/Tools/dbfetch/dbfetch?db=uniprotkb&id={entry}&format=fasta&style=raw&Retrieve=Retrieve"
        )
        return response.text

    def lookup_many(self, entry_list: List[str]):
        """
        entry: Uniprot entries
        """
        if not self.is_individually_retrieved:
            entry_list = ",".join(entry_list)
            response = requests.get(
                f"https://www.ebi.ac.uk/Tools/dbfetch/dbfetch?db=uniprotkb&id={entry_list}&format=fasta&style=raw&Retrieve=Retrieve"
            )
            return response.text
        fasta_format = ""
        count = 0
        # TODO: Make the request async for individual retrieved to speed it up
        for entry in entry_list:
            response = requests.get(
                f"https://www.ebi.ac.uk/Tools/dbfetch/dbfetch?db=uniprotkb&id={entry}&format=fasta&style=raw&Retrieve=Retrieve"
            )
            fasta_format += response.text
            count += 1
            print(f"Fetching {entry}'s sequence {count}")
        return fasta_format
