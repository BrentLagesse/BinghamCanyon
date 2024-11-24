## New way to accomplish method 2 from my earlier document (fungal conservation)

Use a yeast protein sequence for identifying the corresponding protein in another organism (with BLAST search):

1. Do a BLAST with the yeast protein sequence against a specific genome (Schizosaccharomyces pombe, for example); the genomes to use are listed at the end of this document

   - Go to blast.ncbi.nlm.nih.gov
   - Choose “protein blast”
   - Enter yeast protein sequence in search box
   - For Database - choose nonredundant protein sequences
   - For Organism – enter scientific name of organism (will autofill; choose the one that matches; should also have a taxid #; see list below)
   - Run blast

2. Click on the top hit from the blast search & download the sequence as a FASTA sequence (will give you a .txt file)

3. Copy this sequence & then use for a new blast search – using same method in #1 above, except putting in “Saccharomyces cerevisiae” for the Organism (again, need the taxid #)

4. Compare the first hit from this new search (step #3) with the original sequence used for the 1st blast search (step #1). Maybe run a clustal alignment to compare & look for 100% match?

5. If there is a 100% match of the Saccharomyces cerevisiae hit from step #4 with the original sequence from step #1, then you are done; take the protein sequence downloaded in step #2 & use as the one for that organism for the final alignment

6. If the first result from step #2 doesn’t match 100% to original, then go back to the output from step #2 and repeat steps #3-5 with the 2nd hit

7. Continue to go back to the results from step #2, checking up to the first 5 results, using steps #3-5

8. If none of the first 5 results from step #2 match the original sequence from step #1, then discard that organism & don’t include in the alignment

9. Repeat all of these steps as needed to find a sequence for each organism listed below

Fungi

- Saccharomyces cerevisiae (start sequence)
- Schizosaccharomyces pombe
- Scheffersomyces stipitis
- Ogataea parapolymorpha
- Komagataella phaffii
- Cyberlindnera fabianii
- Kluyveromyces lactis
- Vanderwaltozyma polyspora
- Zygosaccharomyces rouxii
- Saccharomyces paradoxus
- Candida glabrata
- Lachancea fermentati
- Ashbya gossypii
- Torulaspora delbruecki
- Naumovozyma castellii
- Cyberlindnera jadinii
- Pachysolen tannophilus
- Candida auris
