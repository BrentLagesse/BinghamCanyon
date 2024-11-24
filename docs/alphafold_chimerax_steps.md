## AlphaFold structure prediction

1. Go to alphafoldserver.com
2. Enter protein sequence in the window provided
3. Once structure has been generated, download the files

## ChimeraX

4. Open the five .cif files in ChimeraX (just drag them in to ChimeraX; these are five different structure predictions)
5. Overlay them by going to Structure Analysis & choosing Matchmaker; just use default settings
6. Open the Jalview alignment in ChimeraX (just drag it in)
7. Right click while hovering over the alignment window & choose Structure, then Associations, then choose one of the models (top one is probably fine) – this will associate the alignment with a sequence/structure
8. Then type into the command line at the bottom: color byattr seq_conservation palette blue:white:red range -1.5,1.5
9. Structure should now be colored with red as most conserved & blue as least conserved
10. Changing the numbers for the range will change the look of the colored conservation
11. I’m not sure of the “best” numbers to use for a default, but maybe the -1.5 to 1.5 is fine; I’ll get back to you on this
12. All structures will now be colored by conservation
13. For easier viewing, go to the Models panel & choose just one of them to be viewed (click off the boxes for the other 4)
