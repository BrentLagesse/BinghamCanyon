# BinghamCanyon

## Abstract:
Saccharomyces cerevisiae, commonly known as yeast, originated hundreds of millions of years ago, while humans emerged only hundreds of thousands of years ago. Despite this vast difference in evolutionary time, there are still proteins that we share. This project aims to automate the analysis of RNA protein sequences in yeast cells to identify conserved and divergent regions within the same protein across a wide range of species, including humans.
## Project Goals:
The biologists have 3 main methods they requested to be implemented. They provided clear, step-by-step instructions for implementing the three methods and the steps after
1.	Method 1: Analyze a given yeast protein and identify similar proteins in any species based on their conservation score.
2.	Method 2: Analyze a given yeast protein specifically across pre-defined fungal species.
3.	Method 3: Analyze a given yeast protein across evolutionary timeframes (wide range of species including humans)
Using the selected method, the project will automatically fetch the protein model, align the protein sequences, and launch Jalview and ChimeraX with the relevant data.
## Methodology & Design:
We utilized Python for its extensive library support and implemented dependency injection to enhance the system's flexibility. This design allows for easy swapping of API. Currently, the system uses with REST APIs from the European Bioinformatics Institute (EBI). However, in the future, we may download the database to perform our own queries, reducing reliance on third-party software. With this architecture, changing the API requires modifying only one line of code, a process made possible by Python’s Protocols, which effectively serve as an interface.

1.	Collaborated closely with biologists via Zoom and email to identify functional requirements, getting feedback on the current status of the project, and gather necessary biology-related information.
2.	Consulted with Professor Brent Lagesse to discuss the structure and design of the code.
3.	Researched how to programmatically execute the instructions provided by the biologists and began coding the project, followed by refactoring the code when necessary
4.	Repeat steps 1-3, continuing further development and refinement based on feedback received.
