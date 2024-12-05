from typing import Protocol, List
import requests


class SequenceDatabase(Protocol):
    def lookup(self, entry: str) -> str:
        """Given protein entry, returns FASTA format"""

    def lookup_many(self, entry_list: List[str]) -> List[str]:
        """Given protein entry array, returns FASTA format"""


class DBFetch(SequenceDatabase):
    """
    API used: https://www.ebi.ac.uk/Tools/dbfetch/
    """

    is_individually_retrieved: bool

    def __init__(self, is_individually_retrieved: bool):
        """
        is_individually_retrieved: The order of uniprot_entries_list is not guaranteed to match the fasta_format returned. Because of this, individually retrieved one by one to keep the same order
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
        sequence_list = []
        count = 0
        # TODO: Make the request async for individual retrieved to speed it up
        for entry in entry_list:
            print(f"PROGRESS: Fetching {entry}'s sequence {count}")
            response = requests.get(
                f"https://www.ebi.ac.uk/Tools/dbfetch/dbfetch?db=uniprotkb&id={entry}&format=fasta&style=raw&Retrieve=Retrieve"
            )
            # Gets rid of first line as it returns the fasta format header. Ex. >Saccharomyces cerevisiae (strain ATCC 204508 / S288c)Serine/threonine-protein kinase MPS1'
            sequence = "".join(response.text.split("\n")[1:])
            # print("SEQ:", sequence)
            sequence_list.append(sequence)
            count += 1
            print(f"COMPLETE: Fetching {entry}'s sequence {count}")
        return sequence_list
