IDM to BlackLine Reversal File Generator

A small Python script that takes an incorrect IDM file already sent to BlackLine and generates a matching reversal file with every amount sign-flipped (for example, 300 becomes -300). Loading the reversal file into BlackLine offsets the incorrect data and brings the net balance back to zero.

Problem

IDM processes financial data and sends the resulting files to BlackLine for downstream reconciliation. If incorrect data is processed in IDM and then sent to BlackLine, the amounts in BlackLine become unbalanced and inaccurate.

BlackLine does not provide a way to delete or reverse data it has already processed. Users must submit corrected data to offset the incorrect file, which adds operational effort and increases the risk of reconciliation issues. This happens roughly monthly or quarterly.

Overview

This script automatically generates a reversal file for any incorrectly processed input file.

Give the script the erroneous file as input.
It creates a reversal file by inverting every transaction amount (for example, 300 becomes -300, so (+300) + (-300) = 0).
Load the reversal file into BlackLine. It offsets the incorrect transactions and the net balance returns to zero.
Once the reversal file has processed successfully, send the corrected source data and process it normally.

