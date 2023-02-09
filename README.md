Final Project for the EPP class
===============================

[![image](https://img.shields.io/github/workflow/status/marinatalantceva/final_project/main/main)](https://github.com/marinatalantceva/final_project/actions?query=branch%3Amain)


[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/marinatalantceva/final_project/main.svg)](https://results.pre-commit.ci/latest/github/marinatalantceva/final_project/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Usage

The following steps must be followed chronologically to understand the purpose as well as the results of this project:

1. Read the following chapter **Project Purpose** to get an intuition what the *Helium Network* is about. We briefly describe what a *Helium* hotspot is and what makes people adopt it. We additionally explain where we get our data from.
2. Run pytask (as explained below).
3. Read the resulting pdf-document. It will provide a description of the prediction model we used in our analysis, as well as a clear data exploration. Additionally, we are using this pdf-document to present and discuss our results (using graphs). Finally, we talk about limitations of our work and give suggestions for future research. 


### pytask information

To get started, create and activate the environment with

```console
$ conda/mamba env create
$ conda activate final_project
```
Now you can build the project using

```console
$ pytask
```


## Project Purpose

### The Helium Network

The purpose of this project is to predict the adoption curve of a new technology using the Bass Model (Bass, 1969), which is well known in the marketing literature and has been widely used in recent decades. This analysis will be based on data from the so-called *Helium Network*.
<br>
<br>
The *Helium Network* is a decentralized, blockchain-based project with the goal of providing a low-power, wide-area network wireless coverage infrastructure for connected devices such as rental vehicles (e.g., e-scooters), or other Internet-of-Things sensors. Unlike traditional communications infrastructure, which is provided by few large commercial providers, the so-called “hotspots” (base stations) are owned and operated by individuals who are paid for offering this connection (Jagtap et al., 2021). The network owner distributes *Helium Tokens* ($HNT) to hotspot owners for transferring data and monitoring the integrity of the network. In turn, a *Helium Token* can be traded on cryptocurrency exchanges for traditional currencies. We study the adoption curve on the city level for a *Helium* hotspot - a small device the size of a consumer Internet router priced at around 400 Euros.

### Data

One of the advantages of having a network running on a blockchain is the decentralized verification of the correctness of data by all network participants. We collect data for every hotspot in a region by scraping the *Helium* blockchain for hotspot data using the *Helium Blockchain API*. We focus on the adoption of hotspots in New York City, USA.


Additional information on how to use the *Helium Blockchain API* can be found in the [Helium Documentation](https://docs.helium.com/api/blockchain/hotspots).

### References

- Bass, F. M. (1969). A new product growth for model consumer durables. *Management Science*, 15(5), 215–227.
- Jagtap, D., Yen, A., Wu, H., Schulman, A., & Pannuto, P. (2021). Federated infrastructure: Usage, patterns, and insights from" the people’s network". *Proceedings of the 21st ACM Internet Measurement Conference*, 22–36.

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).