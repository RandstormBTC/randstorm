# Randstorm

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description
From 2011 - 2015 many popular crypto exchanges used BitcoinJS to generate private keys. 

Unfortunately, for an incredibly popular library, there was an issue in BitcoinJS:

“The most common variations of the library attempts to collect entropy
from window.crypto's CSPRNG, but due to a type error in a comparison
this function is silently stepped over without failing. Entropy is
subsequently gathered from math.Random (a 48bit linear congruential
generator, seeded by the time in some browsers), and a single
execution of a medium resolution timer. In some known configurations
this system has substantially less than 48 bits of entropy.”

This program generates a Random Private Key using the python equivalent to SecureRandom() in JSBN javascript library with Math.random(). 

![GitHub Logo]([https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png](https://images.squarespace-cdn.com/content/v1/6156001e4a686e24886bd0b2/95aaea52-0f97-45ec-b251-fd1a0890040a/Screenshot+from+2023-11-13+16-54-13.png?format=1500w))

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

Provide step-by-step instructions on how to install your project. You can include code snippets or commands if necessary.

```bash
npm install
