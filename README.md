Assuming discrete log (DLP) to be one way, following implementations are made using Python -

-   Built a provably secure PRG
-   Built a provably secure PRF from PRG
-   Used the PRF in secure mode of operation to obtain a CPA-secure encryption scheme
-   Used the PRF to build a secure MAC.
-   Used the aforementioned CPA security and secure MAC to design a provably CCA-secure encryption scheme
-   Used DLP to build a a fixed length collision resistant hash function
-   Used Merkle-Damgard transform to obtain a provably secure collision resistant hash function
-   Used collision resistant hash function to build H-MACs

