# Method 1

#### Align sequences using Clustal Omega

1. Use either UniProt or Saccaromyces Genome Database (for Saccaromyces cerevisiae) to download sequences. If using UniProt, proceed to step 2. If using SGD, proceed to step 6.

#### **UniProt**

2. Go to uniprot.org. Search gene/protein name or other relevant information in the search bar at the top of the webpage.
3. Click the entry button of the desired entry. This page shows you information about the protein as well as the organism in which it is found.
4. Click the “BLAST” button just under the entry name. Use the default setting.
5. The protein sequence should now appear. Copy this sequence to your clipboard.
6. To more easily search all UniProt results for your desired organism, you can download all results as a FASTA (canonical) file and open using Excel, then search for your organism.

#### Saccaromyces Genome Database

7. Go to yeastgenome.org. Search gene/protein name in the search bar in the top right of the webpage. If this does not pull up information about your protein, you may need to select a protein from the drop down menu of the search bar.
8. Click the “Download” button in the Sequence section. Select whichever type of download applies to you (“Protein” for sequence alignment). 9. Open this download with any file that allows you to see the sequence (I typically use Microsoft Word). Copy this sequence to your clipboard.

#### Clustal Omega

10. Go to https://www.ebi.ac.uk/Tools/msa/clustalo/. This should open the input form for a multiple sequence alignment. 11. Paste your copied sequences into the “sequences in any supported format” box. In the line above the start of your sequence, there should be a ‘greater than’ sign followed by whatever you would like this sequence to be called (>S_cerevisiae)(i.e., FASTA formatted). Note that spaces cannot be used. Sequences can be pasted sequentially, in the same text box. Click submit. 12. Your sequence alignment should now be visible. Go to Results Viewer and copy the url under “View result with Jalview.”

Emily’s notes –

- I think it would be helpful to have 2 ways of doing the alignment for fungal species – one using a species every 10-20 that are coming up when blasting on uniport and one from a list of “typical” strains to use (in which one of us looks up a general phylogenetic tree for fungal species & “intelligently” selects species that represent various degrees of divergence). Maybe it would make sense to do the same for alignments that go up to human.
- When I do the blasts, I only get 100 sequences; is there a way to get more than this?
- Depending on the protein, I can also get proteins with a different name, and this might make automation tricky. For example, Spc105 has many blast hits that are “Spc7” in those organisms, and some are just “Spc7-domain containing protein”. I don’t know whether this will be an issue or not.
