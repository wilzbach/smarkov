#!/usr/bin/env python
# -*- coding: utf-8 -*-

from smarkov import Markov

chain = Markov(["AGACAGACGAC"])
print("".join(chain.generate_text()))
